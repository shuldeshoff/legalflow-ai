from typing import List, Dict, Any
from app.services.vector_store import vector_store
from app.services.llm.llm_service import llm_service
from app.schemas.llm import ChatRequest, Message, MessageRole, LLMModel
import logging

logger = logging.getLogger(__name__)


class RAGService:
    """RAG (Retrieval Augmented Generation) service"""
    
    def __init__(self):
        self.vector_store = vector_store
        self.llm_service = llm_service
    
    async def retrieve_context(
        self,
        query: str,
        n_results: int = 3,
        category: str = None
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents from knowledge base"""
        try:
            where = {"category": category} if category else None
            results = self.vector_store.search(
                query=query,
                n_results=n_results,
                where=where
            )
            return results
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    async def generate_with_context(
        self,
        query: str,
        model: LLMModel = LLMModel.GPT_35_TURBO,
        n_results: int = 3,
        category: str = None
    ) -> Dict[str, Any]:
        """Generate answer using RAG"""
        try:
            # 1. Retrieve relevant documents
            contexts = await self.retrieve_context(query, n_results, category)
            
            if not contexts:
                # No context found, use LLM without context
                logger.warning("No context found for query")
                context_text = "Контекст не найден в базе знаний."
            else:
                # Build context from retrieved documents
                context_parts = []
                for idx, ctx in enumerate(contexts, 1):
                    title = ctx['metadata'].get('title', 'Документ')
                    text = ctx['text']
                    context_parts.append(f"[{idx}] {title}:\n{text}")
                
                context_text = "\n\n".join(context_parts)
            
            # 2. Build prompt with context
            system_prompt = """Ты - профессиональный юридический ассистент.
Используй предоставленный контекст из базы знаний для ответа на вопрос.

Правила:
- Отвечай на основе предоставленного контекста
- Указывай источники (номера документов в скобках)
- Если информации недостаточно - скажи об этом
- Будь точен и профессионален"""
            
            user_prompt = f"""Контекст из базы знаний:
{context_text}

Вопрос пользователя:
{query}

Дай точный ответ на основе контекста выше."""
            
            messages = [
                Message(role=MessageRole.SYSTEM, content=system_prompt),
                Message(role=MessageRole.USER, content=user_prompt)
            ]
            
            # 3. Generate response
            request = ChatRequest(
                messages=messages,
                model=model,
                temperature=0.3,  # Lower temperature for more factual answers
                max_tokens=2000
            )
            
            response = await self.llm_service.chat(request)
            
            # 4. Return result with sources
            return {
                "answer": response.content,
                "sources": [
                    {
                        "id": ctx['id'],
                        "title": ctx['metadata'].get('title', 'Документ'),
                        "score": 1 - ctx['distance'],  # Convert distance to similarity
                        "category": ctx['metadata'].get('category')
                    }
                    for ctx in contexts
                ],
                "model": response.model,
                "usage": response.usage
            }
            
        except Exception as e:
            logger.error(f"Error in RAG generation: {e}")
            raise


# Global RAG service instance
rag_service = RAGService()

