import sys
sys.setrecursionlimit(100)  # глубина рекурсии < 10


# приведение словаря к flatten без сторонних библиотек
def flattening(dd, sep='.', prefix=''):
    return {prefix+sep+k if prefix else k: v
            for kk, vv in dd.items()
            for k, v in flattening(vv, sep, kk).items()
            } if isinstance(dd, dict) else {prefix: dd}


def dict_diff(old, new):
    #     """ Функция принимает на вход два словаря old и new,
    #         и возвращает diff их flatten-представлений.
    #         Ключами словарей (.keys()) могут быть только строки.
    #         Значениями (.values()) только словари, строки, числа.
    #     """
    old_dict = flattening(old)
    new_dict = flattening(new)
    out = str()
    for old_key in old_dict:
        if not (old_key in new_dict and old_dict[old_key] == new_dict[old_key]):
            out += '- '+old_key+' '+str(old_dict[old_key])+'\n'
    for new_key in new_dict:
        if not (new_key in old_dict and old_dict[new_key] == new_dict[new_key]):
            out += '+ '+new_key+' '+str(new_dict[new_key])+'\n'
    return out


diff = dict_diff({'a': {'x': 1}, 'b': 2}, {'b': 3, 'c': 4})
print(diff)
"""
- a.x 1
- b 2
+ b 3
+ c 4
"""