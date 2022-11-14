'''
This module contains functions to manipulate
the observer thread from watchdog.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* watchdog
'''

# Import system libs
import os
import logging
from watchdog.observers import Observer
# NOTE: using the `Observer` class instead of `PollingObserver`
# causes the modified event to be triggered more that one time 
# in a row. This may have undesired consequences, so 
# https://github.com/gorakhargosh/watchdog/issues/93 suggests the
# use of `PollingObserver` to bypass this issue.
# XXX: Unfortunatly using `PoolingObserver` was does not seems to
# work correctly in ARM processors.

# Import custom libs
from docker_handler import DockerEventHandler

#######################################


# --------------------
def observer_launch(observer:Observer=None):
    ''' Launch or Restart an observer thread.\n
    `observer` (PollingObserver): Existing thread instance to
    restart or set `None` to create a new one.\n
    '''

    # Enviroment variables
    CONF_PATH = os.getenv('CONF_PATH', default='/home/config/monitoring.yml')
    WATCH_FOLDER = os.getenv('WATCH_FOLDER', default='/home/config')
    
    # Check for exising instance
    if observer is not None:
        if observer.is_alive():
            # Do nothing if thread is still working
            return(observer)
        else:
            # Prepare for restart
            observer.join()
            observer = None
            logging.root.info(f'Thread killed. Restarting...')

    # Instance our docker handler
    event_handler = DockerEventHandler(CONF_PATH,WATCH_FOLDER)
    logging.root.info(f"Configuration file '{CONF_PATH}' loaded.")

    # Initialize the observer
    observer = Observer()
    observer.schedule(event_handler, os.path.realpath(WATCH_FOLDER), recursive=False)
    # Lauch threads
    observer.start()
    logging.root.info(f'Orchestrator is Up and Running.')
    logging.root.info(f"Watching '{os.path.realpath(WATCH_FOLDER)}'' for changes.")

    return(observer)
# --------------------
