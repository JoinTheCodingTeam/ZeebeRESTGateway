"""
Zeebe REST gateway.

Translates Zeebe gRPC calls to REST requests and vice versa.
"""
import os
from asyncio import sleep

from fastapi import FastAPI, HTTPException
from pyzeebe import ZeebeClient
from pyzeebe.exceptions import ZeebeInternalError, ZeebeBackPressure, ZeebeGatewayUnavailable, MessageAlreadyExists

from zeebe_rest_gateway.types.message import Message

ZEEBE_HOSTNAME = os.getenv('ZEEBE_HOSTNAME')
ZEEBE_PORT = int(os.getenv('ZEEBE_PORT', '26500'))
ZEEBE_PUBLISH_RETRY_ATTEMPTS = max(1, int(os.getenv('ZEEBE_PUBLISH_RETRY_ATTEMPTS', '5')))
ZEEBE_PUBLISH_RETRY_DELAY_MS = int(os.getenv('ZEEBE_PUBLISH_RETRY_DELAY_MS', '100'))

app = FastAPI()
zeebe_client = ZeebeClient(ZEEBE_HOSTNAME, ZEEBE_PORT)


@app.post('/publish')
async def publish(message: Message) -> None:
    """Publish message to Zeebe."""
    attempts = ZEEBE_PUBLISH_RETRY_ATTEMPTS
    last_error_type = None
    while attempts > 0:
        attempts -= 1
        try:
            zeebe_client.publish_message(message.name, message.correlation_key, message.variables,
                                         message.time_to_live_in_milliseconds, message.message_id)
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
