# Songbird

Songbird is a midi device built to aid live electronic performance

Hardware:
- Feather S2
- Featherwing OLED screen
- Featherwing MIDI i/o

Software:
- Circuitpython
- Midi lib
- OLED lib
- Custom music lib


## Software architecture:

Songbird has two core libraries:

1. Songbird Music:
This library codifies base building blocks of music theory. Notes build to scales to chords to chord progressions. Time signatures, rythyms, and chord progressions build to tracks. Tracks build to songs.

2. Songbird Interface:
This library creates the user interface of a songbird. Different songbirds will run different programs, controlled and viewed using the buttons and display.


## Todos:

Music lib:
- Song
- Track (midi channel, style)
- Scale (root, mode)
- Chord (triad, 7th, voicing)
- Chord progressions (classical, jazz)
- Rythym (bass / melody)
- Time signature

Interface lib:
- Program
- Display
- Buttons
