"""Service endpoints"""
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from zeebe_rest_gateway.containers import Container
from zeebe_rest_gateway.types.message import Message
from zeebe_rest_gateway.zeebe.client import ZeebeClient, RetryAttemptsExceededError

router = APIRouter()


@router.post('/publish')
@inject
async def publish(message: Message, zeebe_client: ZeebeClient = Depends(Provide[Container.zeebe_client])) -> None:
    """Publish message to Zeebe."""
    try:
        await zeebe_client.publish_message(message)
    except RetryAttemptsExceededError as err:
        raise HTTPException(status_code=500, detail='Zeebe not available. Retry attempts failed.') from err
