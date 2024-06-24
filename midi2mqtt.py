import paho.mqtt.client as mqtt
import rtmidi.midiutil as midi
import argparse
import time
import json
import logging
import logging.handlers
import os

# Set up basic logging
if 'JOURNAL_STREAM' in os.environ:
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    logging.basicConfig(level=logging.WARNING, handlers=[handler])  # Changed to WARNING
else:
    logging.basicConfig(level=logging.WARNING)  # Changed to WARNING

class Midi2Broker:
    """Receiving MIDI events and sending them to an MQTT broker."""

    def __init__(self, host, port, midi_port, topicprefix):
        self.topicprefix = topicprefix
        self.midiin, port_name = midi.open_midiinput(midi_port)
        logging.info("Listening to MIDI device: %s", port_name)
        self.midiin.set_callback(self.on_midi_event)

        self.mqtt = mqtt.Client()
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_disconnect = self.on_disconnect
        self.mqtt.on_publish = self.on_publish
        logging.info("Connecting to MQTT broker at %s:%d", host, port)
        self.mqtt.connect(host, port)
        self.mqtt.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to MQTT broker successfully.")
        else:
            logging.error("Failed to connect to MQTT broker, return code %d", rc)

    def on_disconnect(self, client, userdata, rc):
        logging.warning("Disconnected from MQTT broker with return code %d", rc)

    def on_publish(self, client, userdata, mid):
        logging.info("Message published with mid %s", mid)

    def on_midi_event(self, event, data=None):
        message, _ = event
        chan, note, val = message
        logging.info("MIDI event received: Channel: %d, Note: %d, Value: %d", chan, note, val)
        self.publish(self.topicprefix + f"/chan/{chan}/note/{note}", val)

    def publish(self, topic, payload):
        json_payload = json.dumps({'value': payload})
        result = self.mqtt.publish(topic, json_payload)
        status = result[0]
        if status == 0:
            logging.info("Sent payload to topic %s", topic)
        else:
            logging.error("Failed to send payload to topic %s", topic)

    def start_loop(self):
        """Run an endless loop and wait for events."""
        try:
            while True:
                time.sleep(0.1)  # Use a small sleep to prevent blocking
        except KeyboardInterrupt:
            logging.info("Exiting on user request.")
            self.mqtt.loop_stop()
            self.midiin.close_port()
            exit()
        except Exception as e:
            logging.exception("An exception occurred: %s", e)
            self.mqtt.loop_stop()
            self.midiin.close_port()
            exit()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help="Host of the MQTT-Broker, defaults to localhost", default="localhost")
    parser.add_argument('--port', help="Port of the MQTT-Broker, default: 1883", type=int, default=1883)
    parser.add_argument('--midiport', help="Port of the MIDI Interface, default:1", type=int, default=1)
    parser.add_argument('--topicprefix', help="Prefix for the MQTT topic default:midi", type=str, default="midi")
    args = parser.parse_args()

    logging.info('Use a client to watch MQTT messages: mosquitto_sub -h %s -t "%s/#" -v', args.host, args.topicprefix)
    client = Midi2Broker(args.host, args.port, args.midiport, args.topicprefix)
    client.start_loop()

if __name__ == "__main__":
    main()