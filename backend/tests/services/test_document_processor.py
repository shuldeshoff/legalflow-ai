import pytest
from app.services.document_processor import DocumentProcessor
from io import BytesIO


def test_get_file_type():
    """Test file type detection"""
    processor = DocumentProcessor()
    
    assert processor.get_file_type("test.pdf") == "pdf"
    assert processor.get_file_type("test.docx") == "docx"
    assert processor.get_file_type("test.txt") == "txt"
    
    with pytest.raises(ValueError):
        processor.get_file_type("test.exe")


@pytest.mark.asyncio
async def test_save_file():
    """Test file saving"""
    processor = DocumentProcessor(upload_dir="./test_uploads")
    
    test_content = b"Test file content"
    test_file = BytesIO(test_content)
    
    file_path, file_size = await processor.save_file(test_file, "test.txt")
    
    assert file_path is not None
    assert file_size == len(test_content)
    
    # Cleanup
    import os
    if os.path.exists(file_path):
        os.remove(file_path)
    if os.path.exists("./test_uploads"):
        os.rmdir("./test_uploads")


def test_extract_text_from_txt():
    """Test text extraction from TXT file"""
    processor = DocumentProcessor()
    
    # Create a temporary test file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test content")
        temp_path = f.name
    
    try:
        extracted = processor.extract_text(temp_path, "txt")
        assert extracted == "Test content"
    finally:
        import os
        os.unlink(temp_path)

