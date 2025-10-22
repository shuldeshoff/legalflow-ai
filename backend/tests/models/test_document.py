import pytest
from app.models.document import Document


def test_create_document(db, test_user):
    """Test document model creation"""
    document = Document(
        title="Test Document",
        file_path="/tmp/test.pdf",
        file_type="pdf",
        file_size=1024,
        uploaded_by=test_user.id,
        extracted_text="Test content",
        analysis_status="pending"
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    assert document.id is not None
    assert document.title == "Test Document"
    assert document.file_type == "pdf"
    assert document.analysis_status == "pending"
    assert document.uploaded_at is not None


def test_document_with_analysis(db, test_user):
    """Test document with analysis results"""
    document = Document(
        title="Analyzed Document",
        file_path="/tmp/analyzed.pdf",
        file_type="pdf",
        uploaded_by=test_user.id,
        extracted_text="Legal document content",
        analysis_status="completed",
        analysis_summary="Summary of the document",
        key_points=["Point 1", "Point 2"],
        risks=[
            {
                "type": "Legal risk",
                "description": "Missing clause",
                "severity": "high",
                "recommendation": "Add the clause"
            }
        ],
        recommendations="Overall recommendations"
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    assert document.analysis_status == "completed"
    assert document.analysis_summary is not None
    assert len(document.key_points) == 2
    assert len(document.risks) == 1
    assert document.risks[0]["severity"] == "high"

