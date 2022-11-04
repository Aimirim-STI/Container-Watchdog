'''
This module contains the orchestrator
program \n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* watchdog
'''

# Import system libs
import os
import time
import logging
from watchdog.observers.polling import PollingObserver
# NOTE: using the `Observer` class instead of `PollingObserver`
# causes the modified event to be triggered more that one time 
# in a row. This may have undesired consequences, so 
# https://github.com/gorakhargosh/watchdog/issues/93 suggests the
# use of `PollingObserver` to bypass this issue.

# Import custom libs
from docker_handler import DockerEventHandler

#######################################

# Log initialize
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# Enviroment variables
CONF_PATH = os.getenv('CONF_PATH', default='/home/config/monitoring.yml')
WATCH_FOLDER = os.getenv('WATCH_FOLDER', default='/home/config')

# Instance our docker handler
event_handler = DockerEventHandler(CONF_PATH,WATCH_FOLDER)
logging.root.info(f"Configuration file '{CONF_PATH}' loaded.")

# Initialize the observer
observer = PollingObserver()
observer.schedule(event_handler, os.path.realpath(WATCH_FOLDER), recursive=False)
# Lauch threads
observer.start()

# Keep the program running
try:
    logging.root.info(f'Orchestrator is Up and Running.')
    logging.root.info(f"Watching '{os.path.realpath(WATCH_FOLDER)}'' for changes.")
    while True:
        time.sleep(1)
        # TODO: Implement a sort of restart to the observer thread,
        # so it will never die

# Gracefully end
except KeyboardInterrupt:
    observer.stop()

# Join threads to finish
observer.join()