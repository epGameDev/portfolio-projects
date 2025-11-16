from pypdf import PdfReader
import io

with open ("twopage.pdf", "rb") as file:
    output = file.read()
    reader = PdfReader(io.BytesIO(output)) # Wrap bytes in a BytesIO object for PdfReader
    
    num_pages = len(reader.pages)
    print(num_pages)

    first_page = reader.pages[0]
    text = first_page.extract_text()
    print(text)
    # print(reader)