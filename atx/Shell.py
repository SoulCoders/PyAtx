"""
Shell
-----

众生万象,皆有规律可循,神一般的我发现了其中的规律,开始指手画脚。
我就像个产品狗,我不动手实践,我就瞎BB。

Builder使用组合方式还是类继承由设计者决定。这里只是提供了一个解决方案,并没有提供具体功能。


总要一个例子来说明下
-----------------
from atx.Shell import *
import time


# 我伪装成一个真实shell,不管你发什么,我都只返回时间
class ShellSimulator:
    def send(self, cmd=''):
        return time.ctime()


# 通过telnet接入shell
class TelnetAccessShell(ShellAccess):
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


# 通过COM接入shell
class ComAccessShell(ShellAccess):
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


# 一个可用的shell,真实环境中可能需要继承或组合
class MyShell(Shell):
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

上述脚本会产生以下输出:
telnet open at  ('127.0.0.1', 1000)
Telnet send, recv: Fri Oct 28 19:38:22 2016
telnet close
COM open at  ('COM1', 9600)
COM send, recv: Fri Oct 28 19:38:22 2016
COM close

关于
-----
Author: tkorays<tkorays@hotmail.com>

"""


class ShellAccess:
    """
    吾乃Shell之眼
    """
    def open(self, address):
        return False

    def close(self):
        return False

    def send(self, cmd, exp_list, timeout):
        return -1, None, ''


class Shell:
    """
    出生的时候,我懵懂无知,什么都不懂,父辈们细心地教会我一切;
    待我及笄,你看到的将是新的我。
    """
    def __init__(self, acc=None):
        if isinstance(acc(), ShellAccess):
            self._acc = acc()


class ShellTypeBuilder:
    """
    我自己也啥都不干,我的子孙沿着我走过的轨迹探索未知;
    """
    def build(self, ac):
        return None


class ShellCreator:
    """
    我创造一切,统治万物,我就是权威;
    我的话很少,但是做的事情可不简单;
    我手中的权杖让你不得不服从我的规则,不服从我就无法从我这获得什么.
    """
    __shells = []

    # 我说,要有鲍鱼,厨师就端上来了
    @staticmethod
    def create(name, ac):
        for sh in ShellCreator.__shells:
            if sh[0] == name:
                return sh[1]().build(ac)
        return ShellTypeBuilder().build(ac)

    # 我喜欢不断地请厨师为我烹饪美食
    @staticmethod
    def add(name, builder_class):
        if not isinstance(builder_class(), ShellTypeBuilder):
            return False
        for sh in ShellCreator.__shells:
            if sh[0] == name:
                return True
        ShellCreator.__shells.append((name, builder_class))
        return True

    @staticmethod
    def list():
        return ShellCreator.__shells
