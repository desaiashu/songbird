# class to abstract midi track to send note data
from songbird.interface.midi import midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

def start_note(note, velocity, channel):
    midi.send(NoteOn(note, velocity), channel)

def end_note(note, channel):
    midi.send(NoteOff(note, 0), channel)
