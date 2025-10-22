from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.integration import Payment
from app.schemas.integration import PaymentCreate, PaymentResponse
from app.services.payment_service import payment_service
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/create", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    payment_data: PaymentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new payment"""
    try:
        # Create payment via YooKassa
        yoo_payment = payment_service.create_payment(
            amount=payment_data.amount,
            currency=payment_data.currency,
            description=payment_data.description or "LegalFlow AI - Юридические услуги",
            return_url=payment_data.return_url,
            metadata={
                "user_id": current_user.id,
                "client_id": payment_data.client_id
            }
        )
        
        # Save to database
        db_payment = Payment(
            user_id=current_user.id,
            client_id=payment_data.client_id,
            amount=payment_data.amount,
            currency=payment_data.currency,
            status=yoo_payment["status"],
            payment_system="yookassa",
            payment_id=yoo_payment["payment_id"],
            payment_url=yoo_payment["payment_url"],
            description=payment_data.description
        )
        
        db.add(db_payment)
        await db.commit()
        await db.refresh(db_payment)
        
        logger.info(f"Payment created: {db_payment.id} - {payment_data.amount} {payment_data.currency}")
        
        return db_payment
        
    except Exception as e:
        logger.error(f"Error creating payment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[PaymentResponse])
async def list_payments(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List user payments"""
    try:
        query = select(Payment).where(
            Payment.user_id == current_user.id
        ).offset(skip).limit(limit).order_by(desc(Payment.created_at))
        
        result = await db.execute(query)
        payments = result.scalars().all()
        
        return payments
        
    except Exception as e:
        logger.error(f"Error listing payments: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get payment by ID"""
    try:
        result = await db.execute(
            select(Payment).where(
                Payment.id == payment_id,
                Payment.user_id == current_user.id
            )
        )
        payment = result.scalar_one_or_none()
        
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        return payment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting payment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{payment_id}/check")
async def check_payment_status(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Check payment status with payment provider"""
    try:
        result = await db.execute(
            select(Payment).where(
                Payment.id == payment_id,
                Payment.user_id == current_user.id
            )
        )
        payment = result.scalar_one_or_none()
        
        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")
        
        # Check status with YooKassa
        yoo_payment = payment_service.get_payment(payment.payment_id)
        
        # Update status in database
        payment.status = yoo_payment["status"]
        await db.commit()
        
        return {
            "payment_id": payment.id,
            "status": payment.status,
            "amount": payment.amount,
            "currency": payment.currency,
            "payment_url": payment.payment_url
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking payment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook/yookassa")
async def yookassa_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    YooKassa webhook handler
    
    Receives payment notifications from YooKassa
    """
    try:
        # Get webhook data
        payload = await request.json()
        
        logger.info(f"YooKassa webhook received: {payload}")
        
        # Extract payment info
        event = payload.get("event")
        payment_data = payload.get("object", {})
        payment_id = payment_data.get("id")
        
        if not payment_id:
            raise HTTPException(status_code=400, detail="Invalid webhook payload")
        
        # Find payment in database
        result = await db.execute(
            select(Payment).where(Payment.payment_id == payment_id)
        )
        payment = result.scalar_one_or_none()
        
        if payment:
            # Update payment status
            payment.status = payment_data.get("status")
            await db.commit()
            
            logger.info(f"Payment {payment.id} status updated: {payment.status}")
        
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Error processing YooKassa webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

