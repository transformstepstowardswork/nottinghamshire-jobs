"""Inspect the real Actions YAML and exercise material publication-gate mutations.

Run explicitly with development-only PyYAML; ordinary weekly CSV tests need no
additional dependency. This checks source control flow, not GitHub deployment.
"""
from copy import deepcopy
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
GATE = './.github/actions/build-verified-pages'
MAIN_ONLY = "github.event_name == 'push' && github.ref == 'refs/heads/main'"


def load(path):
    # GitHub uses YAML 1.2. BaseLoader preserves 'on' and scalar values verbatim.
    return yaml.load((ROOT / path).read_text(encoding='utf-8'), Loader=yaml.BaseLoader)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def check_production(workflow, gate):
    require(workflow['on'] == {'push': {'branches': ['main']}}, 'push to main only; no manual/PR deploy')
    require(workflow['permissions'] == {'contents': 'read'}, 'build token must be read-only')
    require(workflow['concurrency'] == {'group': 'pages-production', 'cancel-in-progress': 'true'}, 'cancel superseded production runs')
    require(set(workflow['jobs']) == {'build', 'deploy'}, 'one build and one downstream deploy')
    build, deploy = workflow['jobs']['build'], workflow['jobs']['deploy']
    require(build['if'] == deploy['if'] == MAIN_ONLY, 'both jobs restricted to main push')
    require(deploy['needs'] == 'build', 'deploy must need successful build')
    require('continue-on-error' not in build and 'continue-on-error' not in deploy, 'no ignored job failures')
    require('permissions' not in build, 'no extra build permission')
    require(deploy['permissions'] == {'pages': 'write', 'id-token': 'write'}, 'deploy-only minimum write permissions')
    require(deploy['environment']['name'] == 'github-pages', 'Pages protected environment')
    steps = build['steps']
    require(len(steps) == 3, 'no second checkout/rebuild/mutation between gate and upload')
    require(steps[0]['uses'] == 'actions/checkout@v4', 'checkout before gate')
    require(steps[0]['with'] == {'ref': '${{ github.sha }}', 'persist-credentials': 'false'}, 'checkout immutable triggering commit without stored credential')
    require(steps[1]['uses'] == GATE, 'real shared production build gate')
    require(steps[2]['uses'] == 'actions/upload-pages-artifact@v4', 'official Pages artifact format')
    require(steps[2]['with']['path'] == '_site', 'upload same verified directory')
    require(steps[2]['with']['name'] == 'github-pages', 'single production artifact')
    for step in steps:
        require(not any(key in step for key in ('if', 'continue-on-error')), 'gate and upload require default success semantics')
    require(gate['runs']['using'] == 'composite', 'shared build gate is inspectable')
    gate_steps = gate['runs']['steps']
    require(len(gate_steps) == 3, 'one build then both real output verifiers')
    require(gate_steps[0]['uses'] == 'actions/jekyll-build-pages@v1', 'official Pages Jekyll builder')
    require(gate_steps[0]['with'] == {'source': './', 'destination': './_site', 'build_revision': '${{ github.event.pull_request.head.sha || github.sha }}'}, 'immutable source revision and one destination')
    require([s['run'] for s in gate_steps[1:]] == ['python scripts/verify_editorial_html.py _site', 'python scripts/verify_public_site.py _site'], 'real output must pass both verifiers before upload')
    for step in gate_steps:
        require(not any(key in step for key in ('if', 'continue-on-error')), 'shared gate must fail closed')
    deploy_steps = deploy['steps']
    require(len(deploy_steps) == 2, 'only freshness check then deploy; no rebuilding')
    require('git ls-remote https://github.com/transformstepstowardswork/nottinghamshire-jobs.git refs/heads/main' in deploy_steps[0]['run'] and '"$GITHUB_SHA"' in deploy_steps[0]['run'], 'refuse stale reruns before deployment')
    require(deploy_steps[1]['uses'] == 'actions/deploy-pages@v4', 'official deployment')
    require(deploy_steps[1]['with']['artifact_name'] == 'github-pages', 'deploy exactly the upstream artifact')
    for step in deploy_steps:
        require(not any(key in step for key in ('if', 'continue-on-error')), 'deploy cannot bypass freshness/failure')
    config = load('_config.yml')
    require(config['baseurl'] == '', 'custom-domain publication must use site root base path')


