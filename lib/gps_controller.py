from gps import *
import time
import threading
import math
import sys
import logging

class GpsController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.gpsd = gps(mode=WATCH_ENABLE)  # Starting the stream of info
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            # Grab EACH set of gpsd info to clear the buffer
            self.gpsd.next()

    def stopController(self):
        self.running = False

    @property
    def fix(self):
        return self.gpsd.fix

    @property
    def utc(self):
        return self.gpsd.utc

    @property
    def satellites(self):
        return self.gpsd.satellites

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Create the controller
    gpsc = GpsController()

    try:
        # Start controller
        gpsc.start()

        while True:
            # Print or log GPS information
            logger.debug("Latitude: %s", gpsc.fix.latitude)
            logger.debug("Longitude: %s", gpsc.fix.longitude)
            # ... (other properties)

            time.sleep(0.5)

    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise

    except KeyboardInterrupt:
        logger.info("User cancelled")

    finally:
        logger.info("Stopping GPS controller")
        gpsc.stopController()
        # Wait for the thread to finish
        gpsc.join()

    logger.info("Done")
