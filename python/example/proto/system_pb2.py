# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: system.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csystem.proto\"\x07\n\x05\x41\x63tor\"\x0b\n\tInterface\"\t\n\x07\x43ommand\"\t\n\x07Message\"u\n\x05\x44rone\x12\x1a\n\nsystemBase\x18\x01 \x01(\x0b\x32\x06.Actor\x12&\n\ttelemetry\x18\x02 \x01(\x0b\x32\x13.TelemetryInterface\x12(\n\ncontroller\x18\x03 \x01(\x0b\x32\x14.ControllerInterface\"\x9a\x01\n\x12TelemetryInterface\x12\x1e\n\nsystemBase\x18\x01 \x01(\x0b\x32\n.Interface\x12+\n\x10requestTelemetry\x18\x02 \x01(\x0b\x32\x11.RequestTelemetry\x12\x37\n\x16telemetryUpdateMessage\x18\x03 \x01(\x0b\x32\x17.TelemetryUpdateMessage\"F\n\x10RequestTelemetry\x12\x1c\n\nsystemBase\x18\x01 \x01(\x0b\x32\x08.Command\x12\x14\n\x0cupdatePeriod\x18\x02 \x01(\x02\"L\n\x16TelemetryUpdateMessage\x12\x1c\n\nsystemBase\x18\x01 \x01(\x0b\x32\x08.Message\x12\x14\n\x0c\x62\x61tteryLevel\x18\x02 \x01(\x02\"P\n\x13\x43ontrollerInterface\x12\x1e\n\nsystemBase\x18\x01 \x01(\x0b\x32\n.Interface\x12\x19\n\x07takeOff\x18\x02 \x01(\x0b\x32\x08.TakeOff\"\'\n\x07TakeOff\x12\x1c\n\nsystemBase\x18\x01 \x01(\x0b\x32\x08.Commandb\x06proto3')



_ACTOR = DESCRIPTOR.message_types_by_name['Actor']
_INTERFACE = DESCRIPTOR.message_types_by_name['Interface']
_COMMAND = DESCRIPTOR.message_types_by_name['Command']
_MESSAGE = DESCRIPTOR.message_types_by_name['Message']
_DRONE = DESCRIPTOR.message_types_by_name['Drone']
_TELEMETRYINTERFACE = DESCRIPTOR.message_types_by_name['TelemetryInterface']
_REQUESTTELEMETRY = DESCRIPTOR.message_types_by_name['RequestTelemetry']
_TELEMETRYUPDATEMESSAGE = DESCRIPTOR.message_types_by_name['TelemetryUpdateMessage']
_CONTROLLERINTERFACE = DESCRIPTOR.message_types_by_name['ControllerInterface']
_TAKEOFF = DESCRIPTOR.message_types_by_name['TakeOff']
Actor = _reflection.GeneratedProtocolMessageType('Actor', (_message.Message,), {
  'DESCRIPTOR' : _ACTOR,
  '__module__' : 'system_pb2'
  # @@protoc_insertion_point(class_scope:Actor)
  })
_sym_db.RegisterMessage(Actor)

Interface = _reflection.GeneratedProtocolMessageType('Interface', (_message.Message,), {
  'DESCRIPTOR' : _INTERFACE,
  '__module__' : 'system_pb2'
  # @@protoc_insertion_point(class_scope:Interface)
  })
_sym_db.RegisterMessage(Interface)

Command = _reflection.GeneratedProtocolMessageType('Command', (_message.Message,), {
  'DESCRIPTOR' : _COMMAND,
  '__module__' : 'system_pb2'
  # @@protoc_insertion_point(class_scope:Command)
  })
_sym_db.RegisterMessage(Command)

Message = _reflection.GeneratedProtocolMessageType('Message', (_message.Message,), {
  'DESCRIPTOR' : _MESSAGE,
  '__module__' : 'system_pb2'
  # @@protoc_insertion_point(class_scope:Message)
  })
_sym_db.RegisterMessage(Message)

Drone = _reflection.GeneratedProtocolMessageType('Drone', (_message.Message,), {
  'DESCRIPTOR' : _DRONE,
  '__module__' : 'system_pb2'
  # @@protoc_insertion_point(class_scope:Drone)
  })
_sym_db.RegisterMessage(Drone)

TelemetryInterface = _reflection.GeneratedProtocolMessageType('TelemetryInterface', (_message.Message,), {
  'DESCRIPTOR' : _TELEMETRYINTERFACE,
  '__module__' : 'system_pb2'
  # @@protoc_insertion_point(class_scope:TelemetryInterface)
  })
_sym_db.RegisterMessage(TelemetryInterface)

RequestTelemetry = _reflection.GeneratedProtocolMessageType('RequestTelemetry', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTTELEMETRY,
  '__module__' : 'system_pb2'
  # @@protoc_insertion_point(class_scope:RequestTelemetry)
  })
_sym_db.RegisterMessage(RequestTelemetry)

TelemetryUpdateMessage = _reflection.GeneratedProtocolMessageType('TelemetryUpdateMessage', (_message.Message,), {
  'DESCRIPTOR' : _TELEMETRYUPDATEMESSAGE,
  '__module__' : 'system_pb2'
  # @@protoc_insertion_point(class_scope:TelemetryUpdateMessage)
  })
_sym_db.RegisterMessage(TelemetryUpdateMessage)

ControllerInterface = _reflection.GeneratedProtocolMessageType('ControllerInterface', (_message.Message,), {
  'DESCRIPTOR' : _CONTROLLERINTERFACE,
  '__module__' : 'system_pb2'
  # @@protoc_insertion_point(class_scope:ControllerInterface)
  })
_sym_db.RegisterMessage(ControllerInterface)

TakeOff = _reflection.GeneratedProtocolMessageType('TakeOff', (_message.Message,), {
  'DESCRIPTOR' : _TAKEOFF,
  '__module__' : 'system_pb2'
  # @@protoc_insertion_point(class_scope:TakeOff)
  })
_sym_db.RegisterMessage(TakeOff)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ACTOR._serialized_start=16
  _ACTOR._serialized_end=23
  _INTERFACE._serialized_start=25
  _INTERFACE._serialized_end=36
  _COMMAND._serialized_start=38
  _COMMAND._serialized_end=47
  _MESSAGE._serialized_start=49
  _MESSAGE._serialized_end=58
  _DRONE._serialized_start=60
  _DRONE._serialized_end=177
  _TELEMETRYINTERFACE._serialized_start=180
  _TELEMETRYINTERFACE._serialized_end=334
  _REQUESTTELEMETRY._serialized_start=336
  _REQUESTTELEMETRY._serialized_end=406
  _TELEMETRYUPDATEMESSAGE._serialized_start=408
  _TELEMETRYUPDATEMESSAGE._serialized_end=484
  _CONTROLLERINTERFACE._serialized_start=486
  _CONTROLLERINTERFACE._serialized_end=566
  _TAKEOFF._serialized_start=568
  _TAKEOFF._serialized_end=607
# @@protoc_insertion_point(module_scope)
