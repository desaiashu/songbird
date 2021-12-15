import board
import busio
import adafruit_midi

def initialize_midi():
    # Midi code below
    uart = busio.UART(board.TX, board.RX, baudrate=31250, timeout=0.001)  # init UART
    midi = adafruit_midi.MIDI(
        midi_in=uart,
        midi_out=uart,
        out_channel=0,
        debug=False,
    )
    print("Midi output channel:", midi.out_channel + 1)
    return midi

midi = initialize_midi()
