class Converter(object):
    @staticmethod
    def Null(_):
        return None

    @staticmethod
    def OnOff127(data):
        x = data[0]
        return {0: 'OFF', 127: 'ON'}.get(x,'???')

    @staticmethod
    def Id1(x):
        return x[0]

    @staticmethod
    def Int16(data):
        return (data[0]&0x7f) + (data[1]&0x7f)*128


class SafeEnum(type):

    def __init__(self, code):
        self.code = code

    def __str__(self):
        return str(list(self.__class__.__dict__.keys())[list(self.__class__.__dict__.values()).index(self.code)])

    @classmethod
    def make(cls,n):
        try:
            return cls(n)
        except:
            return None


class ConversionEnum(SafeEnum):

    def __init__(self,*args):
        self.code=args[0]
        self.converter=args[1] if len(args)>1 else Converter.Id1

    def __call__(self,value):
        return self.converter(value)
