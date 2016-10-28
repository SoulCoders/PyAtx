"""
Shell
-----

众生万象,皆有规律可循,神一般的我发现了其中的规律,开始指手画脚。
我就像个产品狗,我不动手实践,我就瞎BB。

Builder使用组合方式还是类继承由设计者决定。

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
