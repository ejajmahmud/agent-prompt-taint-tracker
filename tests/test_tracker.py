"""Tests for agent-prompt-taint-tracker."""
import unittest
from agent_prompt_taint_tracker.tracker import AgentPromptTaintTracker


class TestTaintTracker(unittest.TestCase):
    def setUp(self):
        self.t = AgentPromptTaintTracker()

    def test_taint_sink_violation(self):
        self.t.register_untrusted("user_arg", "malicious_flag", "web")
        check = self.t.check_sink("shell", "git log malicious_flag")
        self.assertFalse(check["is_safe"])
        self.assertEqual(len(check["violations"]), 1)

    def test_safe_execution(self):
        self.t.register_untrusted("user_arg", "evil_val", "web")
        check = self.t.check_sink("shell", "git status")
        self.assertTrue(check["is_safe"])
