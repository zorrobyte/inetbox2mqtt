# MIT License
#
# Copyright (c) 2023  Dr. Magnus Christ (mc0110)
#
# This is part of the inetbox2mqtt package
# 
# Simulate a persistant args-parameter string
# Usable as generator

import os
import logging


class Args():
    
    __ARGS = "args.dat"
    
    def __init__(self, fn = None):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)
        
        self.__arg = ""
        if fn != None:
            self.fn = fn
        else:
            self.fn = self.__ARGS
        # Check if file exists (handle both root and full paths)
        # MicroPython doesn't have os.path.exists, so use try/except
        file_exists = False
        try:
            # Try to check if file is in root directory
            if self.fn in os.listdir("/"):
                file_exists = True
            # For full paths (like /src/args.dat), try to open it
            elif "/" in self.fn:
                try:
                    with open(self.fn, "r") as f:
                        pass  # File exists if we can open it
                    file_exists = True
                except:
                    file_exists = False
        except:
            file_exists = False
        
        if file_exists:
            self.log.info("args_file found -> loaded")
            self.load()
                       
    def reset(self):
        self.__arg = ""
        try:
            os.remove(self.fn)
        except OSError as e:
            self.log.warning(f"Could not remove {self.fn}: {e}")
        except Exception as e:
            self.log.error(f"Unexpected error removing {self.fn}: {e}")
        
    def load(self):
        # Handle both root files and full paths
        # MicroPython doesn't have os.path.exists, so use try/except
        try:
            with open(self.fn, "r") as f:
                self.__arg = f.read()
                self.log.info(f"file: {self.fn} content: {self.__arg}")
        except OSError as e:
            self.log.warning(f"Could not read {self.fn}: {e}")
            self.__arg = ""
        except Exception as e:
            self.log.error(f"Unexpected error reading {self.fn}: {e}")
            self.__arg = ""
            
    def store(self, s):
        try:
            with open(self.fn, "w") as f:
                f.write(s)
            self.__arg = s
        except OSError as e:
            self.log.warning(f"Could not write {self.fn}: {e}")
        except Exception as e:
            self.log.error(f"Unexpected error writing {self.fn}: {e}")
        
    def check(self, s):
        return s in self.__arg
    
    def get(self):
        a = self.__arg.split()
        while a != []:
            q = a.pop(0)
            yield q
            
    def get_key(self, key):
        for i in self.get():
            q = i.split("=")
            if q[0]==key:
                return q[1]
        return None    
