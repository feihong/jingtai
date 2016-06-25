from concurrent.futures import ThreadPoolExecutor

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .server import send


observer = None


def start_watcher(watch_list):
    global observer
    watcher = Watcher()
    observer = Observer()
    for path in watch_list:
        observer.schedule(watcher, str(path), recursive=True)
    observer.start()


class Watcher(FileSystemEventHandler):
    def dispatch(self, evt):
        if not evt.is_directory:
            print('%s: %s' % (evt.event_type, evt.src_path))
            send('reload')

    def stop(self):
        observer.join()
