#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build generator.html from generator.template.html + generate.mjs.

The page must run from file:// with no bundler, so the engine is inlined. It is
injected from the single JS source rather than copy-pasted, so the page can never
drift from the module that snapshot_test.mjs verifies.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(HERE, "generate.mjs")
TPL = os.path.join(HERE, "generator.template.html")
OUT = os.path.join(ROOT, "generator.html")
MARKER = "/*__ENGINE__*/"


def main():
    with open(SRC, encoding="utf-8") as f:
        js = f.read()
    # ESM -> classic script: the module has no imports, only `export const`.
    js = re.sub(r"^export (const|function) ", r"\1 ", js, flags=re.M)
    if "import " in js.split("\n\n")[0]:
        raise SystemExit("generate.mjs must stay dependency-free")

    with open(TPL, encoding="utf-8") as f:
        html = f.read()
    if MARKER not in html:
        raise SystemExit("template marker missing")

    banner = "/* engine/generate.mjs v0.1.0 — inlined by engine/build_page.py, do not edit here */\n"
    out = html.replace(MARKER, banner + js)

    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print("written: %s  (%d KB)" % (OUT, len(out.encode("utf-8")) // 1024))


if __name__ == "__main__":
    main()
