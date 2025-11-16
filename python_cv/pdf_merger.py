from pypdf import PdfWriter
import sys

pdf_merger = PdfWriter()

files = sys.argv[1:]

try:
    if not files:
        raise FileExistsError
    for pdf_file in files:
        pdf_merger.append(pdf_file)

    pdf_merger.write("combined-PDF.pdf")
    pdf_merger.close()

except FileExistsError:
    print("No files were provided for this merge")