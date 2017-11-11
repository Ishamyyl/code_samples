#!/usr/bin/env python3

""" Provided a text file with information about artists and songs:
        Joy Division - Love Will Tear Us Apart
        Joy Division - New Dawn Fades
        Pixies - Where Is My Mind
        Pixies - Hey
        Genesis - Mama

    Write the required classes so the following code works:
        music = MusicFile('/Users/ynonperek/music.txt')
        print(music.artist('Joy Division').songs)
"""


from pathlib import Path
from collections import UserDict, UserList, defaultdict


class Artist(UserList):
    """A musical artist is only defined by the songs they make </wax_poetic>"""
    @property
    def songs(self):
        return self.data

class MusicFile(UserDict):
    def __init__(self, music_path):
        UserDict.__init__(self)
        self.data = defaultdict(Artist)
        with Path(music_path).open('r') as f:
            music_list = f.read().splitlines()
        for line in music_list:
            artist, song = line.split('-')
            self.data[artist.strip()].append(song.strip())

    def artist(self, artist):
        return self.data[artist]

def run():
    music = MusicFile('music.txt')
    print(music.artist('Joy Division').songs)

if __name__ == '__main__':
    run()
