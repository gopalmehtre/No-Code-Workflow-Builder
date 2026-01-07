from pypdf import PdfReader
import os
from typing import Dict

def extract_text_from_pdf(file_path: str) -> Dict[str, any]:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found : {file_path}")

        reader = PdfReader(file_path)
        num_pages= len(reader.pages)

        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"

        preview = full_text[:500] if len(full_text) > 500 else full_text

        return {
            "success" : True,
            "text" : full_text,
            "num_pages" : num_pages,
            "preview" : preview,
            "char_count" : len(full_text)
        }

    except Exception as e:
        return {
            "success" : False,
            "error" : str(e),
            "text" : "",
            "num_pages" : 0,
            "preview" : "",
            "char_count" : 0
        }
