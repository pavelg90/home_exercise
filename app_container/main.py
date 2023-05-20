import os
import time
import pandas as pd
from sqlalchemy import create_engine
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        df = pd.read_csv(event.src_path)
        df.to_sql(os.path.splitext(event.src_path)[0], engine, if_exists='replace')

engine = create_engine('postgresql://admin:admin@db:5432/dbname')
event_handler = Handler()
observer = Observer()
observer.schedule(event_handler, path='/app/data/', recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()
