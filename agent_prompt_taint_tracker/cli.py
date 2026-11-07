"""CLI for agent-prompt-taint-tracker."""
import sys
import argparse
from .tracker import AgentPromptTaintTracker


def main():
    parser = argparse.ArgumentParser(description="Agent Prompt Taint Tracker")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    args = parser.parse_args()

    if args.demo:
        tracker = AgentPromptTaintTracker()
        tracker.register_untrusted("comment", "; drop table users;", source="untrusted_http")
        res1 = tracker.check_sink("bash_exec", "echo 'hello world'")
        res2 = tracker.check_sink("bash_exec", "run_cmd --query '; drop table users;'")
        print(f"Safe check: {res1['is_safe']}")
        print(f"Tainted check: {res2['is_safe']}, Violations: {res2['violations']}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
