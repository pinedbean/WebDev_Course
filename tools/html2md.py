#!/usr/bin/env python3
"""Convert the course's consistent lesson HTML files into clean GitHub-Markdown.

Designed specifically for this repo's lecture/assignment/solution template:
- strips <head>/<style>
- banner  -> title + context + badges + a link back to the .html version
- sections/headings/paragraphs/lists/tables -> markdown
- <pre><code> -> fenced code block with unescaped content + a language guess
- .callout -> blockquote with its label
- .flow/.anatomy/.filetree/.layout -> code/diagram blocks
- footer .nav -> markdown links rewritten from *.html to *.md
"""
import os, re, sys, textwrap
from html.parser import HTMLParser

VOID = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
SKIP = {'style','script','title'}

class Node:
    __slots__ = ('tag','attrs','children')
    def __init__(self, tag, attrs=None):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.children = []

class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('#root')
        self.stack = [self.root]
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.skip += 1; return
        if self.skip: return
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)
    def handle_startendtag(self, tag, attrs):
        if self.skip: return
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
    def handle_endtag(self, tag):
        if tag in SKIP:
            if self.skip: self.skip -= 1
            return
        if self.skip: return
        if tag in VOID: return
        # pop to nearest matching ancestor
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break
    def handle_data(self, data):
        if self.skip: return
        self.stack[-1].children.append(data)

def cls(node):
    return set(node.attrs.get('class','').split()) if isinstance(node, Node) else set()

def find_first(node, tag=None, klass=None):
    for c in node.children:
        if isinstance(c, Node):
            if (tag is None or c.tag == tag) and (klass is None or klass in cls(c)):
                return c
    return None

def text_content(node):
    """Raw text of all descendants, preserving whitespace (for code blocks)."""
    if isinstance(node, str):
        return node
    return ''.join(text_content(c) for c in node.children)

def collapse(s):
    return re.sub(r'\s+', ' ', s)

def rewrite_href(href):
    if not href:
        return href
    if href.startswith(('http://','https://','mailto:','#')):
        return href
    # rewrite sibling/relative .html links to .md
    if href.endswith('.html'):
        return href[:-5] + '.md'
    return href

# ---------- inline ----------
def render_inline(node):
    if isinstance(node, str):
        return collapse(node)
    t = node.tag
    inner = ''.join(render_inline(c) for c in node.children)
    if t in ('strong','b'):
        return '**' + inner.strip() + '**'
    if t in ('em','i'):
        return '*' + inner.strip() + '*'
    if t in ('code','kbd','samp','tt'):
        return '`' + text_content(node).strip() + '`'
    if t == 'a':
        href = rewrite_href(node.attrs.get('href'))
        txt = inner.strip() or href or ''
        if href:
            return f'[{txt}]({href})'
        return txt
    if t == 'br':
        return '  \n'
    if t == 'img':
        return f'![{node.attrs.get("alt","")}]({node.attrs.get("src","")})'
    if t in ('sup','sub','small','span','time','u'):
        return inner
    return inner

def render_inline_seq(children):
    return ''.join(render_inline(c) for c in children)

# ---------- code language guess ----------
def detect_lang(code):
    c = code
    low = c.lower()
    if re.search(r'^\s*(FROM|RUN|CMD|COPY|WORKDIR|ENTRYPOINT|EXPOSE)\b', c, re.M) and 'FROM ' in c:
        return 'dockerfile'
    if re.search(r'\b(def |import |from \w+ import|FastAPI|@app\.|@router\.|Depends\()', c):
        return 'python'
    if re.search(r'\b(SELECT|INSERT INTO|CREATE TABLE|UPDATE |DELETE FROM|ALTER TABLE)\b', c):
        return 'sql'
    if re.search(r'</[a-zA-Z]', c) or re.search(r'<[A-Z][A-Za-z]+', c):
        # has closing tags or capitalized component -> markup/jsx
        if 'return (' in c or '=>' in c or 'const ' in c or 'useState' in c or 'className' in c:
            return 'jsx'
        return 'html'
    if re.search(r'^\s*(version:|services:|steps:|jobs:|on:|name:)\s', c, re.M):
        return 'yaml'
    if re.search(r'\b(const |let |function |=>|useState|import .* from)\b', c):
        return 'javascript'
    if re.search(r'^\s*[#$]?\s*(npm|npx|cd |git |uvicorn|pip3?|python3?|brew|docker|gcloud|alembic|node|ssh|mkdir|touch|curl|source|export)\b', c, re.M):
        return 'bash'
    if re.search(r'^\s*\{', c) and '":' in c:
        return 'json'
    return ''

