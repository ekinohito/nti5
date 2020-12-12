import asyncio
import json
from typing import Callable, Any, Dict

from server.methods.test_methods import TestMethods


class TreeNode:
    def __init__(self, mul):
        self.mul = mul

    async def evaluate(self, user):
        return self.mul


class Branch(TreeNode):
    def __init__(self, mul, desc, func):
        super(Branch, self).__init__(mul)
        self.desc = desc
        self.func = func

    async def evaluate(self, user):
        tasks = [asyncio.ensure_future(x.evaluate(user)) for x in self.desc]
        done, _ = await asyncio.wait(tasks)
        return self.mul * self.func([await x for x in done])


class Leaf(TreeNode):
    def __init__(self, mul, method):
        super(Leaf, self).__init__(mul)
        self.method = method

    async def evaluate(self, user):
        return self.mul * await self.method(user)


class TreeDecoder(json.JSONDecoder):
    funcs = {
        'max': max,
        'sum': sum
    }

    methods = {
        'test': TestMethods.test
    }

    def decode(self, s: str, _w: Callable[..., Any] = ...):
        d = json.loads(s)
        return self._process(d)

    @classmethod
    def _process(cls, d: Dict):
        if 'desc' in d:
            d['desc'] = [cls._process(x) for x in d['desc']]
            d['func'] = cls.funcs[d['func']]
            return Branch(**d)
        else:
            d['method'] = cls.methods[d['method']]
            return Leaf(**d)


def test():
    with open('test_tree.json') as f:
        ioloop = asyncio.get_event_loop()
        res = ioloop.run_until_complete(json.load(f, cls=TreeDecoder).evaluate({}))
        ioloop.close()
        return res


if __name__ == '__main__':
    print(test())
