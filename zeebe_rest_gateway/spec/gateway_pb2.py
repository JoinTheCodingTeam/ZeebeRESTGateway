# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zeebe_rest_gateway/spec/gateway.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='zeebe_rest_gateway/spec/gateway.proto',
  package='gateway_protocol',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n%zeebe_rest_gateway/spec/gateway.proto\x12\x10gateway_protocol\"w\n\x15PublishMessageRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x16\n\x0e\x63orrelationKey\x18\x02 \x01(\t\x12\x12\n\ntimeToLive\x18\x03 \x01(\x03\x12\x11\n\tmessageId\x18\x04 \x01(\t\x12\x11\n\tvariables\x18\x05 \x01(\t\"%\n\x16PublishMessageResponse\x12\x0b\n\x03key\x18\x01 \x01(\x03\"\x8e\x01\n\x13\x41\x63tivateJobsRequest\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0e\n\x06worker\x18\x02 \x01(\t\x12\x0f\n\x07timeout\x18\x03 \x01(\x03\x12\x19\n\x11maxJobsToActivate\x18\x04 \x01(\x05\x12\x15\n\rfetchVariable\x18\x05 \x03(\t\x12\x16\n\x0erequestTimeout\x18\x06 \x01(\x03\"D\n\x14\x41\x63tivateJobsResponse\x12,\n\x04jobs\x18\x01 \x03(\x0b\x32\x1e.gateway_protocol.ActivatedJob\"\xa8\x02\n\x0c\x41\x63tivatedJob\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x1a\n\x12processInstanceKey\x18\x03 \x01(\x03\x12\x15\n\rbpmnProcessId\x18\x04 \x01(\t\x12 \n\x18processDefinitionVersion\x18\x05 \x01(\x05\x12\x1c\n\x14processDefinitionKey\x18\x06 \x01(\x03\x12\x11\n\telementId\x18\x07 \x01(\t\x12\x1a\n\x12\x65lementInstanceKey\x18\x08 \x01(\x03\x12\x15\n\rcustomHeaders\x18\t \x01(\t\x12\x0e\n\x06worker\x18\n \x01(\t\x12\x0f\n\x07retries\x18\x0b \x01(\x05\x12\x10\n\x08\x64\x65\x61\x64line\x18\x0c \x01(\x03\x12\x11\n\tvariables\x18\r \x01(\t\"7\n\x12\x43ompleteJobRequest\x12\x0e\n\x06jobKey\x18\x01 \x01(\x03\x12\x11\n\tvariables\x18\x02 \x01(\t\"\x15\n\x13\x43ompleteJobResponse\"G\n\x0e\x46\x61ilJobRequest\x12\x0e\n\x06jobKey\x18\x01 \x01(\x03\x12\x0f\n\x07retries\x18\x02 \x01(\x05\x12\x14\n\x0c\x65rrorMessage\x18\x03 \x01(\t\"\x11\n\x0f\x46\x61ilJobResponse\"L\n\x11ThrowErrorRequest\x12\x0e\n\x06jobKey\x18\x01 \x01(\x03\x12\x11\n\terrorCode\x18\x02 \x01(\t\x12\x14\n\x0c\x65rrorMessage\x18\x03 \x01(\t\"\x14\n\x12ThrowErrorResponse2\xd3\x01\n\x07Gateway\x12\x65\n\x0ePublishMessage\x12\'.gateway_protocol.PublishMessageRequest\x1a(.gateway_protocol.PublishMessageResponse\"\x00\x12\x61\n\x0c\x41\x63tivateJobs\x12%.gateway_protocol.ActivateJobsRequest\x1a&.gateway_protocol.ActivateJobsResponse\"\x00\x30\x01\x62\x06proto3'
)




_PUBLISHMESSAGEREQUEST = _descriptor.Descriptor(
  name='PublishMessageRequest',
  full_name='gateway_protocol.PublishMessageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='gateway_protocol.PublishMessageRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='correlationKey', full_name='gateway_protocol.PublishMessageRequest.correlationKey', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timeToLive', full_name='gateway_protocol.PublishMessageRequest.timeToLive', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='messageId', full_name='gateway_protocol.PublishMessageRequest.messageId', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='variables', full_name='gateway_protocol.PublishMessageRequest.variables', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=59,
  serialized_end=178,
)


_PUBLISHMESSAGERESPONSE = _descriptor.Descriptor(
  name='PublishMessageResponse',
  full_name='gateway_protocol.PublishMessageResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='gateway_protocol.PublishMessageResponse.key', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=180,
  serialized_end=217,
)


_ACTIVATEJOBSREQUEST = _descriptor.Descriptor(
  name='ActivateJobsRequest',
  full_name='gateway_protocol.ActivateJobsRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='gateway_protocol.ActivateJobsRequest.type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='worker', full_name='gateway_protocol.ActivateJobsRequest.worker', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='timeout', full_name='gateway_protocol.ActivateJobsRequest.timeout', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='maxJobsToActivate', full_name='gateway_protocol.ActivateJobsRequest.maxJobsToActivate', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='fetchVariable', full_name='gateway_protocol.ActivateJobsRequest.fetchVariable', index=4,
      number=5, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='requestTimeout', full_name='gateway_protocol.ActivateJobsRequest.requestTimeout', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=220,
  serialized_end=362,
)


