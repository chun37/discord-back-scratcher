import queue
import dataclasses
from typing import Any

@dataclasses.dataclass
class MusicQueue:
    json: list = dataclasses.field(default_factory=list)
    queue: Any = queue.Queue()

    def _put(self, item):
        self.queue.put(item)
        self.json.append(item)
        return

    def _list(self):
        return self.json

    def _get(self):
        if self.json is False:
            return
        item = self.queue.get_nowait()
        self.json.remove(item)
        return item

@dataclasses.dataclass
class MusicItem:
    title: str
    added: dataclasses.field()

@dataclasses.dataclass
class LocalMusicItem(MusicItem):
    path: str

@dataclasses.dataclass
class StreamMusicItem(MusicItem):
    strem_url: str