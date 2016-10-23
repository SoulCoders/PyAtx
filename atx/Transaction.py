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
        delay_arg = [x for x in delay_arg]
        args = {}
        for index, arg in enumerate(in_arg):
            if hasattr(arg, '__call__'):
                arg = arg(delay_arg[index])
            args[index] = arg
        return args.values()

    def do(self):
        return self.__do(*self.__expand_arg(self.__do_arg, self.__do_delay_arg))

    def undo(self):
        return self.__undo(*self.__expand_arg(self.__undo_arg, self.__undo_delay_arg))


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

    def commit(self):
        for index, c in self.__commands:
            # 延迟绑定的参数
            da = {}
            uda = {}
            do_args = c.get_delay_arg_name()['do']
            undo_args = c.get_delay_arg_name()['undo']
            for i, a in enumerate(do_args):
                # TODO: a存在?
                da[i] = self.__data[a]
            for i, a in enumerate(undo_args):
                uda[i] = self.__data[a]
            # 先获取参数列表,然后获取真实值代替
            c.set_delay_arg(da.values(), uda.values())
            ret = c.do()
            # 保存返回值
            if c.get_ret()['do']:
                self.__data[c.get_ret()['do']] = ret

            # 如果设置了出错后回滚则回滚!
            if not ret and c.is_undo_when_fail():
                self.rollback(index)
                break

    def rollback(self, index=-1):
        pass



class Command1:
    def __init__(self, do_func, do_func_args, undo_func, undo_func_args):
        self.__do_func = do_func
        self.__do_func_args = do_func_args
        self.__undo_func = undo_func
        self.__undo_func_args = undo_func_args
        self.__return_name = ""
        self.__do_delay_feed_name = ""
        self.__undo_delay_feed_name = ""
        self.__do_delay_args = ()
        self.__undo_delay_args = ()
        self.__undo_when_fail = True

    @staticmethod
    def __expand_args(in_args, delay_args):
        args = {}
        for index, arg in enumerate(in_args):
            if hasattr(arg, '__call__'):
                args[index] = arg(*delay_args)
            else:
                args[index] = arg
        return args.values()

    def do(self):
        # we suppose the function to be valid
        return self.__do_func(*self.__expand_args(self.__do_func_args, self.__do_delay_args))

    def undo(self):
        return self.__undo_func(*self.__expand_args(self.__undo_func_args, self.__undo_delay_args))

    def set_do_delay_args(self, args):
        self.__do_delay_args = args

    def set_undo_delay_args(self, args):
        self.__undo_delay_args = args

    def set_return_name(self, name):
        self.__return_name = name

    def set_do_delay_feed_name(self, name):
        self.__do_delay_feed_name = name

    def set_undo_delay_feed_name(self, name):
        self.__undo_delay_feed_name = name

    def get_return_name(self):
        return self.__return_name

    def get_do_delay_feed_name(self):
        return self.__do_delay_feed_name

    def ge_undo_delay_feed_name(self):
        return self.__undo_delay_feed_name

    def set_undo_when_fail(self, s=True):
        self.__undo_when_fail = s


class Transaction:

    def __init__(self):
        self.__commands = []
        self.__data = {}
        pass

    def append(self, do_func, do_func_args, undo_func, undo_func_args):
        if not hasattr(do_func, '__call__') or not hasattr(undo_func, '__call__'):
            logging.error("invalid function!")
            return self
        if type(do_func_args) != type(()) or type(undo_func_args) != type(()):
            logging.error("paramenter should be a tuple!")
            return self
        self.__commands.append(Command(do_func, do_func_args, undo_func, undo_func_args))
        return self

    def ret(self, name):
        self.__commands[len(self.__commands) - 1].set_return_name(name)

    def feed_do_delay_args(self, name):
        if name not in self.__data.keys():
            logging.error("%s is not in the data sets", name)
            return self
        self.__commands[len(self.__commands) - 1].set_do_delay_args(self.data[name])
        return self

    def feed_undo_delay_args(self, name):
        if name not in self.__data.keys():
            logging.error("%s is not in the data sets", name)
            return self
        self.__commands[len(self.__commands) - 1].set_undo_delay_args(self.data[name])
        return self

    def rollback_when_fail(self, s=True):
        self.__commands[len(self.__commands) - 1].set_undo_when_fail(s)
        return self

    def commit(self):
        for index,c in enumerate(self.__commands):
            # feed params
            if c.get_do_delay_feed_name():
                c.set_do_delay_args(self.__data[c.get_do_delay_feed_name()])
            ret = c.do()
            if not ret:
                self.rollback(index)
                return False
            if c.get_return_name():
                self.__data[c.get_return_name()] = ret
        return True

    def rollback(self, start=-1):
        index = len(self.__commands)-1 if start==-1 else start
        if index < 0 or index >= len(self.__commands):
            logging.error("rollback index error!")
            return False
        while index >= 0:
            c = self.__commands[index]
            if c.ge_undo_delay_feed_name():
                c.set_undo_delay_args(self.__data[c.ge_undo_delay_feed_name()])
            c.undo()
        return True
