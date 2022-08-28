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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0csystem.proto\"\x07\n\x05\x41\x63tor\"\x0b\n\tInterface\"\t\n\x07\x43ommand\"\t\n\x07Message\"\x87\x01\n\x05\x44rone\x12\x1a\n\nsystemBase\x18\x01 \x01(\x0b\x32\x06.Actor\x12/\n\x12telemetryInterface\x18\x02 \x01(\x0b\x32\x13.TelemetryInterface\x12\x31\n\x13\x63ontrollerInterface\x18\x03 \x01(\x0b\x32\x14.ControllerInterface\"\xa8\x01\n\x12TelemetryInterface\x12\x1e\n\nsystemBase\x18\x01 \x01(\x0b\x32\n.Interface\x12\x39\n\x17requestTelemetryCommand\x18\x02 \x01(\x0b\x32\x18.RequestTelemetryCommand\x12\x37\n\x16telemetryUpdateMessage\x18\x03 \x01(\x0b\x32\x17.TelemetryUpdateMessage\"M\n\x17RequestTelemetryCommand\x12\x1c\n\nsystemBase\x18\x01 \x01(\x0b\x32\x08.Command\x12\x14\n\x0cupdatePeriod\x18\x02 \x01(\x02\"L\n\x16TelemetryUpdateMessage\x12\x1c\n\nsystemBase\x18\x01 \x01(\x0b\x32\x08.Message\x12\x14\n\x0c\x62\x61tteryLevel\x18\x02 \x01(\x02\"Z\n\x13\x43ontrollerInterface\x12\x1e\n\nsystemBase\x18\x01 \x01(\x0b\x32\n.Interface\x12#\n\x0cstartCommand\x18\x02 \x01(\x0b\x32\r.StartCommand\",\n\x0cStartCommand\x12\x1c\n\nsystemBase\x18\x01 \x01(\x0b\x32\x08.Commandb\x06proto3')



_ACTOR = DESCRIPTOR.message_types_by_name['Actor']
_INTERFACE = DESCRIPTOR.message_types_by_name['Interface']
_COMMAND = DESCRIPTOR.message_types_by_name['Command']
_MESSAGE = DESCRIPTOR.message_types_by_name['Message']
_DRONE = DESCRIPTOR.message_types_by_name['Drone']
_TELEMETRYINTERFACE = DESCRIPTOR.message_types_by_name['TelemetryInterface']
_REQUESTTELEMETRYCOMMAND = DESCRIPTOR.message_types_by_name['RequestTelemetryCommand']
_TELEMETRYUPDATEMESSAGE = DESCRIPTOR.message_types_by_name['TelemetryUpdateMessage']
_CONTROLLERINTERFACE = DESCRIPTOR.message_types_by_name['ControllerInterface']
_STARTCOMMAND = DESCRIPTOR.message_types_by_name['StartCommand']
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

RequestTelemetryCommand = _reflection.GeneratedProtocolMessageType('RequestTelemetryCommand', (_message.Message,), {
  'DESCRIPTOR' : _REQUESTTELEMETRYCOMMAND,
  '__module__' : 'system_pb2'
  # @@protoc_insertion_point(class_scope:RequestTelemetryCommand)
  })
_sym_db.RegisterMessage(RequestTelemetryCommand)

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

StartCommand = _reflection.GeneratedProtocolMessageType('StartCommand', (_message.Message,), {
  'DESCRIPTOR' : _STARTCOMMAND,
  '__module__' : 'system_pb2'
  # @@protoc_insertion_point(class_scope:StartCommand)
  })
_sym_db.RegisterMessage(StartCommand)

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
  _DRONE._serialized_start=61
  _DRONE._serialized_end=196
  _TELEMETRYINTERFACE._serialized_start=199
  _TELEMETRYINTERFACE._serialized_end=367
  _REQUESTTELEMETRYCOMMAND._serialized_start=369
  _REQUESTTELEMETRYCOMMAND._serialized_end=446
  _TELEMETRYUPDATEMESSAGE._serialized_start=448
  _TELEMETRYUPDATEMESSAGE._serialized_end=524
  _CONTROLLERINTERFACE._serialized_start=526
  _CONTROLLERINTERFACE._serialized_end=616
  _STARTCOMMAND._serialized_start=618
  _STARTCOMMAND._serialized_end=662
# @@protoc_insertion_point(module_scope)