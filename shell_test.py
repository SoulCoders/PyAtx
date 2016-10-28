from atx.Shell import *
import time


# 我伪装成一个真实shell,不管你发什么,我都只返回时间
class ShellSimulator:
    def send(self, cmd=''):
        return time.ctime()


class TelnetAccessShell(ShellAccess):
    """
    我会通过telnet连接ShellSimulator,执行任务
    """
    def __init__(self):
        self.__conn = ShellSimulator()

    def open(self, address):
        print("telnet open at ", address)
        return True

    def close(self):
        print("telnet close")
        return True

    def send(self, cmd, exp_list, timeout):
        print('Telnet send, recv:', self.__conn.send())
        return 0, None, ''


class ComAccessShell(ShellAccess):
    """
    我会通过串口连接ShellSimulator,执行任务
    """
    def __init__(self):
        self.__conn = ShellSimulator()

    def open(self, address):
        print("COM open at ", address)
        return True

    def close(self):
        print("COM close")
        return True

    def send(self, cmd, exp_list, timeout):
        print('COM send, recv:', self.__conn.send())
        return 0, None, ''


class MyShell(Shell):
    """
    我是一个具体的shell
    可以通过继承啦、组合啦合成一个复杂的shell
    """
    def __init__(self, acc=None):
        self._acc = None
        Shell.__init__(self, acc)

    def open(self, address):
        return self._acc.open(address)

    def close(self):
        return self._acc.close()

    def send(self, cmd, exp_list=None, timeout=5):
        return self._acc.send(cmd, exp_list, timeout)

    # 可以在这里面实现更多功能
    # .......


class MyShellBuilder(ShellTypeBuilder):
    def build(self, ac):
        sh = MyShell(ac)
        return sh


ShellCreator.add('myshell', MyShellBuilder)

mysh = ShellCreator.create('myshell', TelnetAccessShell)
mysh.open(('127.0.0.1', 1000))
mysh.send('abc')
mysh.close()

mysh = ShellCreator.create('myshell', ComAccessShell)
mysh.open(('COM1', 9600))
mysh.send('abc')
mysh.close()
