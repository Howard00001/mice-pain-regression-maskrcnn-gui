import os


def reformat_string(s):
    assert isinstance(s, str) and len(s) > 0

    # remove file format
    i = len(s) - 1
    while i > 0 and s[i] != '.':
        i -= 1
    s = s[:i]

    # remove alphabet
    rst = []
    for x in s:
        if x.isdigit():
            rst.append(x)
    return ''.join(rst)


class Process():
    def __init__(self):
        self.frame = 0

    def A(self, *args, **kwargs):
        self.frame += 1
        print('A', str(self.frame))

    def B(self, d, *args, **kwargs):
        self.frame += 1
        print('B', str(self.frame))
        print('d', d)

    def C(self, *args, **kwargs):
        self.frame += 1
        print('C', str(self.frame))

    def action(self, status, *args, **kwargs):
        actionMap = {
            'A': (self.A, 'B'),
            'B': (self.B, 'C'),
            'C': (self.C, None)
        }

        while status:
            func, nextStep = actionMap[status]
            func(*args, **kwargs)
            print(args, kwargs)
            status = nextStep


def calc(a, b, *args, **kwargs):
    print(a + b)
    print(args, kwargs)
    return


if __name__ == '__main__':
    a = Process()
    a.action('A', d=5)

    # calc(5,9)
    # calc(a=5, b=9)
    # parms = {
    #     'a': 9,
    #     'b': 100,
    #     'c': 20
    # }
    # calc(**parms)
