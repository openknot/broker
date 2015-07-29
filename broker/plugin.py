"""Plugin

Subclass :class:`Plugin` to create broker plugins with standarized CLI Options and API.
"""


from __future__ import print_function


from os import environ
from logging import getLogger
from inspect import getmodule
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser


from circuits import Component, Debugger


from .utils import parse_bind


def parse_args(parse=True, description=None):
    parser = ArgumentParser(
        description=(description or ""),
        formatter_class=ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-b", "--bind", action="store", dest="bind", metavar="INT", type=str,
        default=environ.get("BIND", "0.0.0.0:1338"),
        help="Interface and Port to Bind to"
    )

    parser.add_argument(
        "-d", "--debug", action="store_true", dest="debug",
        default=environ.get("DEBUG", False),
        help="Enable Debug Mode"
    )

    parser.add_argument(
        "-u", "--url", action="store", dest="url", metavar="URL", type=str,
        default=environ.get("URL", environ.get("BROKER_PORT", "udp://127.0.0.1:1338")),
        help="broker Daemon URL"
    )

    return parser.parse_args() if parse else parser


class Plugin(Component):

    def init(self, parse_args_cb=None):
        # Get description from the first line of the plugin's __doc__
        description = getattr(getmodule(self), "__doc__", "")

        # Allow ArgumentsParser to be extended.
        if parse_args_cb is not None:
            self.args = parse_args_cb(parse_args(False, description)).parse_args()
        else:
            self.args = parse_args(description=description)

        self.bind = parse_bind(self.args.bind)
        self.url = parse_bind(self.args.url)

        self.logger = getLogger(__name__)

    def started(self, *args):
        if self.args.debug:
            Debugger().register(self)
