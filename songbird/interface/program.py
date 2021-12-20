from .display import Display
from .buttons import Buttons

# from songbird.composition.basic_composer import BasicComposer
from songbird.composition.file_composer import FileComposer

# Display initialization and callback
display = Display("", "")

def transport_step_callback(note):
    display.setLabel2(note)

# Construct basic handler
file_composer = FileComposer('midifiles/Groove Monkee/Electronic/Downtempo/069 Downtempo 01 8-Bar Fill.mid', transport_step_callback)
display.setLabel1(file_composer.scale.name())

# Button initialization, handler, and callback
def button_1_callback():
    new = file_composer.change_scale()
    display.setLabel1(new)

buttons = Buttons(button_1_callback)

def handler():
    buttons.checkClicks()
