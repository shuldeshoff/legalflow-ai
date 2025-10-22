import pytest
from app.models.document import Document


def test_create_document(db, test_user):
    """Test document model creation"""
    document = Document(
        original_name="Test Document.pdf",
        file_path="/tmp/test.pdf",
        type="other",
        mime_type="application/pdf",
        size=1024,
        uploaded_by=test_user.id
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    assert document.id is not None
    assert document.original_name == "Test Document.pdf"
    assert document.mime_type == "application/pdf"
    assert document.created_at is not None


def test_document_types(db, test_user):
    """Test document type enum"""
    # Test different document types
    doc_types = ["contract", "claim", "complaint", "other"]
    
    for doc_type in doc_types:
        document = Document(
            original_name=f"test_{doc_type}.pdf",
            file_path=f"/tmp/test_{doc_type}.pdf",
            type=doc_type,
            mime_type="application/pdf",
            size=1024,
            uploaded_by=test_user.id
        )
        
        db.add(document)
        db.commit()
        db.refresh(document)
        
        assert document.type == doc_type
        
    # Test that we created all documents
    all_docs = db.query(Document).filter(Document.uploaded_by == test_user.id).all()
    assert len(all_docs) >= 4
