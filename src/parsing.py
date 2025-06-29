from invoice2data import extract_data
from invoice2data.extract.loader import read_templates
from invoice2data.input import tesseract, pdftotext, ocrmypdf
from pytesseract import pytesseract
import os
from typing import Optional, Dict, Any

pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def parse_pdf(file_path: str, fallback_ocr: bool = True, template_folder: Optional[str] = None) -> Dict[str, Any]:
    """
    Parses a PDF file to extract data using invoice2data.

    Args:
        file_path (str): The path to the PDF file to be parsed.
        fallback_ocr (bool): Whether to fallback to OCR if pdftotext fails.
        template_folder (str, optional): Path to custom templates folder.

    Returns:
        dict: A dictionary containing the extracted data.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF file not found: {file_path}")
    
    # Load templates
    templates = read_templates(template_folder) if template_folder else read_templates()
    
    # Try pdftotext first (faster for text-based PDFs)
    try:
        data = extract_data(file_path, templates=templates, input_module=pdftotext)
        if data:
            return data
    except Exception as e:
        print(f"pdftotext failed: {e}")
    
    # Fallback to OCR if enabled and pdftotext failed
    if fallback_ocr:
        try:
            print("Falling back to OCR...")
            data = extract_data(file_path, templates=templates, input_module=tesseract)
            if data:
                return data
        except Exception as e:
            print(f"OCR failed: {e}")
    
    raise ValueError("No data extracted from the PDF file with any method.")


def parse_pdf_batch(file_paths: list[str], **kwargs) -> Dict[str, Dict[str, Any]]:
    """
    Parse multiple PDF files.
    
    Args:
        file_paths: List of PDF file paths
        **kwargs: Arguments passed to parse_pdf
        
    Returns:
        dict: Mapping of file paths to extracted data
    """
    results = {}
    for file_path in file_paths:
        try:
            results[file_path] = parse_pdf(file_path, **kwargs)
        except Exception as e:
            results[file_path] = {"error": str(e)}
    return results


if __name__ == "__main__":
    # Single file
    try:
        result = parse_pdf(r"data\pdf_files\delta.pdf",template_folder=r"data\templates", fallback_ocr=True)
        print("Extracted data:", result)
    except Exception as e:
        print(f"Error: {e}")
    
    # Batch processing example
    # files = ["pdf_files/invoice1.pdf", "pdf_files/invoice2.pdf"]
    # results = parse_pdf_batch(files)
    # for file, data in results.items():
    #     print(f"{file}: {data}")