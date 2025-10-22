import os
import hashlib
from typing import Optional, BinaryIO
from pathlib import Path
import logging

# Document parsers
import PyPDF2
from docx import Document as DocxDocument

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Service for processing uploaded documents"""
    
    def __init__(self, upload_dir: str = "./uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
    
    async def save_file(self, file: BinaryIO, filename: str) -> tuple[str, int]:
        """
        Save uploaded file to disk
        
        Returns:
            tuple: (file_path, file_size)
        """
        try:
            # Generate unique filename
            file_hash = hashlib.md5(filename.encode()).hexdigest()[:8]
            safe_filename = f"{file_hash}_{filename}"
            file_path = self.upload_dir / safe_filename
            
            # Save file
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)
            
            file_size = len(content)
            
            logger.info(f"File saved: {file_path} ({file_size} bytes)")
            return str(file_path), file_size
            
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise
    
    def extract_text(self, file_path: str, file_type: str) -> str:
        """
        Extract text from document
        
        Args:
            file_path: Path to document file
            file_type: Type of document (pdf, docx, txt)
        
        Returns:
            Extracted text content
        """
        try:
            if file_type == "pdf":
                return self._extract_from_pdf(file_path)
            elif file_type == "docx":
                return self._extract_from_docx(file_path)
            elif file_type == "txt":
                return self._extract_from_txt(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            raise
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text_parts = []
        
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text = page.extract_text()
                    if text.strip():
                        text_parts.append(text)
                except Exception as e:
                    logger.warning(f"Error extracting page {page_num}: {e}")
        
        return "\n\n".join(text_parts)
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = DocxDocument(file_path)
        text_parts = []
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if text:
                text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    
    def get_file_type(self, filename: str) -> str:
        """Get file type from filename"""
        ext = Path(filename).suffix.lower()
        
        if ext == ".pdf":
            return "pdf"
        elif ext in [".docx", ".doc"]:
            return "docx"
        elif ext == ".txt":
            return "txt"
        else:
            raise ValueError(f"Unsupported file extension: {ext}")
    
    def delete_file(self, file_path: str):
        """Delete file from disk"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted: {file_path}")
        except Exception as e:
            logger.error(f"Error deleting file {file_path}: {e}")


# Global instance
document_processor = DocumentProcessor()

