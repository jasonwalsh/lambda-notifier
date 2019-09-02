import logging

from time import sleep


class Retry:

    def __init__(self, interval=10, max_retries=3):
        self.interval = interval
        self.max_retries = max_retries

        # For internal use only
        self.retries = 0
        self.errors = 0

    def __call__(self, action):
        while True:
            try:
                return action()
            except Exception as e:
                logging.error(e)
                self.errors += 1
            if self.retries >= self.max_retries:
                return
            sleep(self.interval)
            self.retries += 1
