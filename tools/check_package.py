#!/usr/bin/env python3
"""Check a repository or a standalone skill. Python standard library only.

This checks files and package structure, not research truth, copyright, oral
quality, native application rendering, or installation into a client.
"""
import argparse
import hashlib
import json
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

TEXT_EXTENSIONS = {'.md', '.json', '.yaml', '.yml', '.py', '.txt'}
NS = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'dc': 'http://purl.org/dc/elements/1.1/',
      'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties'}
errors = []
counts = {'files': 0, 'links': 0, 'skills': 0, 'pptx': 0}

def fail(message):
    errors.append(message)

def digest(file):
    return hashlib.sha256(file.read_bytes()).hexdigest()

def local_resource(base, target, root, context):
    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', target) or target.startswith('#'):
        return
    target = target.split('#', 1)[0].split('?', 1)[0]
    if not target:
        return
    target = target.strip('<>')
    resource = (base / target).resolve()
    try:
        resource.relative_to(root)
    except ValueError:
        fail(f'{context}: resource escapes checked root: {target}')
        return
    if not resource.is_file():
        fail(f'{context}: missing resource: {target}')
    counts['links'] += 1

def check_skill(skill):
    text = (skill / 'SKILL.md').read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---(?:\n|$)', text, re.S)
    if not match:
        fail(f'{skill.name}: missing frontmatter')
        return
    # A minimal scalar check; use the client's YAML-aware quick_validate too.
    fields = dict(re.findall(r'^([a-z-]+):\s*(.+)$', match.group(1), re.M))
    if fields.get('name') != skill.name or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', fields.get('name', '')):
        fail(f'{skill.name}: name does not match directory')
    if not fields.get('description') or len(fields['description']) > 1024:
        fail(f'{skill.name}: missing or excessive description')
    ui = skill / 'agents/openai.yaml'
    if not ui.is_file():
        fail(f'{skill.name}: missing UI metadata')
    else:
        content = ui.read_text(encoding='utf-8')
        for key in ('display_name', 'short_description', 'default_prompt'):
            if not re.search(r'^\s+' + key + r':\s*\S', content, re.M):
                fail(f'{skill.name}: missing UI {key}')
        if '$' + skill.name not in content:
            fail(f'{skill.name}: default prompt does not name skill')
        for icon in re.findall(r'^\s+icon_(?:small|large):\s*"([^"]+)"', content, re.M):
            local_resource(skill, icon, checked_root, f'{skill.name} UI')
    counts['skills'] += 1

