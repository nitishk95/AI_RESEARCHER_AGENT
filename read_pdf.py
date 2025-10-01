from langchain.tools import tool
import requests
import io
import PyPDF2

@tool
def read_pdf(url: str) -> str:
    """Read text from a PDF file at the given URL and return the extracted text.

    Args:
        url (str): The URL of the PDF file.

    Returns:
        str: The extracted text from the PDF file .
    
    
    
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"Failed to download PDF: {e}"

    with io.BytesIO(response.content) as open_pdf:
        try:
            reader = PyPDF2.PdfReader(open_pdf)
            text = ""
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
            return text.strip()
        except Exception as e:
            return f"Error reading PDF: {e}"

# # Test
# pdf_url = "https://arxiv.org/pdf/2309.16759.pdf"
# text = read_pdf(pdf_url)
# # print(text)
