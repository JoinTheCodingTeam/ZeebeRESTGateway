from typing import Dict, Any, Optional

from pydantic import ConstrainedStr, BaseModel, Field, PositiveInt


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
