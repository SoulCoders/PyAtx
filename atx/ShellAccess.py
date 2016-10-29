"""
ShellAccess
----------
很多shell可以用telnet,也可以用ssh,所以说接入方式可选。
因此我们可以在初始化时指定接入的类。

"""
import telnetlib


class ShellAccess:
    def __init__(self, newline='\n'):
        self._newline = newline

    def open(self, address):
        pass

    def close(self):
        pass

    def send(self, cmd, exp=None, timeout=5, newline=True):
        pass

    def read(self, exp, timeout=5):
        pass


class TelnetShell(ShellAccess):
    def __init__(self, newline='\n'):
        ShellAccess.__init__(self, newline)
        self._conn = telnetlib.Telnet()

    def open(self, address):
        self._conn.open(*address)
        return True

    def close(self):
        self._conn.close()
        return True

    def send(self, cmd, exp=None, timeout=5, newline=True):
        pass

    def read(self, exp, timeout=5):
        pass


class TcpShell(ShellAccess):
    def __init__(self, newline='\n'):
        ShellAccess.__init__(self, newline)


class SerialShell(ShellAccess):
    def __init__(self, newline='\n'):
        ShellAccess.__init__(self, newline)


class SshShell(ShellAccess):
    def __init__(self, newline='\n'):
        ShellAccess.__init__(self, newline)
