from queue import Queue

class IterableQueue(Queue):
    def __iter__(self):
        while True:
            try:
                yield self.get_nowait()
            except :
                return

class LineBuffer:
    def __init__(self):
        self.current_buffer: String = ""
        self.lines = IterableQueue()

    def append(self, content: str):
        self.current_buffer += content
        if(content.endswith("\n")):
            self.lines.put(self.current_buffer)
            self.current_buffer = ""

    def empty(self):
        return self.lines.empty()

    def get(self):
        for line in self.lines:
            yield line
