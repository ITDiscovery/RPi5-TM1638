import RPi.GPIO as IO
from time import sleep, localtime

Datapin=22

IO.setwarnings(False)
IO.setmode(IO.BCM)
IO.setup(Datapin, IO.OUT)

while True:
    IO.output(Datapin, IO.HIGH)
    sleep(.1)
    IO.output(Datapin, IO.LOW)
    sleep(.1)
