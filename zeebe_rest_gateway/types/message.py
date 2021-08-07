"""
A type for messages published to Zeebe via REST gateway.
"""
import json
from typing import Dict, Any, Optional

from google.protobuf.reflection import GeneratedProtocolMessageType
from pydantic import ConstrainedStr, BaseModel, Field, PositiveInt

from zeebe_rest_gateway.spec.gateway_pb2 import PublishMessageRequest


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
    time_to_live_ms: Optional[PositiveInt] = Field(default=None, title='How long this message should stay active. '
                                                                       'Default: 60000 ms (60 seconds)')
    message_id: NonEmptyStr = Field(title='A unique message id, usually GUID, for avoiding duplication. '
                                          'If a message with this id is still active, the copy is silently ignored.')

    class Config:
        """Model configuration"""
        schema_extra = {
            'example': {
                'name': 'example_message',
                'correlation_key': '0x3113123123',
                'variables': {'value': 5},
                'message_id': 'c2c4e256054345e4900bb062d62ab5b5',
            }
        }

    def to_request(self) -> GeneratedProtocolMessageType:
        """Converts message to Zeebe gRPC request type"""
        json_variables = json.dumps(self.variables)
        return PublishMessageRequest(name=self.name, correlationKey=self.correlation_key,
                                     timeToLive=self.time_to_live_ms, messageId=self.message_id,
                                     variables=json_variables)
