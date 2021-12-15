from .display import Display
from .buttons import Buttons

from songbird.composition.basic_composer import BasicComposer

# Display initialization and callback
display = Display("", "")

def transport_step_callback(note):
    display.setLabel2(note)

# Construct basic handler
basic_composer = BasicComposer(transport_step_callback)
display.setLabel1(basic_composer.scale.name())

# Button initialization, handler, and callback
def button_1_callback():
    new = basic_composer.change_scale()
    display.setLabel1(new)

buttons = Buttons(button_1_callback)

def handler():
    buttons.checkClicks()
