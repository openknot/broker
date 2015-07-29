#!/usr/bin/env python


"""OpenKnot Broker Daemon"""


from __future__ import print_function


import os
import sys
import logging
from os import environ
from logging import getLogger
from json import dumps, loads
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser


from circuits.web import Controller, Server
from circuits import handler, Component, Debugger


from .events import message
from .mqtt import mqtt, MQTT
from .utils import parse_bind, waitfor


def setup_logging(args):
    logstream = sys.stderr if args.logfile is None else open(args.logfile, "a")

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG if args.debug else logging.INFO,
        stream=logstream,
    )

    return getLogger(__name__)


def setup_mqtt(args, logger):
    if not args.url:
        logger.error("No MQTT URL specified!")
        raise SystemExit(1)

    host, port = parse_bind(args.url)

    logger.debug("Waiting for MQTT Service on {0:s}:{1:d} ...".format(host, port))

    if not waitfor(host, port):
        logger.error("Timed out waiting for MQTT Service on {0:s}:{1:d} ...".format(host, port))
        raise SystemExit(1)


class JSONSerializer(Component):

    channel = "web"

    # 1 higher than the default response handler
    @handler("response", priority=1.0)
    def serialize_response_body(self, response):
        if isinstance(response.body, dict):
            response.headers["Content-Type"] = "application/json"
            response.body = dumps(response.body)


class Dispatcher(Component):

    def message(self, payload):
        protocol = payload.get("protocol", "unknown")

        self.fire(mqtt(protocol, payload))


class API(Controller):

    channel = "/message"

    def POST(self, event, *args, **kwargs):
        req, res = event.args[:2]
        payload = loads(req.body.read())

        self.fire(message(payload))

        return {"success": True}


class App(Component):

    def init(self, args):
        self.args = args

        self.logger = getLogger(__name__)

        if self.args.debug:
            Debugger().register(self)

        bind = parse_bind(self.args.bind)

        MQTT(args.url).register(self)

        Server(bind).register(self)
        JSONSerializer().register(self)

        API().register(self)

    def signal(self, *args):
        raise SystemExit(0)


def parse_args():
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-b", "--bind", action="store", dest="bind", metavar="INT", type=str,
        default=environ.get("BIND", "0.0.0.0:80"),
        help="Interface and Port to Bind to"
    )

    parser.add_argument(
        "-d", "--debug", action="store_true", dest="debug",
        default=environ.get("DEBUG", False),
        help="Enable Debug Mode"
    )

    parser.add_argument(
        "-l", "--logfile", action="store", default=None,
        dest="logfile", metavar="FILE", type=str,
        help="Log file to store logs in"
    )

    parser.add_argument(
        "-u", "--url", action="store", dest="url", metavar="URL", type=str,
        default=environ.get("MQTT_PORT", environ.get("URL", None)),
        help="MQTT URL"
    )

    return parser.parse_args()


def main():
    sys.stdout = os.fdopen(sys.stdout.fileno(), "w", 0)

    args = parse_args()

    logger = setup_logging(args)

    setup_mqtt(args, logger)

    App(args).run()


if __name__ == "__main__":
    main()
