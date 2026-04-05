#!/usr/bin/env python3
"""Generate a PDF from the AirTAC International qanalysis markdown report."""

import re
from fpdf import FPDF

INPUT = "Airtac International-qanalysis.md"
OUTPUT = "docs/pdfs/Airtac International-qanalysis.pdf"


class MarkdownPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=20)
        self.add_page()
        self.set_margins(20, 20, 20)

    def title_page(self, title, subtitle_lines):
        self.set_y(60)
        self.set_font("Helvetica", "B", 28)
        self.multi_cell(0, 14, title, align="C")
        self.ln(10)
        self.set_font("Helvetica", "", 12)
        self.set_text_color(100, 100, 100)
        for line in subtitle_lines:
            self.cell(0, 8, line, align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(10)
        self.set_draw_color(180, 180, 180)
        self.line(40, self.get_y(), self.w - 40, self.get_y())
        self.ln(10)

    def h2(self, text):
        self.ln(6)
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(30, 60, 120)
        self.multi_cell(0, 10, text)
        self.set_text_color(0, 0, 0)
        self.ln(2)

    def h3(self, text):
        self.ln(4)
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(50, 80, 140)
        self.multi_cell(0, 9, text)
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
        text = text.replace("\u2014", " - ")
        text = text.replace("\u2013", "-")
        text = text.replace("\u2018", "'").replace("\u2019", "'")
        text = text.replace("\u201c", '"').replace("\u201d", '"')
        text = text.replace("\u2026", "...")
        text = text.replace("\u2022", "-")
        text = text.replace("\u00d7", "x")
        text = text.replace("\u2190", "<-").replace("\u2192", "->")
        text = text.replace("\u251c", "|").replace("\u2514", "`")
        text = text.replace("\u2500", "-").replace("\u2502", "|")
        return text

    def table_row(self, cells, bold=False):
        style = "B" if bold else ""
        self.set_font("Helvetica", style, 9)
        col_widths = [8, 55, 20, 87]
        h = 7

        for idx, cell_text in enumerate(cells):
            w = col_widths[idx] if idx < len(col_widths) else 40
            t = self._sanitize(cell_text)
            if bold:
                self.set_fill_color(230, 235, 245)
                self.cell(w, h, t[:int(w/2.5)], border=1, fill=True)
            else:
                self.set_fill_color(255, 255, 255)
                self.set_font("Helvetica", "B" if idx == 2 else "", 9)
                self.cell(w, h, t[:int(w/2.2)], border="LBR")
            self.set_font("Helvetica", "", 9)
        self.ln(h)

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
            self.cell(0, 10, "AirTAC International Group - Quartr-Enhanced Analysis", align="C")
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

    pdf.title_page(
        "AirTAC International Group",
        [
            "Quartr-Enhanced Investment Analysis",
            "",
            "Ticker: 1590.TW | Market Cap: TWD 198B (~USD 6.2B)",
            "Date: 5 April 2026",
            "Tool: Claude Code (Claude Opus 4.6)",
        ],
    )

    in_code_block = False
    code_buffer = []
    in_table = False
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()
        if line.startswith("## "):
            break
        i += 1

    while i < len(lines):
        line = lines[i].rstrip()
        i += 1

        if line.startswith("```"):
            if in_code_block:
                pdf.code_block("\n".join(code_buffer)) if hasattr(pdf, 'code_block') else None
                code_buffer = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_buffer.append(line)
            continue

        if not line.strip():
            in_table = False
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

        if line.startswith("|"):
            cells = [c.strip() for c in line.split("|")[1:-1]]
            if len(cells) >= 2:
                if "---" in cells[0] or "---" in cells[1]:
                    continue
                if not in_table:
                    pdf.table_row(cells, bold=True)
                    in_table = True
                else:
                    pdf.table_row(cells)
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
    parse_and_render(INPUT, OUTPUT)
