import pytest
from unittest.mock import Mock, patch
from io import BytesIO
from fastapi import status


def test_upload_document(client, auth_headers):
    """Test document upload"""
    # Create a test file
    test_file = BytesIO(b"Test document content")
    test_file.name = "test.txt"
    
    response = client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files={"file": ("test.txt", test_file, "text/plain")}
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["title"] == "test.txt"
    assert data["file_type"] == "txt"


def test_upload_document_unauthorized(client):
    """Test document upload without auth"""
    test_file = BytesIO(b"Test content")
    test_file.name = "test.txt"
    
    response = client.post(
        "/api/v1/documents/upload",
        files={"file": ("test.txt", test_file, "text/plain")}
    )
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_upload_unsupported_file_type(client, auth_headers):
    """Test upload with unsupported file type"""
    test_file = BytesIO(b"Test content")
    test_file.name = "test.exe"
    
    response = client.post(
        "/api/v1/documents/upload",
        headers=auth_headers,
        files={"file": ("test.exe", test_file, "application/exe")}
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_analyze_document(client, auth_headers, test_user, db):
    """Test document analysis"""
    from app.models.document import Document
    
    # Create a test document
    doc = Document(
        title="test.txt",
        file_path="/tmp/test.txt",
        file_type="txt",
        uploaded_by=test_user.id,
        extracted_text="Test legal document content",
        analysis_status="pending"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    with patch('app.services.document_analyzer.document_analyzer.analyze_document') as mock_analyze:
        mock_analyze.return_value = {
            "summary": "Test summary",
            "key_points": ["Point 1", "Point 2"],
            "risks": [],
            "recommendations": "Test recommendations"
        }
        
        response = client.post(
            f"/api/v1/documents/{doc.id}/analyze",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["analysis_status"] == "completed"
        assert "analysis_summary" in data


def test_list_documents(client, auth_headers, test_user, db):
    """Test listing documents"""
    from app.models.document import Document
    
    # Create test documents
    for i in range(3):
        doc = Document(
            title=f"test_{i}.txt",
            file_path=f"/tmp/test_{i}.txt",
            file_type="txt",
            uploaded_by=test_user.id
        )
        db.add(doc)
    db.commit()
    
    response = client.get(
        "/api/v1/documents/",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_get_document(client, auth_headers, test_user, db):
    """Test getting single document"""
    from app.models.document import Document
    
    doc = Document(
        title="test.txt",
        file_path="/tmp/test.txt",
        file_type="txt",
        uploaded_by=test_user.id,
        analysis_status="completed",
        analysis_summary="Test summary"
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    response = client.get(
        f"/api/v1/documents/{doc.id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == doc.id
    assert data["title"] == "test.txt"


def test_delete_document(client, auth_headers, test_user, db):
    """Test document deletion"""
    from app.models.document import Document
    
    doc = Document(
        title="test.txt",
        file_path="/tmp/test.txt",
        file_type="txt",
        uploaded_by=test_user.id
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    doc_id = doc.id
    
    response = client.delete(
        f"/api/v1/documents/{doc_id}",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify deletion
    deleted_doc = db.query(Document).filter(Document.id == doc_id).first()
    assert deleted_doc is None

