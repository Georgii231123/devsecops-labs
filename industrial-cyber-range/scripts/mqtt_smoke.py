#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import threading

import paho.mqtt.client as mqtt

from otlab.mqtt import TELEMETRY_TOPIC


def main() -> None:
    host = os.getenv("OTLAB_MQTT_HOST", "127.0.0.1")
    port = int(os.getenv("OTLAB_MQTT_PORT", "1883"))
    connected = threading.Event()
    subscribed = threading.Event()
    received = threading.Event()
    payload: dict[str, object] = {}

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="otlab-ci-smoke")

    def on_connect(client, userdata, flags, reason_code, properties):
        del userdata, flags, reason_code, properties
        connected.set()
        client.subscribe(TELEMETRY_TOPIC)

    def on_subscribe(client, userdata, mid, reason_code_list, properties):
        del client, userdata, mid, reason_code_list, properties
        subscribed.set()

    def on_message(client, userdata, message):
        del client, userdata
        payload.update(json.loads(message.payload.decode("utf-8")))
        received.set()

    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.connect(host, port, keepalive=10)
    client.loop_start()
    try:
        assert connected.wait(5), "MQTT connection timeout"
        assert subscribed.wait(5), "MQTT subscription timeout"
        info = client.publish(TELEMETRY_TOPIC, json.dumps({"pressure_bar": 2.5}), qos=0)
        info.wait_for_publish(timeout=5)
        assert received.wait(5), "MQTT message timeout"
        assert payload["pressure_bar"] == 2.5
        print("MQTT smoke test: OK")
    finally:
        client.disconnect()
        client.loop_stop()


if __name__ == "__main__":
    main()
