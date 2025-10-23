#!/usr/bin/env python3
import os
from pathlib import Path
import time

from logtracker.monitoring.factory import HandlerFactory

LOG_FILE = "/Users/robin/DEV/lxpanel-logtracker/logs/lsyncd.log"

# def get_log_activity(callback=None):
#     event_handler = LsyncdLogWatcher(LOG_FILE, callback)
#     observer = Observer()
#     observer.schedule(event_handler, path=LOG_FILE.rsplit("/", 1)[0], recursive=False)
#     observer.start()

#     print(f"Monitoring {LOG_FILE}... (Ctrl+C to stop)")
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
    
if __name__ == '__main__':
    handler = HandlerFactory.create(LOG_FILE)
    handler.run()
    
    # event_handler = LsyncdLogWatcher(LOG_FILE, handler=handler)
    # observer = Observer()
    # observer.schedule(event_handler, path=LOG_FILE.rsplit("/", 1)[0], recursive=False)
    # observer.start()
    
    # print('coucou')

    # print(f"Monitoring {LOG_FILE}... (Ctrl+C to stop)")
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    # observer.join()
    
    

