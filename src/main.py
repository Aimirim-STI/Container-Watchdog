'''
This module contains the orchestrator
program \n
Copyright (c) 2017 Aimirim STI.\n
'''

# Import system libs
import time
import signal
import logging

# Import custom libs
from observer_thread import observer_launch

#######################################

# Log initialize
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

observer = observer_launch(None)

# Bind signals to observer stop
signal.signal(signal.SIGINT, observer.stop)
signal.signal(signal.SIGTERM, observer.stop)

# Keep the program running
try:
    while True:
        observer = observer_launch(observer)
        time.sleep(1)

# Gracefully end
except KeyboardInterrupt:
    observer.stop()

# Join threads to finish
observer.join()