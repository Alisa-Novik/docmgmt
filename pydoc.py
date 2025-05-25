#!/usr/bin/env python3
import os, sys, glob
from docx import Document

src_dir = sys.argv[1]
out_dir = "knowledge_base"
os.makedirs(out_dir, exist_ok=True)
for src in glob.glob(f"{src_dir}/*.docx"):
    name = os.path.splitext(os.path.basename(src))[0]
    dst = os.path.join(out_dir, name + ".txt")
    doc = Document(src)
    with open(dst, "w", encoding="utf-8") as f:
        for p in doc.paragraphs:
            t = p.text.strip()
            if t:
                f.write(t + "\n")
