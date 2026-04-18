class Song:
    """
    Represent a song with artists, tempo, and chords.
    """

    def __init__(self, name, primary_artists, bpm, chords):
        """
        Initialize a Song object.

        Args:
            name (str): The name of the song.
            primary_artists (list): A list of main artists.
            bpm (int): The tempo of the song in beats per minute.
            chords (list): A list of chords in the song.

        Returns:
            None
        """
        self.name = name
        self.artists = {
            "primary_artist": [],
            "features": []
        }

        for artist in primary_artists:
            self.artists["primary_artist"].append(artist)

        self.bpm = bpm
        self.chords = chords

    def associated_artists(self, other_artists):
        """
        Add a featured artist to the song.

        Args:
            other_artists (str): The name of the featured artist.

        Returns:
            None
        """
        self.artists["features"].append(other_artists)

    def change_beat(self, increase=True, change=5):
        """
        Change the tempo of the song.

        Args:
            increase (bool): If True, increase bpm. If False, decrease bpm.
            change (int): The amount to change the bpm by.

        Returns:
            None
        """
        if increase:
            self.bpm += change
        else:
            self.bpm -= change

    def modulate(self, steps=1):
        """
        Modulate every chord in the song by the given number of steps.

        Args:
            steps (int or float): Number of musical steps to move.

        Returns:
            None
        """
        chromatic_scale = [
            "C", "C#", "D", "D#", "E", "F",
            "F#", "G", "G#", "A", "A#", "B"
        ]

        modulated_chords = []
        half_steps = int(steps * 2)

        for chord in self.chords:
            starting_index = chromatic_scale.index(chord)
            new_index = (starting_index + half_steps) % len(chromatic_scale)
            modulated_chords.append(chromatic_scale[new_index])

        self.chords = modulated_chords

    def info(self):
        """
        Build a string with the song's main information.

        Returns:
            str: A summary of the song's name, artists, chords, and bpm.
        """
        return (
            f"Song: {self.name}\n"
            f"Artists: {self.artists}\n"
            f"Chords: {self.chords}\n"
            f"BPM: {self.bpm}"
        )


if __name__ == "__main__":

    test_song = Song(
        "Doomsday",
        ["MF DOOM"],
        90,
        ["C", "G", "A", "F"]
    )

    test_song.associated_artists("Pebbles The Invisible Girl")
    test_song.change_beat()
    test_song.change_beat(False, 10)
    test_song.modulate(1)
    print(test_song.info())