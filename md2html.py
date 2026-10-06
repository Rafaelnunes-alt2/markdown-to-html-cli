# feito por: maquinzz
import argparse, html, re, sys

def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`\n]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*\n]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*\n]+)\*", r"<em>\1</em>", s)
    s = re.sub(r"__([^_\n]+)__", r"<strong>\1</strong>", s)
    s = re.sub(r"_([^_\n]+)_", r"<em>\1</em>", s)
    return s

def convert(text: str) -> str:
    lines = text.splitlines()
    out = []
    in_code = False
    in_ul = False
    in_p = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_p:
                out.append("</p>"); in_p = False
            if in_ul:
                out.append("</ul>"); in_ul = False
            if in_code:
                out.append("</code></pre>"); in_code = False
            else:
                out.append("<pre><code>"); in_code = True
            continue
        if in_code:
            out.append(html.escape(line, quote=False))
            continue
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            if in_p: out.append("</p>"); in_p = False
            if in_ul: out.append("</ul>"); in_ul = False
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2).strip())}</h{level}>")
            continue
        if re.match(r"^[-*+]\s+", stripped):
            if in_p: out.append("</p>"); in_p = False
            if not in_ul:
                out.append("<ul>"); in_ul = True
            item = re.sub(r"^[-*+]\s+", "", stripped)
            out.append(f"<li>{inline(item)}</li>")
            continue
        if stripped == "":
            if in_p: out.append("</p>"); in_p = False
            if in_ul: out.append("</ul>"); in_ul = False
            continue
        if in_ul:
            out.append("</ul>"); in_ul = False
        if in_p:
            out.append(f" {inline(stripped)}")
        else:
            out.append(f"<p>{inline(stripped)}")
            in_p = True
    if in_p: out.append("</p>")
    if in_ul: out.append("</ul>")
    if in_code: out.append("</code></pre>")
    css = "<style>body{font-family:system-ui,sans-serif;max-width:720px;margin:2rem auto;line-height:1.5;padding:0 1rem}pre{background:#f4f4f4;padding:1rem;overflow:auto}code{background:#f4f4f4;padding:.1rem .3rem}</style>"
    return "<!doctype html><html><head><meta charset=\"utf-8\">" + css + "</head><body>\n" + "\n".join(out) + "\n</body></html>\n"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--in", dest="inp", help="input md")
    p.add_argument("--out", dest="out", help="output html")
    a = p.parse_args()
    try:
        text = open(a.inp, encoding="utf-8").read() if a.inp else sys.stdin.read()
    except OSError as e:
        print(f"open_failed: {e}", file=sys.stderr); sys.exit(2)
    if len(text) > 16 * 1024 * 1024:
        print("too_big", file=sys.stderr); sys.exit(2)
    html_out = convert(text)
    if a.out:
        try:
            with open(a.out, "w", encoding="utf-8") as f: f.write(html_out)
        except OSError as e:
            print(f"write_failed: {e}", file=sys.stderr); sys.exit(2)
    else:
        sys.stdout.write(html_out)

if __name__ == "__main__":
    main()
