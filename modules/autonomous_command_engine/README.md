# SuperPlatform Autonomous Command Engine

Lightweight Termux client + remote FastAPI execution server.

Flow:
Termux -> Command API -> Task Planner -> Compute Router -> Worker -> Verification -> Result

Design goals:
- Keep heavy work off the phone when a remote worker is available.
- Accept one high-level command and execute a safe, predefined task workflow.
- Automatically test and retry supported software tasks.
- Keep job status, logs, and artifacts.
- Never silently perform irreversible/high-impact actions.
- Provider adapters can later be added for CPU/GPU/quantum backends.

This starter deliberately does NOT execute arbitrary shell commands received from the network.
Add controlled worker actions instead.
