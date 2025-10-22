from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from typing import Optional
import logging
from app.core.config import settings
from app.services.llm.llm_service import llm_service
from app.schemas.llm import ChatRequest, Message as LLMMessage, MessageRole, LLMModel

logger = logging.getLogger(__name__)


class ConsultationStates(StatesGroup):
    """FSM states for consultation"""
    waiting_for_question = State()
    waiting_for_details = State()


class TelegramBotService:
    """Telegram bot service for legal consultations"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        self.bot: Optional[Bot] = None
        self.dp: Optional[Dispatcher] = None
        self.router = Router()
        
        if self.token:
            self.bot = Bot(token=self.token)
            self.dp = Dispatcher()
            self.setup_handlers()
    
    def setup_handlers(self):
        """Setup message handlers"""
        
        @self.router.message(Command("start"))
        async def cmd_start(message: Message, state: FSMContext):
            """Handler for /start command"""
            await message.answer(
                "👋 Добро пожаловать в LegalFlow AI!\n\n"
                "Я - ваш AI-помощник по юридическим вопросам.\n\n"
                "Доступные команды:\n"
                "/consult - Получить юридическую консультацию\n"
                "/document - Анализ документа\n"
                "/help - Помощь\n\n"
                "Просто напишите ваш вопрос, и я постараюсь помочь!"
            )
        
        @self.router.message(Command("help"))
        async def cmd_help(message: Message):
            """Handler for /help command"""
            await message.answer(
                "📚 Помощь LegalFlow AI\n\n"
                "Доступные функции:\n\n"
                "1️⃣ Юридические консультации\n"
                "Задавайте вопросы по гражданскому, трудовому, семейному праву.\n\n"
                "2️⃣ Анализ документов\n"
                "Отправьте PDF или DOCX документ для анализа.\n\n"
                "3️⃣ Генерация договоров\n"
                "Помощь в подготовке типовых договоров.\n\n"
                "Команды:\n"
                "/start - Начать работу\n"
                "/consult - Консультация\n"
                "/document - Анализ документа\n"
                "/help - Эта справка"
            )
        
        @self.router.message(Command("consult"))
        async def cmd_consult(message: Message, state: FSMContext):
            """Handler for /consult command"""
            await message.answer(
                "⚖️ Юридическая консультация\n\n"
                "Опишите вашу ситуацию или задайте вопрос.\n"
                "Я постараюсь дать профессиональный совет."
            )
            await state.set_state(ConsultationStates.waiting_for_question)
        
        @self.router.message(ConsultationStates.waiting_for_question)
        async def process_question(message: Message, state: FSMContext):
            """Process user question"""
            question = message.text
            
            # Show typing indicator
            await message.answer("🤔 Анализирую ваш вопрос...")
            
            try:
                # Get AI response
                response = await self._get_ai_response(question)
                await message.answer(response)
                
                # Ask if user needs more details
                await message.answer(
                    "Нужны дополнительные разъяснения? "
                    "Задайте уточняющий вопрос или /start для нового обращения."
                )
                
            except Exception as e:
                logger.error(f"Error processing question: {e}")
                await message.answer(
                    "❌ Извините, произошла ошибка при обработке вашего запроса. "
                    "Попробуйте еще раз позже."
                )
            
            await state.clear()
        
        @self.router.message(Command("document"))
        async def cmd_document(message: Message):
            """Handler for /document command"""
            await message.answer(
                "📄 Анализ документа\n\n"
                "Отправьте документ в формате PDF или DOCX, "
                "и я проведу его анализ:\n"
                "- Краткое содержание\n"
                "- Ключевые пункты\n"
                "- Потенциальные риски\n"
                "- Рекомендации"
            )
        
        @self.router.message(F.document)
        async def process_document(message: Message):
            """Process uploaded document"""
            await message.answer(
                "📎 Документ получен!\n\n"
                "Для полного анализа документа воспользуйтесь "
                "веб-интерфейсом LegalFlow AI.\n\n"
                "Там вы сможете:\n"
                "✅ Загрузить документ\n"
                "✅ Получить детальный анализ\n"
                "✅ Выявить риски\n"
                "✅ Получить рекомендации"
            )
        
        @self.router.message(F.text)
        async def process_text(message: Message):
            """Process regular text messages"""
            question = message.text
            
            await message.answer("💬 Обрабатываю ваш запрос...")
            
            try:
                response = await self._get_ai_response(question)
                await message.answer(response)
            except Exception as e:
                logger.error(f"Error processing text: {e}")
                await message.answer(
                    "❌ Извините, произошла ошибка. "
                    "Попробуйте переформулировать вопрос."
                )
        
        # Register router
        if self.dp:
            self.dp.include_router(self.router)
    
    async def _get_ai_response(self, question: str) -> str:
        """Get AI response for user question"""
        try:
            messages = [
                LLMMessage(
                    role=MessageRole.SYSTEM,
                    content=(
                        "Ты - профессиональный юридический консультант. "
                        "Отвечай кратко, понятно и по существу. "
                        "Давай практические советы. "
                        "Если нужна дополнительная информация - спроси."
                    )
                ),
                LLMMessage(
                    role=MessageRole.USER,
                    content=question
                )
            ]
            
            request = ChatRequest(
                messages=messages,
                model=LLMModel.GPT_35_TURBO,
                temperature=0.7,
                max_tokens=1000
            )
            
            response = await llm_service.chat(request)
            return response.content
            
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            raise
    
    async def send_message(self, chat_id: str, text: str):
        """Send message to chat"""
        if not self.bot:
            raise ValueError("Bot not initialized")
        
        await self.bot.send_message(chat_id=chat_id, text=text)
    
    async def start(self):
        """Start bot polling"""
        if not self.dp or not self.bot:
            raise ValueError("Bot not initialized")
        
        logger.info("Starting Telegram bot...")
        await self.dp.start_polling(self.bot)
    
    async def stop(self):
        """Stop bot"""
        if self.bot:
            await self.bot.session.close()


# Global instance (lazy initialization)
telegram_bot_service: Optional[TelegramBotService] = None


def get_telegram_bot() -> Optional[TelegramBotService]:
    """Get telegram bot instance"""
    global telegram_bot_service
    
    if telegram_bot_service is None:
        telegram_bot_service = TelegramBotService()
    
    return telegram_bot_service

