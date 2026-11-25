"""Trusted policy for the sole initial Wiki Agent path."""
import re

PATH = 'docs/faq/index.md'
MAX_BYTES = 16_384
FORBIDDEN = re.compile(
    r'[<>{}\[\]`\\]|https?\s*[:：]|\b(?:gh[pousr]_[a-z0-9]+|github_pat_[a-z0-9_]+)\b|'
    r'\b(?:oc|ou|om|cli)_[a-z0-9_-]{8,}\b|\b(?:localhost|token|api[_ -]?key|password|private key)\b|'
    r'(?<!\d)(?:\d{1,3}\.){3}\d{1,3}(?!\d)|[\x00-\x08\x0b-\x1f\x7f]',
    re.IGNORECASE,
)

def validate_candidate(text):
    if len(text.encode('utf-8')) > MAX_BYTES or FORBIDDEN.search(text):
        raise ValueError('Candidate does not meet the public FAQ publication policy')
    if not text.startswith('# 常见问题\n') or any(line.startswith(('    ', '\t', '---', ':::')) for line in text.splitlines()):
        raise ValueError('Candidate is outside the safe Markdown grammar')
    return text
