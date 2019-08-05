import os
import re
import glob
import sqlite3
import functools

import mutagen
import dotenv

dotenv.load_dotenv()

MUSIC_FILE_EXTENTIONS = [
    "m4a",
]

MUSIC_FILE_DIRECTORY = [
    "./music/",
]

ITUNES_MUSIC_DIRECTORY = [
    # "C:/Users/chun/Music/iTunes/iTunes Media/Music/"
]

ITUNES_MUSIC_DIRECTORY += os.getenv("ITUNES_PATH").split(",")

DB_NAME = os.getenv("MUSIC_DB")

META_DATA = {
    "m4a": {"title": "\xa9nam", "artist": "\xa9ART"}
}

TRACK_PATTERN = re.compile(r"[^\d+\s].+(?=\.)")


def get_file_extention(path: str) -> str:
    return os.path.splitext(path)[1][1:].lower()


def is_music_file(path: str) -> bool:
    ext = get_file_extention(path)
    if ext in MUSIC_FILE_EXTENTIONS:
        return True
    return False


def get_normalized_data(path: str, is_itunes: bool) -> tuple:
    tags = mutagen.File(path).tags
    ext = get_file_extention(path)
    directory, filename = os.path.split(path)
    meta = META_DATA[ext]
    try:
        title = tags[meta["title"]]
    except KeyError:
        title = TRACK_PATTERN.findall(filename)
    try:
        artist = tags[meta["artist"]]
    except KeyError:
        if is_itunes:
            artist = directory.split("\\")[-2]
        else:
            artist = None
    finally:
        artist = None if artist is None else artist[0]
    path = path.replace("\\", "/")
    return (title[0], artist, path)


def get_itunes_music_data(directory: str) -> list:
    all_files = glob.glob(directory + "**", recursive=True)
    music_files = filter(is_music_file, all_files)
    return list(map(
        functools.partial(get_normalized_data, is_itunes=True),
        list(music_files)))


def get_music_data(directory: str) -> list:
    all_files = glob.glob(directory + "**", recursive=True)
    music_files = filter(is_music_file, all_files)
    return list(map(
        functools.partial(get_normalized_data, is_itunes=False),
        list(music_files)))


def main():
    con = sqlite3.connect(DB_NAME)
    cur = con.cursor()

    cur.executescript("""
    drop table if exists local_music;
    create table local_music(id integer primary key, title text, artist text, path text);
    """)

    music_data = []

    if ITUNES_MUSIC_DIRECTORY != []:
        for directory in ITUNES_MUSIC_DIRECTORY:
            music_data += get_itunes_music_data(directory)
    if MUSIC_FILE_DIRECTORY != []:
        for directory in MUSIC_FILE_DIRECTORY:
            music_data += get_music_data(directory)
    insert_sql = 'insert into local_music(title, artist, path) values (?, ?, ?)'
    cur.executemany(insert_sql, music_data)
    con.commit()
    con.close()


if __name__ == "__main__":
    main()
