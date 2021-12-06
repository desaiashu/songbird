import board
import busio
import adafruit_midi

def initialize_midi():
    # Midi code below
    uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)  # init UART
    midi_in_channel = 2
    midi_out_channel = 2
    midi = adafruit_midi.MIDI(
        midi_in=uart,
        midi_out=uart,
        in_channel=(midi_in_channel - 1),
        out_channel=(midi_out_channel - 1),
        debug=False,
    )
    note_hold = 0.85
    rest = note_hold / 5

    print("Midi output channel:", midi.out_channel + 1)
    return midi
