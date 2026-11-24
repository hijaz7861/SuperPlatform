import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from modules.chat_command_engine.intent_parser import IntentParser
from modules.chat_command_engine.command_router import CommandRouter
from modules.chat_command_engine.context_memory import ContextMemory
from modules.chat_command_engine.response_generator import ResponseGenerator


def test_intent_parse():
    p = IntentParser()
    r = p.parse("scan problems in techsupport")
    assert r["intent"] == "scan_problems"


def test_router():
    router = CommandRouter()
    router.register("status", lambda params, parsed: "ok")
    r = router.route("status check")
    assert r["result"] == "ok"


def test_context_memory():
    cm = ContextMemory()
    cm.add("user", "hello", "greet")
    assert len(cm.get_recent()) == 1


def test_response_gen():
    rg = ResponseGenerator()
    out = rg.generate("help")
    assert "commands" in out


if __name__ == "__main__":
    test_intent_parse()
    test_router()
    test_context_memory()
    test_response_gen()
    print("CHAT COMMAND ENGINE TESTS: PASS")
