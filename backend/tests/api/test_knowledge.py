import pytest
from unittest.mock import Mock, patch
from fastapi import status


def test_create_knowledge(client, auth_headers):
    """Test creating knowledge base entry"""
    response = client.post(
        "/api/v1/knowledge/",
        headers=auth_headers,
        json={
            "title": "Test Knowledge",
            "content": "Test content about law",
            "category": "civil_law",
            "source": "Test Source"
        }
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Test Knowledge"
    assert "embedding_id" in data


def test_list_knowledge(client, auth_headers, test_user, db):
    """Test listing knowledge base entries"""
    from app.models.knowledge_base import KnowledgeBase
    
    # Create test entries
    for i in range(3):
        entry = KnowledgeBase(
            title=f"Test Entry {i}",
            content=f"Test content {i}",
            category="test_category",
            created_by=test_user.id
        )
        db.add(entry)
    db.commit()
    
    response = client.get(
        "/api/v1/knowledge/",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 3


def test_search_knowledge(client, auth_headers):
    """Test semantic search in knowledge base"""
    with patch('app.services.vector_store.vector_store.search') as mock_search:
        mock_search.return_value = [
            {
                'id': 'test123',
                'text': 'Test legal content',
                'metadata': {'title': 'Test Law', 'category': 'civil'},
                'distance': 0.2
            }
        ]
        
        response = client.post(
            "/api/v1/knowledge/search",
            headers=auth_headers,
            json={
                "query": "legal question",
                "limit": 5
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)


@pytest.mark.asyncio
async def test_rag_query(client, auth_headers):
    """Test RAG query endpoint"""
    with patch('app.services.rag_service.rag_service.generate_with_context') as mock_rag:
        mock_rag.return_value = {
            "answer": "Test answer based on knowledge base",
            "sources": [
                {"id": "doc1", "title": "Test Doc", "score": 0.9, "category": "civil"}
            ],
            "model": "gpt-3.5-turbo",
            "usage": {"total_tokens": 150}
        }
        
        response = client.post(
            "/api/v1/knowledge/rag",
            headers=auth_headers,
            json={
                "query": "What are the requirements?",
                "limit": 3
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert isinstance(data["sources"], list)


def test_get_knowledge_stats(client, auth_headers, db):
    """Test getting knowledge base statistics"""
    response = client.get(
        "/api/v1/knowledge/stats/summary",
        headers=auth_headers
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "total_documents" in data
    assert "categories" in data

