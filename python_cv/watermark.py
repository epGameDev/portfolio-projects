from pathlib import Path
from pypdf import PdfReader, PdfWriter

try:
    # Collecting resources
    pdf = Path(input("Which PDF do you want to watermark?  ").strip() )
    watermark = Path(input("Which watermark do you want to use?  ").strip() )

    if not pdf.is_file():
        raise FileNotFoundError(f"PDF not found: {pdf}")
    if not watermark.is_file():
        raise FileNotFoundError(f"Watermark not found: {watermark}")

    # Managing resources
    stamp = PdfReader(str(watermark)).pages[0]
    writer = PdfWriter(clone_from=str(pdf))
    
    # Stamping | Watermarking
    for page in writer.pages:
        page.merge_page(stamp, over=False)

    # Writing to File
    writer.write("tagged.pdf")

except FileNotFoundError:
    print("A file was not provided or doesn't exist.")