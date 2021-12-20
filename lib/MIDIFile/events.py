from collections import OrderedDict
from .base import Base
from .messages import NoteMessage, PressureMessage, ControlMessage, ProgramMessage, ChannelPressureMessage, PitchBendMessage, SystemMessage
from .util import SafeEnum

class Event(Base):

    def __init__(self,time,buffer):
        super().__init__(buffer[1:])
        self.time=time
        self.header=buffer[0]
        self.length=0
        self.data=b''
        self.parameters=OrderedDict()

    def __len__(self):
        return self.length

    def __str__(self):
        return self.data

    def __getattr__(self,key):
        return self.parameters[key]


class MetaEventKinds(SafeEnum):

    Sequence_Number = 0
    Text = 1
    Copyright_Notice = 2
    Track_Name = 3
    Instrument_Name = 4
    Lyric = 5
    Marker = 6
    Cue_Point = 7
    MIDI_Channel_Prefix = 0x20
    End_Of_Track = 0x2f
    Set_Tempo = 0x51
    SMTPE_Offset = 0x54
    Time_Signature = 0x58
    Key_Signature = 0x59
    Sequencer_Specific = 0x7f

    def key(self,n):
        if n>=0:
            return ['C','G','D','A','E','B','F#','C#'][n]
        else:
            return ['C','F','Bb','Eb','Ab','Db','Gb','Cb'][-n]

    def attributes(self,_bytes=b''):
        cls=self.__class__
        if self.code in [cls.Text,cls.Copyright_Notice,cls.Track_Name,cls.Instrument_Name,cls.Lyric,cls.Marker,cls.Cue_Point]:
            return OrderedDict(text = _bytes)
        elif self.code==cls.Sequence_Number:
            return OrderedDict(number = Event.build(_bytes[:2]))
        elif self.code==cls.MIDI_Channel_Prefix:
            return OrderedDict(channel = _bytes[0]&0x0f)
        elif self.code==cls.End_Of_Track:
            return OrderedDict()
        elif self.code==cls.Set_Tempo:
            return OrderedDict(tempo = Event.build(_bytes[:3])*120/500000)
        elif self.code==cls.SMTPE_Offset:
            return OrderedDict(hh=_bytes[0],mm=_bytes[1],ss=_bytes[2],frame=_bytes[3]+0.01*_bytes[4])
        elif self.code==cls.Time_Signature:
            return OrderedDict(numerator=_bytes[0],denominator=(1<<_bytes[1]),clocksPerTick=_bytes[2],demisemiquaverPer24Clocks=_bytes[3])
        elif self.code==cls.Key_Signature:
            mode = { 0 : 'major', 1 : 'minor' }[_bytes[1]]
            return OrderedDict(key=self.key(_bytes[0]),mode=mode)
        elif self.code==cls.Sequencer_Specific:
            return OrderedDict(data=_bytes)
        else:
            return OrderedDict()


class MetaEvent(Event):

    def __init__(self,time,buffer):
        super().__init__(time, buffer)
        self.type=self.getInt(1)
        length, n=self.getVarLengthInt()
        self.data=self.getChunk(length)
        self.length=length+n+2

        self.message = MetaEventKinds.make(self.type)
        if self.message:
            self.attributes = self.message.attributes(self.data)


    def __str__(self):
        if self.message:
            attrs = self.stringify([f'{k}={v}' for k,v in self.attributes.items()])
            return f'META@{self.time} {self.message} -> {attrs}'
        else:
            data = self.stringify(self.data)
            return f'META@{self.time} {self.type} -> {data}'


class MIDIEvent(Event):

    commands = {
        0x80: 'NOTE_OFF',
        0x90: 'NOTE_ON',
        0xa0: 'PRESSURE',
        0xb0: 'CONTROL_CHANGE',
        0xc0: 'PROGRAM_CHANGE',
        0xd0: 'CHANNEL_PRESSURE',
        0xe0: 'PITCH_BEND'
    }

    def __init__(self,time,buffer):
        super().__init__(time, buffer)
        self.channel=self.header & 0x0f
        self.command=self.header & 0xf0

        if self.command in [0x80,0x90]:
            self.message=NoteMessage(self.command==0x90,self.buffer)
        elif self.command==0xa0:
            self.message=PressureMessage(self.buffer)
        elif self.command==0xb0:
            self.message=ControlMessage(self.buffer)
        elif self.command==0xc0:
            self.message=ProgramMessage(self.buffer)
        elif self.command==0xd0:
            self.message=ChannelPressureMessage(self.buffer)
        elif self.command==0xe0:
            self.message=PitchBendMessage(self.buffer)
        elif self.command==0xf0:
            self.message=SystemMessage(self.buffer)
        else:
            self.message=''
        length = len(self.message) if self.message else 0
        self.data=self.buffer[:length]
        self.length=length+1

    def __str__(self):
        command = self.commands.get(self.command, None)
        if command:
            return f'MIDI@{self.time} {command}[{self.channel}] {self.message}'
        else:
            data = self.stringify(self.data)
            return f'MIDI@{self.time} {self.command}[{self.channel}] {data}'


class SysExEvent(Event):

    def __init__(self,time,buffer):
        super().__init__(time, buffer)
        self.type=self.header & 0x0f

        length, n=self.getVarLengthInt()
        self.data=self.buffer[:length]
        self.length=length+n+1

    def __str__(self):
        return f'SYSEX@{self.time} {self.type} {self.data} length = {self.length}'
