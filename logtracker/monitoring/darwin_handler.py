import rumps
from pathlib import Path
from logtracker import const
from itertools import cycle


from logtracker.watcher import LsyncdLogWatcher
from watchdog.observers import Observer

class MacOSMonitorApp(rumps.App):
    def __init__(self, log_file):
        super().__init__("LogMon", icon=const.ICON_IDLE, quit_button=None)
        self.log_file = log_file
        self.menu = ['Quit']
        
        # Animation
        self._anim_timer = rumps.Timer(self._blink_icon, 0.3)
        self._anim_timer.start()
        self._anim_cycle = cycle([const.ICON_IDLE, const.ICON_ACTIVE])
        self._animating = False
        
        # Watchdog
        parent_folder = Path(log_file).parent
        event_handler = LsyncdLogWatcher(log_file=self.log_file, handler=self)
        self.observer = Observer()
        self.observer.schedule(event_handler=event_handler, path=parent_folder, recursive=False)
        self.observer.start()
    
    @rumps.clicked('Quit')
    def quit_app(self, _):
        if self.observer:
            self.observer.stop()
            self.observer.join()
        if self._anim_timer:
            self._anim_timer.stop()
        rumps.quit_application()
            
    def notify(self, line):
        if 'copy_start' in line:
            self.start_animation()
        elif 'copy_end' in line:
            self.stop_animation()
        
    def start_animation(self):
        """Start icon blink"""
        self._animating = True

    def stop_animation(self):
        """Stop icon blink"""
        self._animating = False
        self.icon = const.ICON_IDLE

    def _blink_icon(self, _):
        """Updates icone at each timer tick"""
        if not self._animating:
            return
        self.icon = next(self._anim_cycle)
