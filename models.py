import dataclasses

@dataclasses.dataclass
class MusicItem:
    title: str
    artist: str
    added: dataclasses.field()

@dataclasses.dataclass
class LocalMusicItem(MusicItem):
    path: str

@dataclasses.dataclass
class StreamMusicItem(MusicItem):
    strem_url: str