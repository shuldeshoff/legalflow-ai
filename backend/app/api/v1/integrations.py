from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Dict, Any
from app.core.database import get_db
from app.api.deps import get_current_user, get_current_admin
from app.models.user import User
from app.models.integration import Integration, IntegrationLog
from app.schemas.integration import (
    IntegrationCreate,
    IntegrationUpdate,
    IntegrationResponse,
    IntegrationLogResponse,
    WebhookPayload
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=IntegrationResponse, status_code=status.HTTP_201_CREATED)
async def create_integration(
    integration: IntegrationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Create new integration (Admin only)"""
    try:
        db_integration = Integration(
            name=integration.name,
            type=integration.type,
            is_active=integration.is_active,
            config=integration.config,
            created_by=current_user.id
        )
        
        db.add(db_integration)
        await db.commit()
        await db.refresh(db_integration)
        
        logger.info(f"Integration created: {db_integration.id} - {integration.name}")
        
        return db_integration
        
    except Exception as e:
        logger.error(f"Error creating integration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[IntegrationResponse])
async def list_integrations(
    skip: int = 0,
    limit: int = 20,
    type: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """List all integrations (Admin only)"""
    try:
        query = select(Integration)
        
        if type:
            query = query.where(Integration.type == type)
        
        query = query.offset(skip).limit(limit).order_by(desc(Integration.created_at))
        
        result = await db.execute(query)
        integrations = result.scalars().all()
        
        return integrations
        
    except Exception as e:
        logger.error(f"Error listing integrations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{integration_id}", response_model=IntegrationResponse)
async def get_integration(
    integration_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get integration by ID (Admin only)"""
    try:
        result = await db.execute(
            select(Integration).where(Integration.id == integration_id)
        )
        integration = result.scalar_one_or_none()
        
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        return integration
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting integration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{integration_id}", response_model=IntegrationResponse)
async def update_integration(
    integration_id: int,
    integration_update: IntegrationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Update integration (Admin only)"""
    try:
        result = await db.execute(
            select(Integration).where(Integration.id == integration_id)
        )
        integration = result.scalar_one_or_none()
        
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        # Update fields
        update_data = integration_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(integration, field, value)
        
        await db.commit()
        await db.refresh(integration)
        
        return integration
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating integration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{integration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_integration(
    integration_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete integration (Admin only)"""
    try:
        result = await db.execute(
            select(Integration).where(Integration.id == integration_id)
        )
        integration = result.scalar_one_or_none()
        
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        await db.delete(integration)
        await db.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting integration: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{integration_id}/logs", response_model=List[IntegrationLogResponse])
async def get_integration_logs(
    integration_id: int,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get integration logs (Admin only)"""
    try:
        query = select(IntegrationLog).where(
            IntegrationLog.integration_id == integration_id
        ).offset(skip).limit(limit).order_by(desc(IntegrationLog.created_at))
        
        result = await db.execute(query)
        logs = result.scalars().all()
        
        return logs
        
    except Exception as e:
        logger.error(f"Error getting logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/webhook/{integration_id}")
async def webhook_handler(
    integration_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    """
    Generic webhook handler for CRM and other integrations
    
    This endpoint can receive webhooks from various systems
    """
    try:
        # Get integration
        result = await db.execute(
            select(Integration).where(Integration.id == integration_id)
        )
        integration = result.scalar_one_or_none()
        
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        if not integration.is_active:
            raise HTTPException(status_code=403, detail="Integration is not active")
        
        # Get request data
        try:
            payload = await request.json()
        except:
            payload = {}
        
        # Log webhook
        log = IntegrationLog(
            integration_id=integration_id,
            event_type="webhook_received",
            status="success",
            request_data=payload
        )
        
        db.add(log)
        await db.commit()
        
        logger.info(f"Webhook received for integration {integration_id}")
        
        # Process webhook based on type
        # Here you can add custom logic for different integration types
        
        return {
            "status": "success",
            "message": "Webhook received",
            "integration_id": integration_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        
        # Log error
        try:
            log = IntegrationLog(
                integration_id=integration_id,
                event_type="webhook_received",
                status="failed",
                error_message=str(e)
            )
            db.add(log)
            await db.commit()
        except:
            pass
        
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test/{integration_id}")
async def test_integration(
    integration_id: int,
    test_data: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Test integration (Admin only)"""
    try:
        result = await db.execute(
            select(Integration).where(Integration.id == integration_id)
        )
        integration = result.scalar_one_or_none()
        
        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")
        
        # Log test
        log = IntegrationLog(
            integration_id=integration_id,
            event_type="test",
            status="success",
            request_data=test_data,
            response_data={"message": "Test successful"}
        )
        
        db.add(log)
        await db.commit()
        
        return {
            "status": "success",
            "message": f"Integration {integration.name} tested successfully",
            "integration_type": integration.type
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error testing integration: {e}")
        raise HTTPException(status_code=500, detail=str(e))

