from contextlib import redirect_stdout
import io
from pathlib import Path
import shutil
import tempfile
import unittest

from scripts.verify_public_site import ARCHIVES, ASSETS, ROOT, verify


class PublicSiteTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.site = Path(self.temp.name)
        for name in (*ASSETS, 'index.html', 'support.html'):
            target = self.site / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        for name in ARCHIVES:
            target = self.site / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text('<html><head><link rel="stylesheet" href="/styles.css"></head><body><img src="/icons/apple-touch-icon.png" alt=""></body></html>', encoding='utf-8')

    def check(self):
        with redirect_stdout(io.StringIO()):
            return verify(self.site)

    def test_valid_build_preserves_public_contract(self):
        self.assertEqual(self.check(), [])

    def test_altered_feed_and_missing_archive_block_publication(self):
        (self.site / 'jobs.csv').write_text('not,a,feed', encoding='utf-8')
        (self.site / ARCHIVES[0]).unlink()
        errors = self.check()
        self.assertTrue(any('jobs.csv: missing or changed' in e for e in errors))
        self.assertTrue(any('supported 15- or 16-column' in e for e in errors))
        self.assertTrue(any('expected language archive missing' in e for e in errors))

    def test_broken_generated_image_and_internal_source_block_publication(self):
        (self.site / ARCHIVES[0]).write_text('<img src="/media/images/missing.png" alt="Example">', encoding='utf-8')
        (self.site / 'PAGES_RUNBOOK.md').write_text('internal', encoding='utf-8')
        errors = self.check()
        self.assertTrue(any('missing local resource' in e for e in errors))
        self.assertTrue(any('internal source' in e for e in errors))

    def test_legacy_root_prefix_resource_is_not_accepted(self):
        (self.site / ARCHIVES[0]).write_text(
            '<link rel="stylesheet" href="/nottinghamshire-jobs/styles.css">',
            encoding='utf-8',
        )
        self.assertTrue(any('missing local resource' in e for e in self.check()))

    def test_missing_or_modified_public_preview_blocks_publication(self):
        demo = self.site / 'demos' / 'my-next-step-en.html'
        demo.write_text('altered demo', encoding='utf-8')
        errors = self.check()
        self.assertTrue(any('demos/my-next-step-en.html: missing or changed' in e for e in errors))
        demo.unlink()
        errors = self.check()
        self.assertTrue(any('demos/my-next-step-en.html: missing or changed' in e for e in errors))

    def test_changed_support_and_missing_public_asset_block_publication(self):
        (self.site / 'support.html').write_text('<html>Missing enquiry</html>', encoding='utf-8')
        (self.site / 'locale.js').unlink()
        errors = self.check()
        self.assertTrue(any('enquiry destination missing' in e for e in errors))
        self.assertTrue(any('locale.js: missing or changed' in e for e in errors))


if __name__ == '__main__':
    unittest.main()