_ACTIVATEJOBSRESPONSE = _descriptor.Descriptor(
  name='ActivateJobsResponse',
  full_name='gateway_protocol.ActivateJobsResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='jobs', full_name='gateway_protocol.ActivateJobsResponse.jobs', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=364,
  serialized_end=432,
)


_ACTIVATEDJOB = _descriptor.Descriptor(
  name='ActivatedJob',
  full_name='gateway_protocol.ActivatedJob',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='gateway_protocol.ActivatedJob.key', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='type', full_name='gateway_protocol.ActivatedJob.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='processInstanceKey', full_name='gateway_protocol.ActivatedJob.processInstanceKey', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='bpmnProcessId', full_name='gateway_protocol.ActivatedJob.bpmnProcessId', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='processDefinitionVersion', full_name='gateway_protocol.ActivatedJob.processDefinitionVersion', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='processDefinitionKey', full_name='gateway_protocol.ActivatedJob.processDefinitionKey', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='elementId', full_name='gateway_protocol.ActivatedJob.elementId', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='elementInstanceKey', full_name='gateway_protocol.ActivatedJob.elementInstanceKey', index=7,
      number=8, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='customHeaders', full_name='gateway_protocol.ActivatedJob.customHeaders', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='worker', full_name='gateway_protocol.ActivatedJob.worker', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retries', full_name='gateway_protocol.ActivatedJob.retries', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='deadline', full_name='gateway_protocol.ActivatedJob.deadline', index=11,
      number=12, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='variables', full_name='gateway_protocol.ActivatedJob.variables', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=435,
  serialized_end=731,
)


_COMPLETEJOBREQUEST = _descriptor.Descriptor(
  name='CompleteJobRequest',
  full_name='gateway_protocol.CompleteJobRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='jobKey', full_name='gateway_protocol.CompleteJobRequest.jobKey', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='variables', full_name='gateway_protocol.CompleteJobRequest.variables', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=733,
  serialized_end=788,
)


_COMPLETEJOBRESPONSE = _descriptor.Descriptor(
  name='CompleteJobResponse',
  full_name='gateway_protocol.CompleteJobResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=790,
  serialized_end=811,
)


_FAILJOBREQUEST = _descriptor.Descriptor(
  name='FailJobRequest',
  full_name='gateway_protocol.FailJobRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='jobKey', full_name='gateway_protocol.FailJobRequest.jobKey', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='retries', full_name='gateway_protocol.FailJobRequest.retries', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='errorMessage', full_name='gateway_protocol.FailJobRequest.errorMessage', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=813,
  serialized_end=884,
)


_FAILJOBRESPONSE = _descriptor.Descriptor(
  name='FailJobResponse',
  full_name='gateway_protocol.FailJobResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=886,
  serialized_end=903,
)


_THROWERRORREQUEST = _descriptor.Descriptor(
  name='ThrowErrorRequest',
  full_name='gateway_protocol.ThrowErrorRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='jobKey', full_name='gateway_protocol.ThrowErrorRequest.jobKey', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='errorCode', full_name='gateway_protocol.ThrowErrorRequest.errorCode', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='errorMessage', full_name='gateway_protocol.ThrowErrorRequest.errorMessage', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=905,
  serialized_end=981,
)


_THROWERRORRESPONSE = _descriptor.Descriptor(
  name='ThrowErrorResponse',
  full_name='gateway_protocol.ThrowErrorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=983,
  serialized_end=1003,
)

_ACTIVATEJOBSRESPONSE.fields_by_name['jobs'].message_type = _ACTIVATEDJOB
DESCRIPTOR.message_types_by_name['PublishMessageRequest'] = _PUBLISHMESSAGEREQUEST
DESCRIPTOR.message_types_by_name['PublishMessageResponse'] = _PUBLISHMESSAGERESPONSE
DESCRIPTOR.message_types_by_name['ActivateJobsRequest'] = _ACTIVATEJOBSREQUEST
DESCRIPTOR.message_types_by_name['ActivateJobsResponse'] = _ACTIVATEJOBSRESPONSE
DESCRIPTOR.message_types_by_name['ActivatedJob'] = _ACTIVATEDJOB
DESCRIPTOR.message_types_by_name['CompleteJobRequest'] = _COMPLETEJOBREQUEST
DESCRIPTOR.message_types_by_name['CompleteJobResponse'] = _COMPLETEJOBRESPONSE
DESCRIPTOR.message_types_by_name['FailJobRequest'] = _FAILJOBREQUEST
DESCRIPTOR.message_types_by_name['FailJobResponse'] = _FAILJOBRESPONSE
DESCRIPTOR.message_types_by_name['ThrowErrorRequest'] = _THROWERRORREQUEST
DESCRIPTOR.message_types_by_name['ThrowErrorResponse'] = _THROWERRORRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PublishMessageRequest = _reflection.GeneratedProtocolMessageType('PublishMessageRequest', (_message.Message,), {
  'DESCRIPTOR' : _PUBLISHMESSAGEREQUEST,
  '__module__' : 'zeebe_rest_gateway.spec.gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway_protocol.PublishMessageRequest)
  })
