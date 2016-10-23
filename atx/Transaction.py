import logging


class Command:
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
        return args.keys()

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
