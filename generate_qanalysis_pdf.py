#!/usr/bin/env python3
"""Generate a PDF from a Qanalysis markdown report."""

import re
import sys
from fpdf import FPDF


class MarkdownPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()
        self.set_margins(20, 20, 20)
        self._doc_title = ""

    def title_page(self, title, subtitle_lines):
        self._doc_title = title
        self.set_y(60)
        self.set_font("Helvetica", "B", 26)
        self.multi_cell(0, 13, self._sanitize(title), align="C")
        self.ln(8)
        self.set_font("Helvetica", "", 11)
        self.set_text_color(100, 100, 100)
        for line in subtitle_lines:
            self.cell(0, 7, self._sanitize(line), align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(10)
        self.set_draw_color(180, 180, 180)
        self.line(40, self.get_y(), self.w - 40, self.get_y())
        self.ln(10)

    def h2(self, text):
        self.ln(6)
        self.set_font("Helvetica", "B", 17)
        self.set_text_color(30, 60, 120)
        self.multi_cell(0, 10, self._sanitize(text))
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def h3(self, text):
        self.ln(4)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(50, 80, 140)
        self.multi_cell(0, 9, self._sanitize(text))
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def body_text(self, text):
        self.set_font("Helvetica", "", 10.5)
        self._write_rich_text(text)
        self.ln(4)

    def bullet(self, text, indent=0):
        x = self.get_x() + indent
        self.set_x(x)
        self.set_font("Helvetica", "", 10.5)
        bullet_w = 5
        self.cell(bullet_w, 6, "-")
        self._write_rich_text(text, w=self.w - self.r_margin - x - bullet_w)
        self.ln(3)

    def numbered_item(self, num, text, indent=0):
        x = self.get_x() + indent
        self.set_x(x)
        self.set_font("Helvetica", "B", 10.5)
        num_w = 8
        self.cell(num_w, 6, f"{num}.")
        self.set_font("Helvetica", "", 10.5)
        self._write_rich_text(text, w=self.w - self.r_margin - x - num_w)
        self.ln(3)

    @staticmethod
    def _sanitize(text):
        replacements = {
            "\u2014": " - ", "\u2013": "-",
            "\u2018": "'", "\u2019": "'",
            "\u201c": '"', "\u201d": '"',
            "\u2026": "...", "\u2022": "-",
            "\u00d7": "x", "\u2190": "<-", "\u2192": "->",
            "\u251c": "|", "\u2514": "`",
            "\u2500": "-", "\u2502": "|",
            "\u2248": "~", "\u2265": ">=", "\u2264": "<=",
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        text = text.encode('latin-1', errors='replace').decode('latin-1')
        return text

    def _write_rich_text(self, text, w=None):
        if w is None:
            w = self.w - self.l_margin - self.r_margin
        text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
        text = re.sub(r'`([^`]+)`', r'\1', text)
        text = self._sanitize(text)
        parts = re.split(r'(\*\*[^*]+\*\*)', text)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                self.set_font("Helvetica", "B", 10.5)
                self.write(6, part[2:-2])
                self.set_font("Helvetica", "", 10.5)
            else:
                self.write(6, part)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, self._sanitize(self._doc_title), align="C")
            self.set_text_color(0, 0, 0)
            self.ln(12)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")
        self.set_text_color(0, 0, 0)


def parse_and_render(md_path, output_path):
    with open(md_path, "r") as f:
        lines = f.readlines()

    pdf = MarkdownPDF()

    title = "Investment Analysis"
    subtitle_lines = []
    for line in lines[:10]:
        line = line.rstrip()
        if line.startswith("# "):
            title = line[2:].strip()
        elif line.startswith("**Date:"):
            subtitle_lines.append(line.replace("**", "").strip())
        elif line.startswith("**Market Cap:"):
            subtitle_lines.append(line.replace("**", "").strip())
        elif line.startswith("**GICS:"):
            subtitle_lines.append(line.replace("**", "").strip())

    if not subtitle_lines:
        subtitle_lines = ["Quartr-Enhanced Investment Analysis"]

    pdf.title_page(title, subtitle_lines)

    in_code_block = False
    code_buffer = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()
        if line.startswith("## "):
            break
        if line.startswith("---"):
            i += 1
            continue
        i += 1

    while i < len(lines):
        line = lines[i].rstrip()
        i += 1

        if line.startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        if not line.strip():
            continue

        if line.strip() == "---":
            pdf.ln(3)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(20, pdf.get_y(), pdf.w - 20, pdf.get_y())
            pdf.ln(3)
            continue

        if line.startswith("## "):
            pdf.h2(line[3:].strip())
            continue
        if line.startswith("### "):
            pdf.h3(line[4:].strip())
            continue

        m = re.match(r'^(\d+)\.\s+(.*)', line)
        if m:
            pdf.numbered_item(m.group(1), m.group(2))
            continue

        if line.startswith("- "):
            pdf.bullet(line[2:])
            continue

        pdf.body_text(line)

    pdf.output(output_path)
    print(f"PDF saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python generate_qanalysis_pdf.py <input.md> <output.pdf>")
        sys.exit(1)
    parse_and_render(sys.argv[1], sys.argv[2])
