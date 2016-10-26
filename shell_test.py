from atx.Shell import *
import time


# 我伪装成一个真实shell,不管你发什么,我都只返回时间
class ShellSimulator:
    def send(self, cmd=''):
        return time.ctime()


# 我只会实现shell的一部分功能
class ShellPart1(Shell):
    def open(self, address):
        print('send open: ', self.conn.send('open'))
        return True

    def close(self):
        print('send close: ', self.conn.send('close'))
        return True


class ShellPart2(Shell):
    def login(self, user):
        print('send login:', self.conn.send('login'))
        return True

    def logout(self):
        print('send logout: ', self.conn.send('logout'))
        return True


class ShellPart2Dev1(Shell):
    def login(self, user):
        print('send login(dev1):', self.conn.send('login'))
        return True

    def logout(self):
        print('send logout(dev1): ', self.conn.send('logout'))
        return True


# 我是ShellSimulator的替身,是它在程序中的呈现
class SMBuilder(ShellTypeBuilder):
    def build(self):
        class MyShell(ShellPart1, ShellPart2):
            def __init__(self):
                # 父类和子类共有的变量需要可见
                self.conn = ShellSimulator()
                ShellPart1.__init__(self)
                ShellPart2.__init__(self)

        return MyShell()


class SMBuilderDev1(ShellTypeBuilder):
    def build(self):
        class MyShell(ShellPart1, ShellPart2Dev1):
            def __init__(self):
                self.conn = ShellSimulator()
                ShellPart1.__init__(self)
                ShellPart2Dev1.__init__(self)
        return MyShell()


"""
好吧,我想我应该来说明下,这样写有什么意义!
我们试想这样一些场景:
1) 自动化中,需要连接各式各样设备,所以需要有一个工厂统一管理shell对象生产
2) 对于同一类设备,shell间可能存在差别,如果一个类能搞定更好,但是通常,我们引入builder来帮我们构建

所以,如果你要使用一个shell,首先需要定义好shell功能,再由builder构建,最后由Creator交给你。
"""
ShellCreator.add('dev0', SMBuilder)
ShellCreator.add('dev1', SMBuilderDev1)

sh = ShellCreator.create('dev0')
sh.open('b')
sh.login('b')
sh.logout()
sh.close()

sh = ShellCreator.create('dev1')
sh.open('b')
sh.login('b')
sh.logout()
sh.close()
