#!/usr/bin/env python3
import os
import sys
import glob
import re
import zipfile
import xml.etree.ElementTree as ET


def extract_docx(path: str) -> str:
    with zipfile.ZipFile(path) as z:
        xml_data = z.read("word/document.xml")
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    root = ET.fromstring(xml_data)
    texts = [t.text for t in root.findall(".//w:t", ns) if t.text]
    lines = [t.strip() for t in texts if t.strip()]
    return "\n".join(lines)


def extract_pdf(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read().decode("latin1")
    lines = []
    for match in re.finditer(r"stream\r?\n(.*?)\r?\nendstream", data, re.S):
        segment = match.group(1)
        for text in re.findall(r"\((.*?)\)", segment):
            cleaned = text.strip()
            if cleaned:
                lines.append(cleaned)
    return "\n".join(lines)

src_dir = sys.argv[1]
out_dir = "knowledge_base"
os.makedirs(out_dir, exist_ok=True)

for pattern in ("*.docx", "*.pdf"):
    for src in glob.glob(os.path.join(src_dir, pattern)):
        name = os.path.splitext(os.path.basename(src))[0]
        dst = os.path.join(out_dir, name + ".txt")
        if src.lower().endswith(".docx"):
            text = extract_docx(src)
        else:
            text = extract_pdf(src)
        with open(dst, "w", encoding="utf-8") as f:
            if text:
                f.write(text + "\n")
