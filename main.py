#!/usr/bin/env python3
from __future__ import annotations
# TODO: replace with async?
from pysiaalarm import SIAClient, SIAAccount, SIAEvent
from typing import NamedTuple, Optional
from paho.mqtt.client import Client as MqttClient

def handle_event(event: SIAEvent) -> None:
    #print(event)
    print(event.ri, event.code)
    assert event.valid_message
    parsed = ParsedEvent.from_sia(event)
    print(parsed)
    if parsed:
        mqtt.publish(f"sia/{parsed.type_}", parsed.triggered)

class ParsedEvent(NamedTuple):
    type_: int
    triggered: bool

    @classmethod
    def from_sia(cls, event: SIAEvent) -> Optional[ParsedEvent]:
        if not event.ri:
            print(f"unknown event ri")
            return None
        type_ = int(event.ri)
        match event.code:
            case "BA" | "FA" | "YZ":
                triggered = True
            case "BH" | "FH" | "YX":
                triggered = False
            case code:
                print(f"unknown event code: {code}")
                return None
        return cls(type_, triggered)

sia = SIAClient("0.0.0.0", 1234, [SIAAccount("12345678")], handle_event)
mqtt = MqttClient()
mqtt.connect("mqttserver")

with sia as s:
    while True:
        pass
