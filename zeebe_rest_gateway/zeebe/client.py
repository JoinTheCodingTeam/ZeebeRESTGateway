"""Zeebe gRPC client"""
from asyncio import sleep
from typing import Optional

import grpc
from fastapi.logger import logger

from zeebe_rest_gateway.settings import Settings
from zeebe_rest_gateway.spec.gateway_pb2_grpc import GatewayStub
from zeebe_rest_gateway.types.message import Message


class UnrecoverableZeebeError(Exception):
    """Unrecoverable Zeebe exception"""

    def __init__(self, code: grpc.StatusCode, details: Optional[str]):
        super().__init__()
        self.code = code
        self.details = details


class RetryAttemptsExceededError(Exception):
    """Exception raised when retry attempts exceeded"""

    def __init__(self, code: grpc.StatusCode, details: Optional[str]):
        super().__init__()
        self.code = code
        self.details = details


class ZeebeClient:
    """Zeebe gRPC client"""

    def __init__(self, *, settings: Settings, gateway_stub: GatewayStub):
        self.settings = settings
        self.gateway_stub = gateway_stub

    async def publish_message(self, message: Message):
        """Publish message to Zeebe."""
        request = message.to_request()
        attempt_number = 1
        while True:
            logger.debug('Publishing message %s[%s] (attempt %d)', message.name, message.message_id, attempt_number)
            attempt_number += 1

            try:
                response = await self.gateway_stub.PublishMessage(request)
                logger.debug('PublishMessage response: %s', response)
                return
            except grpc.aio.AioRpcError as err:
                if err.code() in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.RESOURCE_EXHAUSTED,
                                  grpc.StatusCode.INTERNAL):
                    # Recoverable errors, retrying.
                    if attempt_number > self.settings.zeebe_publish_retry_attempts:
                        raise RetryAttemptsExceededError(err.code(), err.details()) from err

                    logger.debug("Message %s[%s] couldn't be delivered, retrying", message.name, message.message_id)
                    await sleep(self.settings.zeebe_publish_retry_delay_ms / 1000)
                    continue

                if err.code() == grpc.StatusCode.ALREADY_EXISTS:
                    logger.debug('Message %s[%s] already published, skipping.', message.name, message.message_id)
                    return

                raise UnrecoverableZeebeError(err.code(), err.details()) from err
