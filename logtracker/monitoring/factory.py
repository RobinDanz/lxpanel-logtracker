import platform
import importlib

class HandlerFactory:
    CLASS_MAP = {
        'darwin': 'logtracker.monitoring.darwin_handler.MacOSHandler',
        'linux': 'logtracker.monitoring.linux_handler.LinuxLogMonitorApp'
    }
    
    @classmethod
    def create(cls, log_file):
        system = platform.system().lower()
        module_path, class_name = cls.CLASS_MAP[system].rsplit(".", 1)
        
        module = importlib.import_module(module_path)
        
        return getattr(module, class_name)(log_file=log_file)
        
        
        
        
        