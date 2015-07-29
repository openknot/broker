"""MQTT"""


from __future__ import print_function


from paho.mqtt.client import Client

from circuits import Event, Component


from .utils import parse_bind


class mqtt(Event):
    """mqtt Event"""


class MQTT(Component):

    def init(self, url):
        self.url = url

        host, port = parse_bind(self.url)

        self.client = Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

        self.client.connect(host, port)
        self.client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        print("Connected with result code {0}".format(rc))

    def _on_message(self, client, userdata, msg):
        print("{0} {1}".format(msg.topic, msg.payload))
