"""
Zeebe gRPC<->REST adapter.
"""
import os
import uuid
from asyncio import sleep
from typing import Optional, Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, PositiveInt, Field, ConstrainedStr
from pyzeebe import ZeebeClient
from pyzeebe.exceptions import ZeebeInternalError, ZeebeBackPressure, ZeebeGatewayUnavailable, MessageAlreadyExists

ZEEBE_HOSTNAME = os.getenv('ZEEBE_HOSTNAME')
ZEEBE_PORT = int(os.getenv('ZEEBE_PORT', '26500'))
ZEEBE_PUBLISH_RETRY_ATTEMPTS = max(1, int(os.getenv('ZEEBE_PUBLISH_RETRY_ATTEMPTS', '5')))
ZEEBE_PUBLISH_RETRY_DELAY_MS = int(os.getenv('ZEEBE_PUBLISH_RETRY_DELAY_MS', '100'))

app = FastAPI()
zeebe_client = ZeebeClient(ZEEBE_HOSTNAME, ZEEBE_PORT)


class NonEmptyStr(ConstrainedStr):
    """Type for non-empty string"""
    min_length = 1
    strip_whitespace = True


class Message(BaseModel):
    """Message"""
    name: NonEmptyStr = Field(title='The message name')
    correlation_key: NonEmptyStr = \
        Field(title='The correlation key. For more info: '
                    'https://docs.zeebe.io/glossary.html?highlight=correlation#correlation-key')
    variables: Dict[str, Any] = Field(title='Message payload. The variables the message should contain.')
    time_to_live_in_milliseconds: Optional[PositiveInt] = Field(default=None,
                                                                title='How long this message should stay active. '
                                                                      'Default: 60000 ms (60 seconds)')

    class Config:
        """Model configuration"""
        schema_extra = {
            'example': {
                'name': 'example_message',
                'correlation_key': '0x3113123123',
                'variables': {'value': 5},
            }
        }


@app.post('/publish')
async def publish(message: Message) -> None:
    """Publish message to Zeebe."""
    attempts = ZEEBE_PUBLISH_RETRY_ATTEMPTS
    message_id = uuid.uuid4().hex
    last_error_type = None
    while attempts > 0:
        attempts -= 1
        try:
            zeebe_client.publish_message(message.name, message.correlation_key, message.variables,
                                         message.time_to_live_in_milliseconds, message_id)
        except (ZeebeInternalError, ZeebeBackPressure, ZeebeGatewayUnavailable) as err:
            # Retrying after a delay.
            await sleep(ZEEBE_PUBLISH_RETRY_DELAY_MS / 1000)
            last_error_type = type(err).__name__
            continue

        except MessageAlreadyExists:
            # Silently skipping.
            return

        return
    raise HTTPException(status_code=500, detail=f'Unrecoverable Zeebe error ({last_error_type})`. All retries failed.')
