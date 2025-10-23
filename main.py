#!/usr/bin/env python3
from logtracker.monitoring.factory import HandlerFactory
from logtracker.indicator import PystrayMonitorApp

LOG_FILE = "/Users/robin/DEV/lxpanel-logtracker/logs/lsyncd.log"
    
if __name__ == '__main__':
    monitor = PystrayMonitorApp(log_file=LOG_FILE)
    
    monitor.run()
    
    