def fenced(code, lang=''):
    code = code.strip('\n')
    fence = '```'
    if '```' in code:
        fence = '~~~'
    return f'{fence}{lang}\n{code}\n{fence}'

# ---------- table ----------
def render_table(node):
    rows = []
    def walk(n):
        for c in n.children:
            if isinstance(c, Node):
                if c.tag == 'tr':
                    cells = [render_inline_seq(cell.children).strip().replace('|','\\|').replace('\n',' ')
                             for cell in c.children if isinstance(cell, Node) and cell.tag in ('th','td')]
                    rows.append(cells)
                else:
                    walk(c)
    walk(node)
    rows = [r for r in rows if r]
    if not rows:
        return ''
    ncol = max(len(r) for r in rows)
    rows = [r + ['']*(ncol-len(r)) for r in rows]
    out = []
    out.append('| ' + ' | '.join(rows[0]) + ' |')
    out.append('| ' + ' | '.join(['---']*ncol) + ' |')
    for r in rows[1:]:
        out.append('| ' + ' | '.join(r) + ' |')
    return '\n'.join(out)

# ---------- blocks ----------
def render_callout(node):
    label = ''
    lab = find_first(node, klass='label')
    if lab:
        label = render_inline_seq(lab.children).strip()
    parts = []
    for c in node.children:
        if isinstance(c, Node) and 'label' in cls(c):
            continue
        parts.append(c)
    body = render_blocks(parts).strip()
    lines = []
    if label:
        lines.append('> **' + label + '**')
        lines.append('>')
    for bl in body.split('\n'):
        lines.append('> ' + bl if bl else '>')
    return '\n'.join(lines)

def render_flow(node):
    bits = []
    for c in node.children:
        if isinstance(c, Node):
            txt = collapse(text_content(c)).strip()
            if txt:
                bits.append(txt)
    return '> ' + '  →  '.join(bits)

def render_list(node, depth=0):
    ordered = node.tag == 'ol'
    lines = []
    idx = 1
    for li in node.children:
        if not (isinstance(li, Node) and li.tag == 'li'):
            continue
        inline_parts, sublists = [], []
        for c in li.children:
            if isinstance(c, Node) and c.tag in ('ul','ol'):
                sublists.append(c)
            else:
                inline_parts.append(c)
        marker = (f'{idx}. ' if ordered else '- ')
        text = render_inline_seq(inline_parts).strip()
        lines.append('  '*depth + marker + text)
        for sub in sublists:
            lines.append(render_list(sub, depth+1))
        idx += 1
    return '\n'.join(lines)

def render_block(node):
    if isinstance(node, str):
        s = collapse(node).strip()
        return s
    t = node.tag
    c = cls(node)
    if t in ('h1','h2','h3','h4','h5','h6'):
        level = int(t[1])
        # demote: h1 reserved for the page title -> h2 minimum inside body
        level = max(level, 2)
        return '#'*level + ' ' + render_inline_seq(node.children).strip()
    if t == 'p':
        return render_inline_seq(node.children).strip()
    if t in ('ul','ol'):
        return render_list(node)
    if t == 'pre':
        code = text_content(node)
        return fenced(code, detect_lang(code))
    if t == 'table':
        return render_table(node)
    if t == 'hr':
        return '---'
    if t == 'img':
        return f'![{node.attrs.get("alt","")}]({node.attrs.get("src","")})'
    if t == 'blockquote':
        body = render_blocks(node.children).strip()
        return '\n'.join('> ' + l if l else '>' for l in body.split('\n'))
    if t == 'div':
        if 'callout' in c:
            return render_callout(node)
        if 'flow' in c:
            return render_flow(node)
        if 'demo' in c:
            return '*(Interactive demo — open the `.html` version in a browser to try it live.)*'
        if c & {'anatomy','filetree','layout'}:
            txt = text_content(node)
            # strip trailing space per line, dedent common leading indentation
            # (preserves relative indentation for tree/layout diagrams), drop blank edges
            txt = re.sub(r'[ \t]+\n', '\n', txt)
            txt = textwrap.dedent(txt).strip('\n')
            return fenced(txt, 'text')
        # generic wrapper
        return render_blocks(node.children)
    if t in ('section','main','article','header','footer','span'):
        return render_blocks(node.children)
    # fallback
    return render_blocks(node.children)

