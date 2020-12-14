import asyncio
import json
from typing import Callable, Any, Dict

from server.methods.fortnite import Fortnite
from server.methods.csgo import Csgo
from server.methods.test_methods import TestMethods


class TreeNode:
    def __init__(self, mul, title=''):
        self.mul = mul
        self.title = title

    async def evaluate(self, user):
        return self.mul


class Branch(TreeNode):
    def __init__(self, mul, desc, func, title=''):
        super(Branch, self).__init__(mul)
        self.desc = desc
        self.func = func
        self.title = title

    async def evaluate(self, user):
        tasks = [asyncio.ensure_future(x.evaluate(user)) for x in self.desc]
        done, _ = await asyncio.wait(tasks)
        return self.mul * self.func([await x for x in done])


class Leaf(TreeNode):
    def __init__(self, mul, method, title=''):
        super(Leaf, self).__init__(mul)
        self.method = method
        self.title = title

    async def evaluate(self, user):
        return self.mul * await self.method(user)


class TreeDecoder(json.JSONDecoder):
    funcs = {
        'max': max,
        'sum': sum
    }
    fortnite = Fortnite()
    csgo = Csgo()
    methods = {
        'test': TestMethods.test,
        'fortnite.duo.wins': fortnite.request_duo_wins,
        'fortnite.duo.top5': fortnite.request_duo_top5,
        'fortnite.duo.top12': fortnite.request_duo_top12,
        'fortnite.trio.wins': fortnite.request_trio_wins,
        'fortnite.trio.top3': fortnite.request_trio_top3,
        'fortnite.trio.top6': fortnite.request_trio_top6,
        'fortnite.squad.wins': fortnite.request_squad_wins,
        'fortnite.squad.top3': fortnite.request_squad_top3,
        'fortnite.squad.top6': fortnite.request_squad_top6,
            
        'csgo.total_time_played': csgo.request_total_time_played,
        'csgo.total_wins': csgo.request_total_wins,
        'csgo.total_rounds_played': csgo.request_total_rounds_played,
        'csgo.total_mvps': csgo.request_total_mvps,
        'csgo.total_matches_won': csgo.request_total_matches_won,
        'csgo.total_matches_played': csgo.request_total_matches_played,
        'csgo.total_weapons_donated': csgo.request_total_weapons_donated,
        'csgo.matches_winrate': csgo.request_matches_winrate,
        'csgo.rounds_winrate': csgo.request_rounds_winrate,
        'csgo.avg_round_per_match': csgo.request_avg_round_per_match,
        'csgo.avg_won_round_per_match': csgo.request_avg_won_round_per_match,
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
        res = ioloop.run_until_complete(json.load(f, cls=TreeDecoder).evaluate({"fortnite-name": "100"}))
        ioloop.close()
        return res


if __name__ == '__main__':
    print(test())