class WorkflowSafetyTests(unittest.TestCase):
    def setUp(self):
        self.workflow = load('.github/workflows/pages-publish.yml')
        self.gate = load('.github/actions/build-verified-pages/action.yml')

    def test_actual_production_graph(self):
        check_production(self.workflow, self.gate)

    def test_rejects_material_gate_bypasses(self):
        mutations = [
            lambda w: w['jobs']['deploy'].pop('needs'),
            lambda w: w['jobs']['deploy'].update({'needs': 'unverified'}),
            lambda w: w['jobs']['deploy'].update({'if': 'always()'}),
            lambda w: w['jobs']['build']['steps'][1].update({'continue-on-error': 'true'}),
            lambda w: w['jobs']['build']['steps'][2].update({'if': 'always()'}),
            lambda w: w['jobs']['build']['steps'][2]['with'].update({'path': '.'}),
            lambda w: w['jobs']['build']['steps'].reverse(),
            lambda w: w['jobs']['build']['steps'][0]['with'].update({'ref': 'main'}),
            lambda w: w['permissions'].update({'pages': 'write'}),
            lambda w: w['on'].update({'workflow_dispatch': ''}),
            lambda w: w['jobs']['deploy']['steps'][1]['with'].update({'artifact_name': 'fixture-site'}),
        ]
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                candidate = deepcopy(self.workflow)
                mutation(candidate)
                with self.assertRaises((AssertionError, KeyError)):
                    check_production(candidate, self.gate)
        unsafe_gate = deepcopy(self.gate)
        unsafe_gate['runs']['steps'][1]['continue-on-error'] = 'true'
        with self.assertRaises(AssertionError):
            check_production(self.workflow, unsafe_gate)

    def test_non_deploying_evidence_uses_real_gate_and_handoff(self):
        readiness = load('.github/workflows/pages-readiness.yml')
        self.assertEqual(readiness['permissions'], {'contents': 'read'})
        self.assertEqual(readiness['jobs']['handoff']['needs'], 'build')
        for job in readiness['jobs'].values():
            self.assertNotIn('permissions', job)
            self.assertNotIn('environment', job)
        actual = readiness['jobs']['build']['steps']
        self.assertEqual(actual[1]['uses'], GATE)
        self.assertEqual(actual[2]['uses'], 'actions/upload-pages-artifact@v4')
        self.assertEqual(actual[2]['with']['path'], '_site')
        hostile = readiness['jobs']['hostile']['steps']
        self.assertEqual(hostile[2]['uses'], GATE)
        self.assertEqual(hostile[2]['continue-on-error'], 'true')
        self.assertEqual(hostile[3]['if'], "steps.gate.outcome == 'success'")
        self.assertIn('test "$UPLOAD_OUTCOME" = skipped', hostile[4]['run'])
        self.assertIn('unsupported URL scheme', hostile[4]['run'])
        self.assertIn('sha256sum --check', readiness['jobs']['handoff']['steps'][-1]['run'])

    def test_only_canonical_workflow_can_deploy(self):
        deployers = []
        for path in (ROOT / '.github/workflows').glob('*.yml'):
            workflow = load(path.relative_to(ROOT))
            for job in workflow['jobs'].values():
                for step in job.get('steps', []):
                    if step.get('uses', '').startswith('actions/deploy-pages@'):
                        deployers.append(path.name)
            if path.name != 'pages-publish.yml':
                self.assertEqual(workflow['permissions'], {'contents': 'read'}, path.name)
        self.assertEqual(deployers, ['pages-publish.yml'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
