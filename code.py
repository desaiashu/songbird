import time
import songbird.interface.program as program
from songbird.clock.clock import clock

# Run loop
while True:
    program.handler()
    clock.handler()
