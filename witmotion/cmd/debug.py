import logging

import time
import sys
import argparse

try:
    import coloredlogs
except ImportError:
    coloredlogs = None

from .. import IMU, protocol

log = logging.getLogger(__name__)


def main(argv=sys.argv):
    p = argparse.ArgumentParser(description="Emit IMU output")
    p.add_argument(
        "--path", default="/dev/ttyUSB0", help="Path to serial device"
    )
    p.add_argument(
        "--baudrate", type=int, default=9600, help="Serial baud rate"
    )
    p.add_argument(
        "--vertical",
        action="store_true",
        help="Set installation direction to vertical",
    )
    p.add_argument("--verbose", action="store_true", help="Verbose debugging")
    opts = p.parse_args(argv[1:])

    if coloredlogs:
        coloredlogs.install(level="debug" if opts.verbose else "info")
    else:
        logging.basicConfig(
            level=logging.DEBUG if opts.verbose else logging.INFO
        )

    log.debug("opening IMU at %s baudrate %s", opts.path, opts.baudrate)

    imu = IMU(path=opts.path, baudrate=opts.baudrate)

    def callback(msg):
        log.info("message: %s", msg)

    imu.subscribe(callback)

    # imu.set_installation_direction(horizontal=(not opts.vertical))
    classes = set()
    classes.add(protocol.AngleMessage)
    imu.set_messages_enabled(classes=classes)

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        log.info("exiting")
    finally:
        imu.close()