_sym_db.RegisterMessage(PublishMessageRequest)

PublishMessageResponse = _reflection.GeneratedProtocolMessageType('PublishMessageResponse', (_message.Message,), {
  'DESCRIPTOR' : _PUBLISHMESSAGERESPONSE,
  '__module__' : 'zeebe_rest_gateway.spec.gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway_protocol.PublishMessageResponse)
  })
_sym_db.RegisterMessage(PublishMessageResponse)

ActivateJobsRequest = _reflection.GeneratedProtocolMessageType('ActivateJobsRequest', (_message.Message,), {
  'DESCRIPTOR' : _ACTIVATEJOBSREQUEST,
  '__module__' : 'zeebe_rest_gateway.spec.gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway_protocol.ActivateJobsRequest)
  })
_sym_db.RegisterMessage(ActivateJobsRequest)

ActivateJobsResponse = _reflection.GeneratedProtocolMessageType('ActivateJobsResponse', (_message.Message,), {
  'DESCRIPTOR' : _ACTIVATEJOBSRESPONSE,
  '__module__' : 'zeebe_rest_gateway.spec.gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway_protocol.ActivateJobsResponse)
  })
_sym_db.RegisterMessage(ActivateJobsResponse)

ActivatedJob = _reflection.GeneratedProtocolMessageType('ActivatedJob', (_message.Message,), {
  'DESCRIPTOR' : _ACTIVATEDJOB,
  '__module__' : 'zeebe_rest_gateway.spec.gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway_protocol.ActivatedJob)
  })
_sym_db.RegisterMessage(ActivatedJob)

CompleteJobRequest = _reflection.GeneratedProtocolMessageType('CompleteJobRequest', (_message.Message,), {
  'DESCRIPTOR' : _COMPLETEJOBREQUEST,
  '__module__' : 'zeebe_rest_gateway.spec.gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway_protocol.CompleteJobRequest)
  })
_sym_db.RegisterMessage(CompleteJobRequest)

CompleteJobResponse = _reflection.GeneratedProtocolMessageType('CompleteJobResponse', (_message.Message,), {
  'DESCRIPTOR' : _COMPLETEJOBRESPONSE,
  '__module__' : 'zeebe_rest_gateway.spec.gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway_protocol.CompleteJobResponse)
  })
_sym_db.RegisterMessage(CompleteJobResponse)

FailJobRequest = _reflection.GeneratedProtocolMessageType('FailJobRequest', (_message.Message,), {
  'DESCRIPTOR' : _FAILJOBREQUEST,
  '__module__' : 'zeebe_rest_gateway.spec.gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway_protocol.FailJobRequest)
  })
_sym_db.RegisterMessage(FailJobRequest)

FailJobResponse = _reflection.GeneratedProtocolMessageType('FailJobResponse', (_message.Message,), {
  'DESCRIPTOR' : _FAILJOBRESPONSE,
  '__module__' : 'zeebe_rest_gateway.spec.gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway_protocol.FailJobResponse)
  })
_sym_db.RegisterMessage(FailJobResponse)

ThrowErrorRequest = _reflection.GeneratedProtocolMessageType('ThrowErrorRequest', (_message.Message,), {
  'DESCRIPTOR' : _THROWERRORREQUEST,
  '__module__' : 'zeebe_rest_gateway.spec.gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway_protocol.ThrowErrorRequest)
  })
_sym_db.RegisterMessage(ThrowErrorRequest)

ThrowErrorResponse = _reflection.GeneratedProtocolMessageType('ThrowErrorResponse', (_message.Message,), {
  'DESCRIPTOR' : _THROWERRORRESPONSE,
  '__module__' : 'zeebe_rest_gateway.spec.gateway_pb2'
  # @@protoc_insertion_point(class_scope:gateway_protocol.ThrowErrorResponse)
  })
_sym_db.RegisterMessage(ThrowErrorResponse)



_GATEWAY = _descriptor.ServiceDescriptor(
  name='Gateway',
  full_name='gateway_protocol.Gateway',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=1006,
  serialized_end=1217,
  methods=[
  _descriptor.MethodDescriptor(
    name='PublishMessage',
    full_name='gateway_protocol.Gateway.PublishMessage',
    index=0,
    containing_service=None,
    input_type=_PUBLISHMESSAGEREQUEST,
    output_type=_PUBLISHMESSAGERESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ActivateJobs',
    full_name='gateway_protocol.Gateway.ActivateJobs',
    index=1,
    containing_service=None,
    input_type=_ACTIVATEJOBSREQUEST,
    output_type=_ACTIVATEJOBSRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_GATEWAY)

DESCRIPTOR.services_by_name['Gateway'] = _GATEWAY

# @@protoc_insertion_point(module_scope)
