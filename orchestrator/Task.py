from abc import ABC, abstractmethod
import threading, uuid, datetime


class Task(threading.Thread, ABC):
    def __init__(self):
        self.running: bool = False
        self._on_finish_events = []
        self._on_error_events = []
        self._on_start_events = []
        self._id = str(uuid.uuid4())
        self.start_date = datetime.datetime.now()
        self.end_date = None
        self.last_update_date = None
        self._progress = 0
        self.status = "PENDING"
        self.canceled = False
        threading.Thread.__init__(self)

    def id(self):
        return self._id

    def append_on_finish_event(self, callback):
        self._on_finish_events += [callback]

    def append_on_error_event(self, callback):
        self._on_error_events += [callback]

    def append_on_start_event(self, callback):
        self._on_start_events += [callback]

    def start(self):
        super().start()

    def run(self):
        for event in self._on_start_events:
            event()

        self.status = "RUNNING"
        self.running = True
        if self.canceled:
            self.status = "CANCELED"
            for event in self._on_error_events:
                event()
            self.running = False
            self.end_date = datetime.datetime.now()
        else:
            try:
                self.handle()
                self.status = "DONE"
                for event in self._on_finish_events:
                    event()
            except Exception as e:
                print(e)
                self.status = "ERROR"
                for event in self._on_error_events:
                    event()
            finally:
                self.running = False
                self.end_date = datetime.datetime.now()

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
