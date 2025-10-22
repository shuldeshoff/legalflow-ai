from typing import Dict, Any, List
from app.services.llm.llm_service import llm_service
from app.schemas.llm import ChatRequest, Message, MessageRole, LLMModel
import logging
import json

logger = logging.getLogger(__name__)


class DocumentAnalyzer:
    """Service for analyzing documents using LLM"""
    
    def __init__(self):
        self.llm_service = llm_service
    
    async def analyze_document(
        self,
        text: str,
        title: str,
        analyze_risks: bool = True,
        analyze_key_points: bool = True,
        generate_summary: bool = True,
        model: LLMModel = LLMModel.GPT_4_TURBO
    ) -> Dict[str, Any]:
        """
        Comprehensive document analysis using LLM
        
        Args:
            text: Document text content
            title: Document title
            analyze_risks: Whether to analyze risks
            analyze_key_points: Whether to extract key points
            generate_summary: Whether to generate summary
            model: LLM model to use
        
        Returns:
            Dictionary with analysis results
        """
        try:
            # Build analysis prompt
            system_prompt = self._build_system_prompt()
            user_prompt = self._build_analysis_prompt(
                text=text,
                title=title,
                analyze_risks=analyze_risks,
                analyze_key_points=analyze_key_points,
                generate_summary=generate_summary
            )
            
            messages = [
                Message(role=MessageRole.SYSTEM, content=system_prompt),
                Message(role=MessageRole.USER, content=user_prompt)
            ]
            
            # Send to LLM
            request = ChatRequest(
                messages=messages,
                model=model,
                temperature=0.3,  # Lower temperature for factual analysis
                max_tokens=3000
            )
            
            response = await self.llm_service.chat(request)
            
            # Parse response
            result = self._parse_analysis_response(response.content)
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing document: {e}")
            raise
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for document analysis"""
        return """Ты - профессиональный юридический аналитик с многолетним опытом.
Твоя задача - провести детальный анализ юридических документов.

Правила анализа:
- Будь точен и объективен
- Выделяй важные юридические аспекты
- Указывай потенциальные риски и проблемы
- Давай практические рекомендации
- Используй профессиональную юридическую терминологию
- Структурируй ответ в формате JSON

Формат ответа (строго JSON):
{
  "summary": "Краткое содержание документа (2-3 предложения)",
  "key_points": [
    "Ключевой пункт 1",
    "Ключевой пункт 2",
    ...
  ],
  "risks": [
    {
      "type": "Тип риска",
      "description": "Описание риска",
      "severity": "low|medium|high",
      "recommendation": "Рекомендация по устранению"
    },
    ...
  ],
  "recommendations": "Общие рекомендации по документу"
}"""
    
    def _build_analysis_prompt(
        self,
        text: str,
        title: str,
        analyze_risks: bool,
        analyze_key_points: bool,
        generate_summary: bool
    ) -> str:
        """Build user prompt for analysis"""
        prompt_parts = [
            f"Проанализируй следующий документ:\n",
            f"Название: {title}\n",
            f"Содержание:\n{text[:5000]}\n"  # Limit text length
        ]
        
        prompt_parts.append("\nВыполни следующий анализ:\n")
        
        if generate_summary:
            prompt_parts.append("- Создай краткое содержание документа\n")
        
        if analyze_key_points:
            prompt_parts.append("- Выдели ключевые пункты и условия\n")
        
        if analyze_risks:
            prompt_parts.append("- Определи потенциальные юридические риски\n")
            prompt_parts.append("- Дай рекомендации по каждому риску\n")
        
        prompt_parts.append("\nВерни результат строго в формате JSON, как указано в системном промпте.")
        
        return "".join(prompt_parts)
    
    def _parse_analysis_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured format"""
        try:
            # Try to extract JSON from response
            # Sometimes LLM adds markdown code blocks
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "```" in response:
                json_start = response.find("```") + 3
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            else:
                json_str = response.strip()
            
            result = json.loads(json_str)
            
            # Ensure all fields exist
            return {
                "summary": result.get("summary", ""),
                "key_points": result.get("key_points", []),
                "risks": result.get("risks", []),
                "recommendations": result.get("recommendations", "")
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response: {e}")
            logger.debug(f"Response: {response}")
            
            # Return basic structure with raw response
            return {
                "summary": "Ошибка парсинга результатов анализа",
                "key_points": [],
                "risks": [],
                "recommendations": response
            }
    
    async def extract_summary(self, text: str, max_length: int = 500) -> str:
        """Quick summary extraction"""
        try:
            messages = [
                Message(
                    role=MessageRole.SYSTEM,
                    content="Ты - помощник для создания кратких саммари документов. Отвечай кратко, 2-3 предложения."
                ),
                Message(
                    role=MessageRole.USER,
                    content=f"Создай краткое содержание этого текста:\n\n{text[:3000]}"
                )
            ]
            
            request = ChatRequest(
                messages=messages,
                model=LLMModel.GPT_35_TURBO,
                temperature=0.3,
                max_tokens=200
            )
            
            response = await self.llm_service.chat(request)
            return response.content
            
        except Exception as e:
            logger.error(f"Error extracting summary: {e}")
            return "Не удалось создать краткое содержание"


# Global instance
document_analyzer = DocumentAnalyzer()

