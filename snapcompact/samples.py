"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "order":
        events = [
            (0, "set", ("x", 1)), (0, "compact", "r1"),
            (1, "set", ("x", 2)), (1, "compact", "r2"),
        ]
        state, _ = core.simulate(events, 10, core.Counter())
        _line({"x": state["merged"].get("x")})
        return 0
    if name == "future":
        events = [
            (0, "set", ("x", 1)), (9, "set", ("y", 2)), (5, "compact", "r1"),
        ]
        state, _ = core.simulate(events, 10, core.Counter())
        _line({"keys": sorted(state["merged"])})
        return 0
    if name == "idem":
        events = [
            (0, "set", ("x", 1)), (0, "compact", "r1"), (1, "compact", "r1"),
        ]
        state, _ = core.simulate(events, 10, core.Counter())
        _line({"history": len(state["history"])})
        return 0
    if name == "retention":
        events = [(0, "compact", "r1"), (5, "compact", "r2"), (20, "compact", "r3")]
        state, _ = core.simulate(events, 10, core.Counter())
        _line({"history": len(state["history"])})
        return 0
    if name == "work":
        events = []
        for i in range(2000):
            events.append((i, "set", ("k%04d" % i, i)))
            events.append((i, "compact", "c%04d" % i))
        counter = core.Counter()
        core.simulate(events, 10, counter)
        _line({"compacts": 2000, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
