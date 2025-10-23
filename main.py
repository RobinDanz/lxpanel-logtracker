#!/usr/bin/env python3
from logtracker.monitoring.factory import HandlerFactory

LOG_FILE = "/Users/robin/DEV/lxpanel-logtracker/logs/lsyncd.log"
    
if __name__ == '__main__':
    handler = HandlerFactory.create(LOG_FILE)
    handler.run()
    
    

