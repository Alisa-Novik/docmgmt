from pathlib import Path
import subprocess
import zipfile

# Helper to create a simple PDF with plain text using minimal syntax

def create_pdf(path: Path, text: str) -> None:
    header = b"%PDF-1.4\n"
    objects = [
        "1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        "2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        (
            "3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] "
            "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n"
        ),
        "4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
    ]
    stream = f"BT\n/F1 24 Tf\n100 100 Td\n({text}) Tj\nET"
    objects.append(
        f"5 0 obj\n<< /Length {len(stream)} >>\nstream\n{stream}\nendstream\nendobj\n"
    )

    offsets = [len(header)]
    for o in objects[:-1]:
        offsets.append(offsets[-1] + len(o.encode()))

    pdf = bytearray(header)
    for o in objects:
        pdf += o.encode()

    xref_start = len(pdf)
    xref_lines = ["xref", f"0 {len(objects)+1}", "0000000000 65535 f \n"]
    for off in [0] + offsets:
        xref_lines.append(f"{off:010d} 00000 n \n")

    trailer = (
        f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n"
    )

    pdf += "\n".join(xref_lines).encode() + b"\n" + trailer.encode()

    with open(path, "wb") as f:
        f.write(pdf)


def create_docx(path: Path, text: str) -> None:
    doc_xml = (
        "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
        "<w:document xmlns:w='http://schemas.openxmlformats.org/wordprocessingml/2006/main'>"
        "<w:body><w:p><w:r><w:t>" + text + "</w:t></w:r></w:p></w:body></w:document>"
    )
    ctypes = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        "<Types xmlns='http://schemas.openxmlformats.org/package/2006/content-types'>"
        "<Default Extension='rels' ContentType='application/vnd.openxmlformats-package.relationships+xml'/>"
        "<Default Extension='xml' ContentType='application/xml'/>"
        "<Override PartName='/word/document.xml' ContentType='application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml'/>"
        "</Types>"
    )
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("[Content_Types].xml", ctypes)
        z.writestr("word/document.xml", doc_xml)


def test_pydoc_extracts_docx_and_pdf(tmp_path: Path):
    src = tmp_path / "src"
    src.mkdir()
    out = tmp_path / "knowledge_base"

    docx_file = src / "sample_doc.docx"
    create_docx(docx_file, "Docx text")

    pdf_file = src / "sample_pdf.pdf"
    create_pdf(pdf_file, "Pdf text")

    subprocess.check_call(["python", str(Path(__file__).resolve().parents[1] / "pydoc.py"), str(src)], cwd=tmp_path)

    with open(out / "sample_doc.txt", encoding="utf-8") as f:
        assert f.read().strip() == "Docx text"

    with open(out / "sample_pdf.txt", encoding="utf-8") as f:
        assert f.read().strip() == "Pdf text"
