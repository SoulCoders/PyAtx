"""
Shell
-----

众生万象,皆有规律可循,神一般的我发现了其中的规律,开始指手画脚。
我就像个产品狗,我不动手实践,我就瞎BB。

"""


class Shell:
    """
    出生的时候,我懵懂无知,什么都不懂,父辈们细心地教会我一切;
    待我及笄,你看到的将是新的我。
    """
    def open(self, address):
        return True

    def close(self):
        return True

    def login(self, user):
        return True

    def logout(self):
        return True

    def send(self, cmd, exp_list, timeout):
        return True

    def read(self, exp_list, timeout):
        return True

    # 我只是为了解决pycharm中的代码提示
    def __getattr__(self, item):
        pass


class ShellTypeBuilder:
    """
    我自己也啥都不干,我的子孙沿着我走过的轨迹探索未知;
    """
    def build(self):
        # 为了语法提示,我们这里还是决定返回一个默认shell,只是它什么也干不了
        return Shell()


class ShellCreator:
    """
    我创造一切,统治万物,我就是权威;
    我的话很少,但是做的事情可不简单;
    我手中的权杖让你不得不服从我的规则,不服从我就无法从我这获得什么.
    """
    __shells = []

    # 我说,要有鲍鱼,厨师就端上来了
    @staticmethod
    def create(name):
        for sh in ShellCreator.__shells:
            if sh[0] == name:
                return sh[1]().build()
        return ShellTypeBuilder().build()

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
