import base64
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from public_policy import validate_candidate
from stage_previews import eligible, stage

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

    def test_exact_sha_preview_and_stale_cleanup(self):
        sha = '2'*40
        pr = {'number':5, 'state':'open', 'user': {'login':'docs-writer[bot]'},
              'draft':True, 'base':{'ref':'main'}, 'head':{'repo':{'full_name':'example/wiki'},
              'ref':'mvp-e2e/'+'1'*32, 'sha':sha}}
        faq = Path('docs/faq/index.md').read_text()
        content = {'type':'file', 'path':'docs/faq/index.md', 'encoding':'base64',
                   'content':base64.b64encode(faq.encode()).decode()}
        files = [{'filename':'docs/faq/index.md','status':'modified'}]
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            with patch('stage_previews.api', side_effect=[[pr],files,content,pr]) as api:
                stage('example/wiki','docs-writer[bot]','test',docs)
            self.assertTrue(api.call_args_list[2].args[1].endswith('?ref='+sha))
            self.assertEqual(json.loads((docs/'public/previews/pr-5/candidate.json').read_text()), {'number':5,'sha':sha})
            self.assertIn('## 常见问题', (docs/'previews/pr-5/index.md').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            docs = Path(tmp)
            with patch('stage_previews.api', side_effect=[[pr],files,content,{**pr,'state':'closed'}]):
                stage('example/wiki','docs-writer[bot]','test',docs)
            self.assertFalse((docs/'previews').exists())