def check_ppt(file):
    counts['pptx'] += 1
    with zipfile.ZipFile(file) as z:
        names = set(z.namelist())
        for required in ('[Content_Types].xml', '_rels/.rels', 'ppt/presentation.xml'):
            if required not in names:
                fail(f'{file.name}: missing {required}')
        for name in names:
            if name.endswith('.xml') or name.endswith('.rels'):
                try:
                    ET.fromstring(z.read(name))
                except ET.ParseError:
                    fail(f'{file.name}: malformed XML {name}')
            if name.endswith('.rels'):
                rels = ET.fromstring(z.read(name))
                base = posixpath.dirname(posixpath.dirname(name))
                for rel in rels:
                    if rel.get('TargetMode') == 'External':
                        fail(f'{file.name}: unexpected external relationship')
                        continue
                    target = rel.get('Target', '').split('#', 1)[0]
                    resolved = (target.lstrip('/') if target.startswith('/') else
                                posixpath.normpath(posixpath.join(base, target)))
                    if resolved not in names:
                        fail(f'{file.name}: missing relationship target {resolved}')
        slides = [n for n in names if re.fullmatch(r'ppt/slides/slide\d+\.xml', n)]
        notes = [n for n in names if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml', n)]
        tables = sum(len(ET.fromstring(z.read(n)).findall('.//a:tbl', NS)) for n in slides)
        if len(slides) != 16 or len(notes) != 16 or tables != 1:
            fail(f'{file.name}: expected sixteen complete template pages, sixteen notes and one native table')
        media = [n for n in names if n.startswith('ppt/media/') and not n.endswith('/')]
        if file.name == 'blank-template.pptx':
            if media:
                fail(f'{file.name}: blank template must not contain research images')
        elif file.name in {'reference.pptx', 'soc-reference.pptx'}:
            if len(media) != 8 or any(not n.endswith('.png') for n in media):
                fail(f'{file.name}: expected eight documented research PNGs')
        else:
            fail(f'{file.name}: unrecognized presentation role')
        if any(n.startswith(('ppt/fonts/', 'ppt/embeddings/', 'ppt/comments/', 'customXml/')) for n in names):
            fail(f'{file.name}: unexpected font, attachment, comment or custom XML')
        if 'docProps/custom.xml' in names:
            fail(f'{file.name}: custom document properties retained')
        if 'docProps/core.xml' in names:
            core = ET.fromstring(z.read('docProps/core.xml'))
            for tag in ('dc:creator', 'cp:lastModifiedBy'):
                node = core.find(tag, NS)
                if node is not None and (node.text or '').strip():
                    fail(f'{file.name}: personal editor metadata retained')
        for name in names:
            if name.endswith(('.xml', '.rels')):
                text = z.read(name).decode('utf-8')
                if re.search(r'(?i)\b[a-z]:[\\/]', text) or re.search(r'/(?:Users|home)/[^/\s]+/', text):
                    fail(f'{file.name}: private absolute path in {name}')
        # Validate the full reference script against actual note text, not a generic talk.
        if file.name in {'reference.pptx', 'soc-reference.pptx'}:
            talk = file.parent.parent / 'examples/reference-talk.md'
            if not talk.is_file():
                fail(f'{file.name}: missing paired original notes')
            else:
                sections = re.split(r'^## P(\d+)\s*$', talk.read_text(encoding='utf-8'), flags=re.M)
                actual = {int(sections[i]): sections[i+1].strip() for i in range(1, len(sections), 2)}
                if set(actual) != set(range(1, 17)):
                    fail(f'{file.name}: paired script must contain pages 1 through 16')
                for i in range(1, 17):
                    note = ET.fromstring(z.read(f'ppt/notesSlides/notesSlide{i}.xml'))
                    paragraphs = []
                    for shape in note.findall('.//{http://schemas.openxmlformats.org/presentationml/2006/main}sp'):
                        ph = shape.find('.//{http://schemas.openxmlformats.org/presentationml/2006/main}ph')
                        if ph is not None and ph.get('type') == 'body':
                            paragraphs.extend(''.join(t.text or '' for t in para.findall('.//a:t', NS))
                                              for para in shape.findall('.//a:p', NS))
                    expected = '\n\n'.join(p for p in paragraphs if p.strip()).strip()
                    if actual.get(i) != expected:
                        fail(f'{file.name}: script differs from actual notes on page {i}')

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('root', nargs='?', default='.')
args = parser.parse_args()
checked_root = Path(args.root).resolve()
if not checked_root.is_dir():
    parser.error('root must be an existing directory')
files = sorted(p for p in checked_root.rglob('*') if p.is_file()
               and not any(part in {'.git', '__pycache__', 'node_modules'} for part in p.relative_to(checked_root).parts))
for file in files:
    counts['files'] += 1
    relative = file.relative_to(checked_root).as_posix()
    if file.suffix in TEXT_EXTENSIONS:
        text = file.read_text(encoding='utf-8')
        if re.search(r'(?i)\b[a-z]:[\\/]', text) or re.search(r'/(?:Users|home)/[^/\s]+/', text):
            fail(f'{relative}: machine-specific absolute path')
        if file.suffix == '.md':
            for target in re.findall(r'!?\[[^\]]*\]\(([^)\n]+)\)', text):
                local_resource(file.parent, target, checked_root, relative)
    if file.suffix == '.json':
        data = json.loads(file.read_text(encoding='utf-8'))
        if file.name == 'artifact-template.json':
            if data.get('kind') != 'presentation' or data.get('schemaVersion') != 1:
                fail(f'{relative}: incorrect template schema')
            for key in ('reference', 'preview'):
                local_resource(file.parent, data.get(key, ''), checked_root, relative)
        elif file.name == 'reference-source.json':
            for target in data.get('visual_resources', []):
                local_resource(file.parent, target, checked_root, relative)
            template = data.get('editable_template')
            if template:
                local_resource(file.parent, template['path'], checked_root, relative)
                resource = (file.parent / template['path']).resolve()
                if resource.is_file() and digest(resource) != template['sha256']:
                    fail(f'{relative}: template hash mismatch')
            if data.get('generic_talk'):
                local_resource(file.parent, data['generic_talk'], checked_root, relative)
        elif file.name == 'asset-manifest.json':
            listed = set()
            for asset in data.get('assets', []):
                local_resource(file.parent, asset['path'], checked_root, relative)
                resource = (file.parent / asset['path']).resolve()
                listed.add(resource)
                if resource.is_file() and digest(resource) != asset['sha256']:
                    fail(f'{asset["path"]}: SHA256 mismatch')
            actual = {p.resolve() for p in files if p.suffix in {'.png', '.pptx'}}
            if listed != actual:
                fail('asset manifest does not cover exactly the delivered binary assets')
    if file.suffix == '.pptx':
        check_ppt(file)
for skill_file in [p for p in files if p.name == 'SKILL.md']:
    check_skill(skill_file.parent)
if not counts['skills']:
    fail('no skill entry found')
result = {'status': 'fail' if errors else 'pass', 'checks': counts,
          'errors': errors,
          'boundary': 'File and structure checks only; not copyright, research, oral rehearsal, native rendering or installation.'}
print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(1 if errors else 0)
