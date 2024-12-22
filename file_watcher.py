import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

LOG_FILE = "/home/ubuntu/bsm/logs/changes.json"
WATCH_DIR = "/home/ubuntu/bsm/test"

class Watcher:
    def __init__(self, directory_to_watch):
        self.directory_to_watch = directory_to_watch
        self.event_handler = ChangeHandler()
        self.observer = Observer()

    def run(self):
        self.observer.schedule(self.event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        log_entry = {
            "event_type": event.event_type,
            "src_path": event.src_path,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        with open(LOG_FILE, "a") as log_file:
            log_file.write(json.dumps(log_entry) + "\n")
        print(f"Logged: {log_entry}")

if __name__ == "__main__":
    watcher = Watcher(WATCH_DIR)
    watcher.run()
