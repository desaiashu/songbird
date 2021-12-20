import time
import songbird.interface.program as program
import songbird.clock.clock as clock
import gc

# Run loop
while True:
    program.handler()
    clock.handler()
    time.sleep(0.005)
