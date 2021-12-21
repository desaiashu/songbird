from .util import SafeEnum, ConversionEnum, Converter
from .base import MIDIParserError
import re

def Pedals(data):
    x = data[0]
    onOff = 'OFF' if x<64 else 'ON'
    return f' {onOff} ({x})'


class ControlMessages(ConversionEnum):

    Data_Entry_MSB = 6
    Channel_Volume = 7
    Pan = 10
    Data_Entry_LSB = 38
    Damper_Pedal = (64,Pedals)
    RPN_LSB = 100
    RPN_MSB = 101
    All_Sound_Off = (120,Converter.Null)
    Reset_All_Controllers = (121,Converter.Null)
    Local_Control = (122,Converter.OnOff127)
    All_Notes_Off = (123,Converter.Null)
    Omni_Mode_Off = (124,Converter.Null)
    Omni_Mode_On = (125,Converter.Null)
    Mono_Mode_On = 126
    Poly_Mode_On = (127,Converter.Null)


class ControlMessage(object):

    def __init__(self,data=b''):

        command=ControlMessages.make(data[0])
        if command:
            self.command=command
            self.value=command(data[1:])
        else:
            self.command=data[0]
            self.value=data[1:]

    def __str__(self):
        if self.value is not None:
            return f'{str(self.command)} := {self.value}'
        else:
            return str(self.command)

    def __len__(self):
        return 2

class TimeCodeMessages(SafeEnum):

    Frame_Number_LSB = 0x00
    Frame_Number_MSB = 0x10
    Second_LSB = 0x20
    Second_MSB = 0x30
    Minute_LSB = 0x40
    Minute_MSB = 0x50
    Hour_LSB = 0x60
    Rate_And_Hour_MSB = 0x70

def TimeCode(data):
    x = data[0]
    kind = TimeCodeMessages(x&0x70)
    return f'Type: {str(kind)} value: {x&15}'


class SystemMessages(ConversionEnum):

    Exclusive = 0
    Time_Code_Quarter_Frame = (1,TimeCode)
    Song_Position_Pointer = (2,Converter.Int16)
    Song_Select = 3
    Tune_Request = (6,Converter.Null)
    End_Of_Exclusive = (7,Converter.Null)
    RT_Timing_Clock = (8,Converter.Null)
    RT_Start = (10,Converter.Null)
    RT_Continue = (11,Converter.Null)
    RT_Stop = (12,Converter.Null)
    RT_Active_Sensing = (14,Converter.Null)
    RT_Reset = (15,Converter.Null)

    def length(self):
        cls=self.__class__
        if self.code == cls.Exclusive:
            return None
        elif self.code in [cls.Time_Code_Quarter_Frame,cls.Song_Select]:
            return 1
        elif self.code == cls.Song_Position_Pointer:
            return 2
        else:
            return 0

class SystemMessage(object):

    def __init__(self,data=b''):

        command=SystemMessages.make(data[0]&15)
        if command:
            self.command=command
            self.value=command(data[1:])
            self.length=command.length or 0
        else:
            self.command=data[0]
            self.value=data[1:]
            self.length=len(data)-1

    def __len__(self):
        return self.length

    def __str__(self):
        if self.value is not None:
            return f'{str(self.command)} := {self.value}'
        else:
            return str(self.command)


class Note(object):

    notes=['c','c#','d','d#','e','f','f#','g','g#','a','a#','b']

    def _fromNumber(self,n):
        number=n&0xff
        self.note=self.notes[number % 12]
        self.octave=number//12

    def _fromString(self,s):
        match=re.fullmatch('([a-g]{1}[\#]?)([\d]{1,2})',s,flags=re.RegexFlag.IGNORECASE)
        if not match:
            raise MIDIParserError(f'Invalid note label {s}')
        n, o = match.groups()
        self.note=self.notes.index(n.lower())
        self.octave=int(o)

    def _fromPitchAndOctave(self,pitch,octave):
        if pitch<0 or octave<0:
            raise MIDIParserError('pitch and octave must be non-negative')
        self.note=int(pitch)%12
        self.octave=octave

    def __init__(self,*args,**kwargs):
        if len(args)>0:
            arg=args[0]
            if type(arg)==int:
                self._fromNumber(arg)
            elif type(arg)==str:
                self._fromString(arg)
            else:
                raise MIDIParserError(f'Cannot parse note string {arg}')
        elif 'pitch' in kwargs and 'octave' in kwargs:
            self._fromPitchAndOctave(kwargs['pitch'],kwargs['octave'])
        else:
            raise MIDIParserError('illegal arguments for MIDI Note')

    @property
    def number(self):
        return self.notes.index(self.note.lower())+self.octave*12

    def __str__(self):
        return f'{self.note.upper()}{self.octave}'

class NoteMessage(object):

    def __init__(self,onOff,data=b''):
        self.onOff='ON' if onOff else 'OFF'
        self.note=Note(data[0])
        self.velocity=data[1]

    def __str__(self):
        return f'{self.note} {self.onOff} velocity := {self.velocity}'

    def __len__(self):
        return 2

class PressureMessage(object):

    def __init__(self,data=b''):
        self.note=Note(data[0])
        self.pressure=data[1]

    def __str__(self):
        return f'{self.note} pressure := {self.pressure}'

    def __len__(self):
        return 2


class SimpleMessage(object):

    def compute(self,data):
        return data[0]


    def __init__(self,name,data=b''):
        self.name=name
        self.value=self.compute(data)

    def __str__(self):
        return f'{self.name} := {self.value}'

    def __len__(self):
        return 1


class ProgramMessage(SimpleMessage):

    def __init__(self,data=b''):
        super().__init__('Program',data)

class ChannelPressureMessage(SimpleMessage):

    def __init__(self,data=b''):
        super().__init__('Pressure',data)

class PitchBendMessage(SimpleMessage):

    def compute(self, data):
        return Converter.Int16(data)-8192

    def __init__(self,data=b''):
        super().__init__('Bend',data)

    def __len__(self):
        return 2
