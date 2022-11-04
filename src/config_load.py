'''
This module (...)\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* yaml
'''

# Import system libs
import yaml


#######################################

class OrchestratorConfig:
    ''' Initilize (...) module.\n
    '''

    # --------------------
    def __init__(self, yml_config_path:str):
        self.configpath = yml_config_path
        self.configs = {}
    # --------------------

    # --------------------
    def load(self):
        ''' Read the `yaml` file into `configs` and creates
        the `watchlist` to make the event handling easier.\n
        return `configs` (dict): Parsed `yaml` file.\n
        '''
        # Read file
        with open(self.configpath, 'r') as fstream:
            self.configs = yaml.safe_load(fstream)
        # Check configuration structure
        self._sanity_check()
    
        return(self.configs)
    # --------------------

    # --------------------
    def _sanity_check(self):
        ''' Performs a series of verifications to check the
        validity of the configurations parsed.\n
        '''
        if 'watch_folder' not in self.configs.keys():
            raise LookupError(f"The 'watch_folder' key is not present in '{self.configpath}'.")

        if 'services' not in self.configs.keys():
            raise LookupError(f"The 'services' key is not present in '{self.configpath}'.")
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

