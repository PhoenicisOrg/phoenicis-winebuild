from abc import ABC, abstractmethod
import threading, uuid, datetime

class Task(threading.Thread, ABC):
    def __init__(self):
        self.running: bool = False
        self._on_finish_events = []
        self._id = str(uuid.uuid4())
        self.start_date = datetime.datetime.now()
        self.end_date = None
        self.last_update_date = None
        self._progress = 0
        threading.Thread.__init__(self)

    def id(self):
        return self._id

    def append_on_finish_event(self, callback):
        self._on_finish_events += [callback]

    def start(self):
        self.running = True
        super().start()

    def run(self):
        self.handle()
        self.running = False
        self.end_date = datetime.datetime.now()
        for event in self._on_finish_events:
            event()

    def type(self):
        return self.__class__.__name__

    """
        The argument the task (exemple: the environement name, the build information, etc...)
    """
    @abstractmethod
    def argument(self):
        pass

    """
        The handler
    """
    @abstractmethod
    def handle(self):
        pass

    """
        The description of what the task do
    """
    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def get_message(self) -> str:
        pass

    @abstractmethod
    def get_progress(self) -> int:
        pass

    @abstractmethod
    def set_progress(self, progress: int):
        pass
