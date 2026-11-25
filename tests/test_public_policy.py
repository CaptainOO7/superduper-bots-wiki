import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from public_policy import validate_candidate
from stage_previews import eligible

class PublicPolicy(unittest.TestCase):
    def test_current_faq_is_previewable(self):
        validate_candidate(Path('docs/faq/index.md').read_text())

    def test_active_content_and_sensitive_identifiers_are_refused(self):
        for item in ('<script>run()</script>', '{{ 2 + 2 }}', '[bad](https://example.com)',
                     'ou_12345678', '192.168.1.2', '---', '    content', 'password'):
            with self.subTest(item=item), self.assertRaises(ValueError):
                validate_candidate('# 常见问题\n' + item)

    def test_wrong_actor_and_fork_are_refused(self):
        pr = {'user': {'login':'docs-writer[bot]'}, 'draft':True, 'base':{'ref':'main'},
              'head':{'repo':{'full_name':'example/wiki'}, 'ref':'mvp-e2e/'+'1'*32, 'sha':'2'*40}}
        self.assertTrue(eligible(pr, 'example/wiki', 'docs-writer[bot]'))
        self.assertFalse(eligible(pr, 'example/wiki', 'unexpected[bot]'))
        pr['head']['repo']['full_name'] = 'fork/wiki'
        self.assertFalse(eligible(pr, 'example/wiki', 'docs-writer[bot]'))
