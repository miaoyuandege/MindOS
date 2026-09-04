import hashlib
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('preflight', ROOT/'tools/prepublish_scan.py')
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)


class CandidateTests(unittest.TestCase):
    def fixture(self, content, name='example.md'):
        tmp = tempfile.TemporaryDirectory(); self.addCleanup(tmp.cleanup)
        root = Path(tmp.name); (root/name).write_text(content, encoding='utf-8')
        return root

    def test_credentials_block_without_echoing_values(self):
        value = 'sk-' + 'syntheticvalueonly' * 2
        result = scanner.scan(self.fixture(value), False)
        self.assertFalse(result['passed'])
        self.assertNotIn(value, json.dumps(result))

    def test_keywords_are_not_credentials(self):
        result = scanner.scan(self.fixture('Do not upload secret, Authorization, Cookie, Bearer or API key values.'), False)
        self.assertTrue(result['passed'])
        self.assertIn('expected synthetic/example', result['categories'])

    def test_unknown_address_and_absolute_path_need_review(self):
        address = '.'.join(['10','42','17','8'])
        absolute = 'Q:' + chr(92) + 'private'
        result = scanner.scan(self.fixture(address + '\n' + absolute), False)
        self.assertFalse(result['passed'])
        self.assertIn('suspicious', result['categories'])

    def test_documentation_address_is_classified(self):
        result = scanner.scan(self.fixture('https://example.com and 192.0.2.4'), False)
        self.assertTrue(result['passed'])

    def test_private_data_file_blocked_even_when_ignored(self):
        root = self.fixture('not real history', 'raw.jsonl')
        (root/'.gitignore').write_text('*.jsonl\n', encoding='utf-8')
        self.assertFalse(scanner.scan(root, False)['passed'])

    def test_reviewed_public_reference_hosts_are_exact(self):
        self.assertTrue(scanner.scan(self.fixture('https://learn.chatgpt.com/docs/build-skills'), False)['passed'])
        fake_host = 'https' + '://' + 'learn.chatgpt.com' + '.invalid/docs'
        self.assertFalse(scanner.scan(self.fixture(fake_host), False)['passed'])

    def test_loopback_port_is_not_external(self):
        self.assertTrue(scanner.scan(self.fixture('http://127.0.0.1:9'), False)['passed'])

    def test_manifest_detects_modified_and_unmapped_assets(self):
        root = self.fixture('safe')
        (root/'docs').mkdir()
        data={'assets':[{'path':'example.md','origin':'NEW','transformation':'synthetic','sha256':hashlib.sha256(b'safe').hexdigest()}]}
        (root/scanner.MANIFEST).write_text(json.dumps(data),encoding='utf-8')
        self.assertTrue(scanner.scan(root)['passed'])
        (root/'example.md').write_text('changed',encoding='utf-8')
        self.assertFalse(scanner.scan(root)['passed'])
        (root/'extra.md').write_text('unknown origin',encoding='utf-8')
        self.assertTrue(any(x['rule']=='unmapped_or_missing_assets' for x in scanner.scan(root)['findings']))

    def test_root_license_is_scanned_not_exempted(self):
        self.assertTrue(scanner.scan(self.fixture('MIT License', 'LICENSE'), False)['passed'])
        value = 'sk-' + 'syntheticvalueonly' * 2
        self.assertFalse(scanner.scan(self.fixture(value, 'LICENSE'), False)['passed'])
        self.assertFalse(scanner.scan(self.fixture('unknown', 'LICENSE-other'), False)['passed'])
        root = self.fixture('safe')
        (root/'nested').mkdir()
        (root/'nested/LICENSE').write_text('not allowlisted', encoding='utf-8')
        self.assertFalse(scanner.scan(root, False)['passed'])

    def test_candidate_links_exist(self):
        for path in ROOT.rglob('*.md'):
            for raw in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8-sig')):
                target=unquote(raw.strip('<>').split('#')[0])
                if not target or '://' in target: continue
                self.assertTrue((path.parent/target).exists(),f'{path.relative_to(ROOT)}: {target}')

    def test_candidate_has_mit_license(self):
        self.assertEqual(hashlib.sha256((ROOT/'LICENSE').read_bytes()).hexdigest(), '6f2c4c9dc24551fa09b715bac553e4523dc870fdec737c5548633fc7e523769d')
        license_text = (ROOT/'LICENSE').read_text(encoding='utf-8')
        self.assertIn('Copyright (c) 2026 miaoyuandege', license_text)
        self.assertTrue(license_text.startswith('MIT License\n'))
        self.assertEqual(len(list((ROOT/'core/templates').glob('*.md'))),6)


if __name__ == '__main__': unittest.main()
