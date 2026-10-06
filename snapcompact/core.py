"""增量合并与压缩记录维护。"""


class Counter:
    """记录压缩时重放过的增量条数。"""

    def __init__(self):
        self.scanned = 0


def new_state():
    return {
        "merged": {},
        "deltas": [],
        "applied": 0,
        "compactions": {},
        "history": [],
    }


def compact(state, now, window, rid, counter):
    """把增量并进基准视图，登记一次压缩。"""
    if rid in state["compactions"]:
        return {"keys": len(state["merged"]), "history": len(state["history"])}
    ready = []
    pending = []
    for d in state["deltas"]:
        counter.scanned += 1
        if d["tick"] <= now:
            ready.append(d)
        else:
            pending.append(d)
    ready.sort(key=lambda d: d["tick"])
    for d in ready:
        state["merged"][d["key"]] = d["value"]
    state["applied"] += len(ready)
    state["deltas"] = pending
    state["compactions"][rid] = now
    state["history"].append({"tick": now, "keys": len(state["merged"])})
    state["history"] = [h for h in state["history"] if now - window <= h["tick"] <= now]
    return {"keys": len(state["merged"]), "history": len(state["history"])}


def simulate(events, window, counter):
    """按给定的事件序列逐 tick 推进，返回最终状态与时间线。"""
    state = new_state()
    timeline = []
    for tick, kind, payload in events:
        if kind == "set":
            state["deltas"].append({"tick": tick, "key": payload[0], "value": payload[1]})
        elif kind == "compact":
            compact(state, tick, window, payload, counter)
        timeline.append({"tick": tick, "keys": len(state["merged"]), "history": len(state["history"])})
    return state, timeline
