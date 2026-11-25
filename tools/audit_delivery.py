"""Check staged bytes and secret/size exclusions without printing credentials."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

root = Path(__file__).resolve().parents[1]
entries = subprocess.check_output(['git', 'ls-files', '-s', '-z'], cwd=root).split(b'\0')
findings = {'staged_files': 0, 'staged_bytes': 0, 'byte_mismatches': [], 'credential_like_paths': [], 'over_5mb': []}
for entry in entries:
    if not entry:
        continue
    meta, raw_name = entry.split(b'\t', 1)
    name = raw_name.decode('utf-8')
    expected = meta.split()[1].decode()
    data = (root / name).read_bytes()
    actual = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    findings['staged_files'] += 1
    findings['staged_bytes'] += len(data)
    if actual != expected:
        findings['byte_mismatches'].append(name)
    if re.search(rb'\bsk-[A-Za-z0-9_-]{20,}', data):
        findings['credential_like_paths'].append(name)
    if len(data) > 5 * 1024 * 1024:
        findings['over_5mb'].append({'path': name, 'bytes': len(data)})
print(json.dumps(findings, ensure_ascii=False, indent=2))
assert not any(findings[k] for k in ('byte_mismatches', 'credential_like_paths', 'over_5mb'))