def render_blocks(children):
    out = []
    for c in children:
        if isinstance(c, str):
            s = collapse(c).strip()
            if s:
                out.append(s)
            continue
        block = render_block(c)
        if block and block.strip():
            out.append(block.rstrip())
    return '\n\n'.join(out)

# ---------- top-level page ----------
def find_descendant(node, tag=None, klass=None):
    for c in node.children:
        if isinstance(c, Node):
            if (tag is None or c.tag == tag) and (klass is None or klass in cls(c)):
                return c
            r = find_descendant(c, tag, klass)
            if r:
                return r
    return None

def convert(html, html_filename):
    tb = TreeBuilder()
    tb.feed(html)
    body = find_descendant(tb.root, tag='body') or tb.root
    parts = []

    banner = find_descendant(body, klass='banner')
    if banner:
        crumbs = find_descendant(banner, klass='crumbs')
        h1 = find_descendant(banner, tag='h1')
        badges = []
        def collect_badges(n):
            for ch in n.children:
                if isinstance(ch, Node):
                    if 'badge' in cls(ch):
                        badges.append(collapse(text_content(ch)).strip())
                    collect_badges(ch)
        collect_badges(banner)
        if crumbs:
            parts.append('*' + collapse(text_content(crumbs)).strip() + '*')
        if h1:
            parts.append('# ' + collapse(text_content(h1)).strip())
        if badges:
            parts.append(' · '.join('**'+b+'**' for b in badges))

    parts.append(f'> 📄 **Prefer the styled version?** Open [`{html_filename}`]({html_filename}) '
                 f'in your browser for the formatted page with colors and live demos.')
    parts.append('---')

    main = find_descendant(body, tag='main')
    if main:
        for sec in main.children:
            if isinstance(sec, Node) and sec.tag == 'section':
                block = render_blocks(sec.children).strip()
                if block:
                    parts.append(block)
            elif isinstance(sec, Node):
                block = render_block(sec).strip()
                if block:
                    parts.append(block)

    footer = find_descendant(body, tag='footer')
    if footer:
        nav = find_descendant(footer, klass='nav')
        if nav:
            links = []
            for a in nav.children:
                if isinstance(a, Node) and a.tag == 'a':
                    label = collapse(text_content(a)).strip()
                    label = label.replace('→','').replace('←','').strip()
                    href = rewrite_href(a.attrs.get('href'))
                    if href:
                        links.append(f'[{label}]({href})')
                    else:
                        links.append(f'**{label}**')
            if links:
                parts.append('---')
                parts.append('**Navigate:** ' + ' · '.join(links))

    md = '\n\n'.join(p for p in parts if p and p.strip())
    md = re.sub(r'\n{3,}', '\n\n', md).strip() + '\n'
    return md

def main():
    root = sys.argv[1]
    count = 0
    for dirpath, _, files in os.walk(root):
        if '/.git' in dirpath:
            continue
        for f in sorted(files):
            if not f.endswith('.html'):
                continue
            src = os.path.join(dirpath, f)
            with open(src, encoding='utf-8') as fh:
                html = fh.read()
            md = convert(html, f)
            dst = os.path.join(dirpath, f[:-5] + '.md')
            with open(dst, 'w', encoding='utf-8') as fh:
                fh.write(md)
            count += 1
    print(f'Converted {count} HTML files to Markdown.')

if __name__ == '__main__':
    main()
