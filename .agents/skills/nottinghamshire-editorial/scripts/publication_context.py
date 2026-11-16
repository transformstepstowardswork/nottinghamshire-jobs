"""Emit checked GitHub arguments for this project's editorial publication.

Read-only: no network, file writes, commits or merges. Approval, live PR state
and CI must still be checked by the caller.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

EXPECTED_REPOSITORY = "transformstepstowardswork/nottinghamshire-jobs"


def repository_from_remote(remote):
    match = re.fullmatch(
        r"(?:https://github\.com/|git@github\.com:|ssh://git@github\.com/)"
        r"([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+?)(?:\.git)?/?",
        remote.strip(),
    )
    if not match or match[1].casefold() != EXPECTED_REPOSITORY.casefold():
        raise ValueError("origin must identify " + EXPECTED_REPOSITORY)
    return EXPECTED_REPOSITORY


def publication_context(remote, pr_url=None, expected_head=None, merge_method=None):
    repository = repository_from_remote(remote)
    if pr_url is None:
        if expected_head is not None or merge_method is not None:
            raise ValueError("A verified --pr-url is required for merge arguments")
        return {"repository_full_name": repository}
    match = re.fullmatch(
        r"https://github\.com/([^/\s]+/[^/\s]+)/pull/([1-9][0-9]*)/?",
        pr_url,
    )
    if not match or match[1].casefold() != repository.casefold():
        raise ValueError("PR URL must belong to https://github.com/" + repository)
    if (expected_head is None) != (merge_method is None):
        raise ValueError("Supply both --expected-head and --merge-method for merge arguments")
    if expected_head is not None and not re.fullmatch(r"[0-9a-fA-F]{40}", expected_head):
        raise ValueError("Expected head must be a complete 40-character Git SHA")
    if merge_method is not None and merge_method not in {"merge", "squash", "rebase"}:
        raise ValueError("Unsupported merge method")
    number = int(match[2])
    result = {
        "repository_full_name": repository,
        "pr_url": f"https://github.com/{repository}/pull/{number}",
        "read_pr_args": {"repo_full_name": repository, "pr_number": number},
        "main_runs_url": (
            f"https://api.github.com/repos/{repository}/actions/runs"
            "?branch=main&event=push&per_page=10"
        ),
    }
    if expected_head is not None:
        result["merge_pr_args"] = {
            "repository_full_name": repository,
            "pr_number": number,
            "expected_head_sha": expected_head.lower(),
            "merge_method": merge_method,
        }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr-url")
    parser.add_argument("--expected-head")
    parser.add_argument("--merge-method", choices=("merge", "squash", "rebase"))
    args = parser.parse_args()
    try:
        root = Path(__file__).resolve().parents[4]
        active_root = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], text=True, stderr=subprocess.PIPE
        ).strip()
        if Path(active_root).resolve() != root:
            raise ValueError("Run from this skill's repository working tree")
        remote = subprocess.check_output(
            ["git", "remote", "get-url", "origin"], text=True, stderr=subprocess.PIPE
        ).strip()
        result = publication_context(
            remote, args.pr_url, args.expected_head, args.merge_method
        )
    except (OSError, subprocess.CalledProcessError, ValueError) as exc:
        message = str(exc) if isinstance(exc, ValueError) else "Cannot read local Git identity"
        parser.exit(2, f"Publication context error: {message}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()