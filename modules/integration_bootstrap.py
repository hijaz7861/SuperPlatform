"""Bootstrap: register all modules into UniversalRegistry."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core.universal.universal_registry import UniversalRegistry


def build_registry():
    reg = UniversalRegistry()
    try:
        from modules.problem_scanner import RedditScanner, ProblemClassifier, PricingEngine
        reg.register_module("problem_scanner", RedditScanner())
        reg.register_engine("problem_classifier", ProblemClassifier())
        reg.register_engine("pricing_engine", PricingEngine())
    except Exception as e:
        print("problem_scanner register failed:", e)
    try:
        from modules.token_manager import QuotaEngine, RateLimiter, UsageTracker, PerformanceMonitor
        reg.register_engine("quota_engine", QuotaEngine())
        reg.register_engine("rate_limiter", RateLimiter())
        reg.register_engine("usage_tracker", UsageTracker())
        reg.register_engine("performance_monitor", PerformanceMonitor())
    except Exception as e:
        print("token_manager register failed:", e)
    try:
        from modules.chat_command_engine import IntentParser, CommandRouter, ContextMemory, ResponseGenerator
        reg.register_engine("intent_parser", IntentParser())
        reg.register_engine("command_router", CommandRouter())
        reg.register_engine("context_memory", ContextMemory())
        reg.register_engine("response_generator", ResponseGenerator())
    except Exception as e:
        print("chat_command_engine register failed:", e)
    try:
        from modules.voice_listener import VoiceListener, Transcriber, WakeWordDetector
        reg.register_engine("voice_listener", VoiceListener())
        reg.register_engine("transcriber", Transcriber())
        reg.register_engine("wake_word", WakeWordDetector())
    except Exception as e:
        print("voice_listener register failed:", e)
    try:
        from modules.distributed_agent import Coordinator, Worker, TaskQueue, Aggregator
        reg.register_engine("distributed_coordinator", Coordinator(num_workers=10))
        reg.register_engine("distributed_task_queue", TaskQueue())
        reg.register_engine("distributed_aggregator", Aggregator())
    except Exception as e:
        print("distributed_agent register failed:", e)
    return reg


if __name__ == "__main__":
    r = build_registry()
    print(r.describe())
