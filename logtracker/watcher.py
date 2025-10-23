from watchdog.events import FileSystemEventHandler
import threading

class LsyncdLogWatcher(FileSystemEventHandler):
    def __init__(self, log_file, handler):
        self.log_file = log_file
        self.handler = handler
        self._position = 0

    def on_modified(self, event):
        if event.src_path != self.log_file:
            return

        print('modified')
        
        with open(self.log_file, "r") as f:
            f.seek(self._position)
            new_lines = f.readlines()
            self._position = f.tell()

        for line in new_lines:
            self._process_line(line.strip())

    def _process_line(self, line):
        if not line:
            return
        
        if "Normal: Calling rsync" in line:
            self.handler.notify('copy_start')

        elif "sending incremental file list" in line:
            self.handler.notify('sync_list_start')

        elif "sent" in line and "bytes" in line:
            self.handler.notify('sync_list_end')

        elif "Normal: Finished" in line:
            self.handler.notify('copy_end')