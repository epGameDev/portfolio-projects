from pypdf import PdfWriter

pdf_merger = PdfWriter()

for pdf_file in ["twopage.pdf", "wtr.pdf", "dummy.pdf"]:
    pdf_merger.append(pdf_file)

pdf_merger.write("large-PDF.pdf")
pdf_merger.close()