"""
Xb
----------

牛逼的二进制序列化工具,写出这么牛逼的代码,我都佩服我自己

例子
-----
@binaryobject
class AAA:
    a = Type.i32()
    b = Type.i32()
    c = Type.str(13)
    d = Type.i32()
    e = Type.str(6)
    f = Type.i32(1)
    g = Type.i32()

    def __init__(self):
        pass


a = AAA()
# st = struct.pack(a.unpack_str, 33, 13, "www.baidu.com".encode('ascii'), 6, "aas".encode('ascii'), 0, 0)
# a.decode(st)
a.b = 0xABCD
print(a)
print(a.encode())


关于
-----
Author: tkorays<tkorays@hotmail.com>
"""
import struct


class Type:

    def __init__(self, name, count=0, default=None):
        self.name = name
        self.count = count
        self.value = default

    def __str__(self):
        return "{}({})".format(self.name, self.value)

    @staticmethod
    def bit(count):
        return Type('bit', 0, count)

    @staticmethod
    def char(count=1):
        return Type('char', count, 0)

    @staticmethod
    def uchar(count=1):
        return Type('uchar', count, 0)

    @staticmethod
    def i16(count=1):
        return Type('i16', count, 0)

    @staticmethod
    def ui16(count=1):
        return Type('ui16', count, 0)

    @staticmethod
    def i32(count=1):
        return Type('i32', count, 0)

    @staticmethod
    def ui32(count=1):
        return Type('ui32', count, 0)

    @staticmethod
    def i64(count=1):
        return Type('i64', count, 0)

    @staticmethod
    def ui64(count=1):
        return Type('ui64', count, 0)

    @staticmethod
    def str(count=1):
        return Type('str', count, b"")



def binaryobject(aClass):
    class Wrapper:
        def __init__(self, *args, **kargs):
            self.__dict__['wrapped'] = aClass(*args, **kargs)
            super(aClass, self.wrapped).__init__()
            self.wrapped.types = {}
            for t in [v for v in aClass.__dict__ if isinstance(aClass.__dict__[v], Type)]:
                self.wrapped.types[t] = aClass.__dict__[t]
            for t in [v for v in self.wrapped.__dict__ if
                      isinstance(self.wrapped.__dict__[v], Type)]:
                self.wrapped.types[t] = self.wrapped.__dict__[t]

            self.wrapped.unpack_str = ""
            _tmp = {
                'char': 'c',
                'uchar': 'b',
                'i16': 'h',
                'ui16': 'H',
                'i32': 'i',
                'ui32': 'I',
                'i64': 'l',
                'ui64': 'L',
                'str': 's'
            }
            for k, v in self.wrapped.types.items():
                self.wrapped.unpack_str += "{}{}".format(v.count, _tmp[v.name])

        def __getattr__(self, attr_name):
            return getattr(self.wrapped, attr_name)

        def __setattr__(self, key, value):
            if isinstance(self.wrapped.types[key], Type):
                self.wrapped.types[key].value = value
            else:
                setattr(self.wrapped, key, value)

        def encode(self):
            v = [x.value.encode('utf-8') if x.name == 'str' and x.value else x.value for x in self.wrapped.types.values()]
            return struct.pack(self.wrapped.unpack_str, *v)

        def decode(self, bindata):
            allval = struct.unpack(self.wrapped.unpack_str, bindata)
            if len(allval) < len(self.wrapped.types):
                return
            i = 0
            for k, v in self.wrapped.types.items():
                v.value = allval[i].decode('utf-8') if v.name == 'str' else allval[i]
                self.wrapped.__dict__[k] = v
                i += 1

        def __str__(self):
            s = "{}\n{{\n".format(type(self.wrapped))
            for k, v in self.wrapped.types.items():
                s += "    {} = {}\n".format(k, v.value)
            s += "};"
            return s

        def __repr__(self):
            return self.__str__()

    return Wrapper

