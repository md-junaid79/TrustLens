import PyPDF2
import os

def parse_document(path):
    """Fast PDF parsing without OCR/layout detection"""
    
    if not os.path.exists(path):
        print(f"[-] File not found: {path}")
        return []
    
    try:
        # Use lightweight PyPDF2 for text extraction
        blocks = []
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text() + "\n"
        
        # Split by double newlines (paragraphs)
        paragraphs = text.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if len(para) > 10:  # Filter short lines
                blocks.append({
                    "text": para,
                    "type": "NarrativeText"
                })
        
        print(f"[OK] Parsed {len(blocks)} blocks from {path}")
        return blocks
        
    except Exception as e:
        print(f"[-] Parse error for {path}: {str(e)}")
        return []
