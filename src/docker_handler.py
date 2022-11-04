'''
This module implements the FileSystemEventHandler
methods to manipulate docker containers on filesystem
events.\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* yaml
* docker
* watchdog
'''

# Import system libs
import os
import yaml
import docker
import logging
from watchdog.events import FileSystemEventHandler

#######################################


class DockerEventHandler(FileSystemEventHandler):

    # --------------------
    def __init__(self, yml_conf_path:str, watch_folder:str, logger=None):
        ''' Check for file-change events and restart the 
        corresponding docker container.
        `yml_conf_path` (str): Path to configuration with
        files to watch and services to restart.\n
        `logger` (logging.Logger): The log instance to print.\n
        '''
        super().__init__()
        # Initialize the logger
        self.logger = logger or logging.root
        
        # Get the configurations
        self.configs = None
        self.watchlist = None
        self.configpath = yml_conf_path
        self.watch_folder = watch_folder
        self._parse_config()
        
        # Get Docker instance
        self.docker_client = docker.from_env()

    # --------------------

    # --------------------
    def _parse_config(self):
        ''' Read the `yaml` file into `configs` and creates
        the `watchlist` to make the event handling easier.\n
        '''
        # Read file
        with open(self.configpath, 'r') as fstream:
            self.configs = yaml.safe_load(fstream)
        
        # Check configuration structure
        self._sanity_check()
        
        # Invert the configuration to a dictionary using files as keys and
        # a list of container names as values
        self.watchlist = {}
        for srv in self.configs['services'].values():
            for f in srv['watch_files']:
                if (not os.path.isabs(f)):
                    # Resolve relative paths starting from watch_folder
                    absf = os.path.realpath( os.path.join(self.watch_folder,f) )
                else:
                    absf = os.path.realpath(f)
                    # Check if file is in watch_folder 
                    if not (absf.startswith(os.path.realpath(self.watch_folder))):
                        self.logger.warn(f"File {f} is outside of {self.watch_folder} and will be ignored.")
                    
                if (absf in self.watchlist.keys()): 
                    self.watchlist[absf] = self.watchlist[absf].append(srv['container_name'])
                else:
                    self.watchlist[absf] = [srv['container_name']]
        
    # --------------------

    # --------------------
    def _sanity_check(self):
        ''' Performs a series of verifications to check the
        validity of the configurations parsed.\n
        '''

        if 'services' not in self.configs.keys():
            raise LookupError(f"The 'services' key is not present in '{self.configpath}' ")
        if type(self.configs['services'])!=dict:
            raise LookupError(f"No services to look at in '{self.configpath}' ")
        if len(self.configs['services'])==0:
            raise LookupError(f"No services to look at in '{self.configpath}' ")
        for k,srv in self.configs['services'].items():
            if 'container_name' not in srv.keys():
                raise LookupError(f"The 'container_name' key is not present in '{k}' service")
            if 'watch_files' not in srv.keys():
                raise LookupError(f"The 'watch_files' key is not present in '{k}' service")
            if type(srv['watch_files'])!=list:
                raise LookupError(f"The 'watch_files' key in '{k}' service must be a list")
                
    # --------------------

    # --------------------
    # NOTE: Implementing the `on_closed` method also does
    # the job but it would only work in Linux systems.
    def on_modified(self, event):
        ''' Triggered once a file is modified.\n
        `event` (FileSystemEvent): Object representing the file system event.\n
        '''
        super().on_modified(event)
        
        # Check for file in configured watchlist
        if (not event.is_directory and event.src_path in self.watchlist.keys()):

            for container_name in self.watchlist[event.src_path]:
                # Seach for configured container in running dockers
                container = None
                try:
                    container = self.docker_client.containers.get(container_name)
                
                # Error handling
                except docker.errors.NotFound:
                    self.logger.error(f"No container named '{container_name}' found. Skipping...")
                except docker.errors.APIError:
                    self.logger.warn(f"Unable to connect to docker server. No actions taken for '{container_name}'.")
                except Exception as ex:
                    self.logger.warn(f"Unable to access container '{container_name}'.")
                    self.logger.error(ex)
                
                if container is not None:
                    # Restarts the requested container
                    try:
                        container.restart(timeout=10)
                        self.logger.info(f"Sending restart signal to '{container_name}'.")
                        # TODO: Check if container trully restarted

                    # Error handling
                    except docker.errors.APIError:
                        self.logger.warn(f"Unable to connect to docker server. No actions taken for '{container_name}'.")
                    except Exception as ex:
                        self.logger.warn(f"Unable to restart '{container_name}'.")
                        self.logger.error(ex)

    # --------------------
