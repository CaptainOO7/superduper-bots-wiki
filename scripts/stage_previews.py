"""Fetch only reviewed Markdown bytes by immutable SHA and build with checked-in Wiki code."""
import base64
import json
import os
from pathlib import Path
import re
import urllib.request
from public_policy import PATH, validate_candidate

def api(repository, suffix, token):
    request = urllib.request.Request('https://api.github.com/repos/' + repository + suffix, headers={
        'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer ' + token,
        'X-GitHub-Api-Version': '2022-11-28',
    })
    with urllib.request.urlopen(request, timeout=15) as response:
        return json.loads(response.read(4 * 1024 * 1024 + 1))

def eligible(pr, repository, writer):
    return (writer and pr['user']['login'].casefold() == writer.casefold() and pr['draft'] and
            pr['base']['ref'] == 'main' and pr['head']['repo'] is not None and
            pr['head']['repo']['full_name'].casefold() == repository.casefold() and
            re.fullmatch(r'mvp-e2e/[0-9a-f]{32}', pr['head']['ref']) and
            re.fullmatch(r'[0-9a-f]{40}', pr['head']['sha']))

def stage(repository, writer, token, docs):
    for page in range(1, 11):
        pulls = api(repository, f'/pulls?state=open&per_page=100&page={page}', token)
        for pr in pulls:
            if not eligible(pr, repository, writer):
                continue
            number, sha = pr['number'], pr['head']['sha']
            files = api(repository, f'/pulls/{number}/files?per_page=3', token)
            if len(files) != 1 or files[0]['filename'] != PATH or files[0]['status'] != 'modified':
                continue
            item = api(repository, f'/contents/{PATH}?ref={sha}', token)
            if item.get('type') != 'file' or item.get('path') != PATH or item.get('encoding') != 'base64':
                continue
            try:
                data = base64.b64decode(''.join(item['content'].split()), validate=True)
                candidate = validate_candidate(data.decode('utf-8'))
            except (ValueError, UnicodeError):
                print(f'PR {number}: candidate violates the public policy')
                continue
            current = api(repository, f'/pulls/{number}', token)
            if current['state'] != 'open' or current['head']['sha'] != sha or not eligible(current, repository, writer):
                continue
            folder = docs / 'previews' / f'pr-{number}'
            folder.mkdir(parents=True, exist_ok=True)
            (folder / 'index.md').write_text(
                f'---\nsearch: false\n---\n\n# Draft PR {number} preview\n\nCandidate commit `{sha}`\n\n' +
                candidate.replace('# 常见问题', '## 常见问题', 1), encoding='utf-8',
            )
            marker = docs / 'public' / 'previews' / f'pr-{number}'
            marker.mkdir(parents=True, exist_ok=True)
            (marker / 'candidate.json').write_text(json.dumps({'number': number, 'sha': sha}), encoding='utf-8')
        if len(pulls) < 100:
            return
    raise RuntimeError('Open PR limit exceeded')

if __name__ == '__main__':
    stage(os.environ['GITHUB_REPOSITORY'], os.environ.get('WIKI_PREVIEW_WRITER', ''),
          os.environ['GITHUB_TOKEN'], Path('docs'))
