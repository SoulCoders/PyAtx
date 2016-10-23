import logging


class Command:
    """
    Command for Transactions.
    This class have not do some checking, DO NOT use this class!!!
    """
    def __init__(self, do, do_arg, undo, undo_arg, undo_when_fail):
        self.__do = do
        self.__do_arg = do_arg
        self.__undo = undo
        self.__undo_arg = undo_arg
        self.__undo_when_fail = undo_when_fail

        # 用户设置返回值名称,事务自动管理返回值
        self.__do_ret_name = ''
        self.__undo_ret_name = ''
        # 延迟参数绑定,支持多个参数绑定
        self.__do_delay_arg_name = []
        self.__undo_delay_arg_name = []
        self.__do_delay_arg = None
        self.__undo_delay_arg = None

    # 设置返回值名称,避免初始化时传入过多参数
    def set_ret(self, do_ret_name='', undo_ret_name=''):
        self.__do_ret_name = do_ret_name
        self.__undo_ret_name = undo_ret_name

    def get_ret(self):
        return {
            'do': self.__do_ret_name,
            'undo': self.__undo_ret_name
        }

    def set_delay_arg_name(self, do_arg=None, undo_arg=None):
        if do_arg:
            self.__do_delay_arg_name = do_arg
        if undo_arg:
            self.__undo_delay_arg_name = undo_arg

    def get_delay_arg_name(self):
        return {
            'do': self.__do_delay_arg_name,
            'undo': self.__undo_delay_arg_name
        }

    def set_delay_arg(self, do_arg=None, undo_arg=None):
        self.__do_delay_arg = do_arg
        self.__undo_delay_arg = undo_arg

    def is_undo_when_fail(self):
        return self.__undo_when_fail

    @staticmethod
    def __expand_arg(in_arg, delay_arg):
        args = {}
        for index, arg in enumerate(in_arg):
            if hasattr(arg, '__call__'):
                arg = arg(delay_arg[index])
            args[index] = arg
        return args.values()

    def do(self):
        return self.__do(*self.__expand_arg(self.__do_arg, [x for x in self.__do_delay_arg]))

    def undo(self):
        return self.__undo(*self.__expand_arg(self.__undo_arg, [x for x in self.__undo_delay_arg]))


class Transaction:

    def __init__(self):
        self.__commands = []
        self.__data = {}

    # 支持链式调用
    def add(self, do_func, do_func_arg=(), undo_func=None, undo_func_arg=(), undo_when_fail=True):
        if not hasattr(do_func, '__call__') or (undo_func and not hasattr(undo_func, '__call__')):
            print('DO and UNDO function must be callable or NoneType!')
            return self
        if not isinstance(do_func_arg, type(())) or not isinstance(undo_func_arg, type(())):
            print("Args should be tupple!")
            return self

        self.__commands.append(Command(do_func, do_func_arg, undo_func, undo_func_arg))
        return self

    def save_ret(self, do_ret='', undo_ret=''):
        self.__commands[len(self.__commands) - 1].set_ret(do_ret, undo_ret)
        return self

    # 延迟参数需要用字符串的list表示
    def set_delay_arg(self, do_arg, undo_arg):
        if not isinstance(do_arg, type([])) or not isinstance(undo_arg, type([])):
            print("Delay args should be list!")
            return self
        self.__commands[len(self.__commands) - 1].set_delay_arg_name(do_arg, undo_arg)
        return self

    # 事务提交,执行成功返回True,失败后自动回滚并返回False
    def commit(self):
        for index, c in self.__commands:
            # 延迟绑定的参数
            da = {}
            for i, a in enumerate(c.get_delay_arg_name()['do']):
                # TODO: 憋问我为什么不检查是否存在这个键值,懒得检查
                da[i] = self.__data[a]
            c.set_delay_arg(do_arg=da.values())

            ret = c.do()
            # 保存返回值
            if c.get_ret()['do']:
                self.__data[c.get_ret()['do']] = ret

            # 如果设置了出错后回滚则回滚!
            if not ret and c.is_undo_when_fail():
                self.rollback(index)
                return False
        return True

    def rollback(self, index=-1):
        index = index if 0 <= index < len(self.__commands) else (len(self.__commands) - 1)
        while index >= 0:
            c = self.__commands[index]

            # 延迟参数绑定
            uda = {}
            for i, a in enumerate(c.get_delay_arg_name()['undo']):
                # TODO: 如果你传入一个错误的参数,怪我我咯?
                uda[i] = self.__data[a]
            # 此时并不关心给do参数设置成啥
            c.set_delay_arg(undo_arg=uda.values())

            # 回滚失败继续执行
            ret = c.undo()
            if c.get_ret()['undo']:
                self.__data[c.get_ret()['undo']] = ret
            index -= 1
