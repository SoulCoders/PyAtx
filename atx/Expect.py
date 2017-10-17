"""
ObjectExpect
----------

话说,我喜欢我的对象符合我的要求.

例子
-----
from atx.Expect import ObjectExpect

result = ObjectExpect({
    "a": 0,
    "b": 1,
    "c": "sss",
    "d": {
        "a": 1
    }
}, {
    "a": [0, 1, 2, 3],
    "b": lambda x: x <= 1,
    "c": lambda x: len(x) == 3,
    "d": {
        "a": [1,2],
        "f": 22
    },
})

关于
-----
Author: tkorays<tkorays@hotmail.com>
"""


def ObjectExpect(obj, exp):
    if type(obj) is not object and not dict:
        raise Exception("obj is expected to be a object or a dict.")
    if type(exp) is not dict:
        raise Exception("exp should be a dict.")

    if not obj and exp:
        return False
    elif not obj and not exp:
        return True

    for k, v in exp.items():
        o = obj.__dict__ if type(obj) is object else obj
        if k not in o:
            print('[expect][fail] key "{}": not exist.'.format(k))
            return False
        if type(v) is dict:
            ret = ObjectExpect(o[k], v)
            if not ret:
                return False
        elif type(v) is list:
            if o[k] not in v:
                print('[expect][fail] key "{}": "{}" in list "{}"'.format(k, o[k], v))
                return False
        elif callable(v):
            if not v(o[k]):
                print('[expect][fail] key "{}": function judge fail.'.format(k))
                return False
        else:
            if o[k] != v:
                return False
    return True


