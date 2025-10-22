from yookassa import Configuration, Payment as YooPayment
from typing import Dict, Any, Optional
import logging
from app.core.config import settings
from uuid import uuid4

logger = logging.getLogger(__name__)


class PaymentService:
    """Service for payment processing via YooKassa"""
    
    def __init__(self):
        # Configure YooKassa
        self.shop_id = getattr(settings, 'YOOKASSA_SHOP_ID', None)
        self.secret_key = getattr(settings, 'YOOKASSA_SECRET_KEY', None)
        
        if self.shop_id and self.secret_key:
            Configuration.account_id = self.shop_id
            Configuration.secret_key = self.secret_key
            self.enabled = True
            logger.info("YooKassa payment service initialized")
        else:
            self.enabled = False
            logger.warning("YooKassa credentials not configured")
    
    def create_payment(
        self,
        amount: int,
        currency: str = "RUB",
        description: str = "",
        return_url: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create payment
        
        Args:
            amount: Amount in kopecks (e.g., 10000 = 100 RUB)
            currency: Currency code (RUB, USD, EUR)
            description: Payment description
            return_url: URL to redirect after payment
            metadata: Additional metadata
        
        Returns:
            Payment data with payment_id and confirmation_url
        """
        if not self.enabled:
            raise ValueError("Payment service not configured")
        
        try:
            # Create payment
            idempotence_key = str(uuid4())
            
            payment_data = {
                "amount": {
                    "value": f"{amount / 100:.2f}",  # Convert kopecks to rubles
                    "currency": currency
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": return_url or "https://legalflow.ai/payment/success"
                },
                "capture": True,
                "description": description
            }
            
            if metadata:
                payment_data["metadata"] = metadata
            
            payment = YooPayment.create(payment_data, idempotence_key)
            
            return {
                "payment_id": payment.id,
                "status": payment.status,
                "payment_url": payment.confirmation.confirmation_url if payment.confirmation else None,
                "created_at": payment.created_at
            }
            
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            raise
    
    def get_payment(self, payment_id: str) -> Dict[str, Any]:
        """Get payment status"""
        if not self.enabled:
            raise ValueError("Payment service not configured")
        
        try:
            payment = YooPayment.find_one(payment_id)
            
            return {
                "payment_id": payment.id,
                "status": payment.status,
                "amount": float(payment.amount.value),
                "currency": payment.amount.currency,
                "paid": payment.paid,
                "created_at": payment.created_at
            }
            
        except Exception as e:
            logger.error(f"Error getting payment: {e}")
            raise
    
    def cancel_payment(self, payment_id: str) -> bool:
        """Cancel payment"""
        if not self.enabled:
            raise ValueError("Payment service not configured")
        
        try:
            payment = YooPayment.cancel(payment_id, str(uuid4()))
            return payment.status == "canceled"
            
        except Exception as e:
            logger.error(f"Error canceling payment: {e}")
            return False


# Global instance
payment_service = PaymentService()

