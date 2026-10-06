import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from snapcompact import core


class SnapcompactTest(unittest.TestCase):
    def test_new_state_empty(self):
        state = core.new_state()
        self.assertEqual(state["merged"], {})
        self.assertEqual(state["history"], [])

    def test_single_delta_merges(self):
        state = core.new_state()
        state["deltas"].append({"tick": 0, "key": "x", "value": 1})
        core.compact(state, 0, 10, "r1", core.Counter())
        self.assertEqual(state["merged"]["x"], 1)

    def test_history_records_compaction(self):
        state = core.new_state()
        core.compact(state, 0, 10, "r1", core.Counter())
        self.assertEqual(len(state["history"]), 1)

    def test_compaction_registered(self):
        state = core.new_state()
        core.compact(state, 3, 10, "r1", core.Counter())
        self.assertEqual(state["compactions"]["r1"], 3)

    def test_distinct_ids_append(self):
        state = core.new_state()
        core.compact(state, 0, 10, "r1", core.Counter())
        core.compact(state, 1, 10, "r2", core.Counter())
        self.assertEqual(len(state["history"]), 2)

    def test_simulate_timeline_length(self):
        events = [(0, "set", ("x", 1)), (0, "compact", "r1")]
        _state, timeline = core.simulate(events, 10, core.Counter())
        self.assertEqual(len(timeline), 2)


if __name__ == "__main__":
    unittest.main()
