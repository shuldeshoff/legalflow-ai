import pytest
from app.services.document_processor import DocumentProcessor


def test_get_file_type():
    """Test file type detection"""
    processor = DocumentProcessor()
    
    assert processor.get_file_type("test.pdf") == "pdf"
    assert processor.get_file_type("test.docx") == "docx"
    assert processor.get_file_type("test.txt") == "txt"
    
    with pytest.raises(ValueError):
        processor.get_file_type("test.exe")


def test_extract_text_from_txt():
    """Test text extraction from TXT file"""
    processor = DocumentProcessor()
    
    # Create a temporary test file
    import tempfile
    import os
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test content")
        temp_path = f.name
    
    try:
        extracted = processor.extract_text(temp_path, "txt")
        assert extracted == "Test content"
    finally:
        os.unlink(temp_path)
