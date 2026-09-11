#!/usr/bin/env python3

import json
import os
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.home() / "SuperPlatform"

CONFIG = ROOT / "config" / "cloud"
LOGS = ROOT / "logs" / "cloud"
BACKUPS = ROOT / "backups" / "cloud"

PROVIDERS_FILE = CONFIG / "providers.json"
REPORT_FILE = CONFIG / "verification.json"
LOG_FILE = LOGS / "cloudctl.log"


def now():
    return datetime.now(timezone.utc).isoformat()


def log(message):
    LOGS.mkdir(parents=True, exist_ok=True)
    line = f"[{now()}] {message}"
    print(line)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def http_get(url, headers=None, timeout=10):
    request = urllib.request.Request(
        url,
        headers=headers or {},
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(4096).decode("utf-8", errors="replace")
            return {
                "reachable": True,
                "status": response.status,
                "body": body,
                "error": None,
            }

    except urllib.error.HTTPError as exc:
        body = exc.read(4096).decode("utf-8", errors="replace")
        return {
            "reachable": True,
            "status": exc.code,
            "body": body,
            "error": None,
        }

    except Exception as exc:
        return {
            "reachable": False,
            "status": None,
            "body": "",
            "error": type(exc).__name__,
        }


def internet_check():
    for url in [
        "https://www.cloudflare.com",
        "https://github.com",
    ]:
        result = http_get(url, timeout=8)

        if result["reachable"]:
            return True

    return False


def local_verify():
    checks = {
        "project": ROOT.is_dir(),
        "python": shutil.which("python") is not None,
        "git": shutil.which("git") is not None,
        "tar": shutil.which("tar") is not None,
        "internet": internet_check(),
        "cloud_directory": CONFIG.is_dir(),
    }

    print("=== SUPERPLATFORM LOCAL PREFLIGHT ===")

    for name, result in checks.items():
        print(f"{name.upper():20} {'PASS' if result else 'FAIL'}")

    return all(checks.values())


def base_providers():
    return [
        {
            "id": "render",
            "name": "Render",
            "category": "cloud_application_host",
            "runtime": ["python", "fastapi"],
            "free_candidate": True,
            "authentication_required": True,
            "deployment": "api_or_git",
            "verified": False,
        },
        {
            "id": "cloudflare",
            "name": "Cloudflare",
            "category": "edge_platform",
            "runtime": ["workers"],
            "free_candidate": True,
            "authentication_required": True,
            "deployment": "api_or_git",
            "verified": False,
        },
    ]


def discover_providers():
    providers = base_providers()

    CONFIG.mkdir(parents=True, exist_ok=True)

    data = {
        "generated_at": now(),
        "providers": providers,
    }

    PROVIDERS_FILE.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("=== PROVIDER DISCOVERY ===")

    for provider in providers:
        print(
            f"{provider['name']}: "
            f"{provider['category']} | "
            f"free_candidate={provider['free_candidate']} | "
            f"verified={provider['verified']}"
        )

    log("Provider registry created.")
    return providers


def verify_render():
    token = os.environ.get("RENDER_API_KEY")

    result = {
        "provider": "render",
        "endpoint": "https://api.render.com/v1/services?limit=1",
        "network_reachable": False,
        "credentials_present": bool(token),
        "authenticated": False,
        "verified": False,
        "status": None,
        "reason": "",
    }

    headers = {
        "Accept": "application/json",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = http_get(
        "https://api.render.com/v1/services?limit=1",
        headers=headers,
    )

    result["network_reachable"] = response["reachable"]
    result["status"] = response["status"]

    if not response["reachable"]:
        result["reason"] = "Render API unreachable"
        return result

    if not token:
        result["reason"] = "RENDER_API_KEY not configured"
        return result

    if response["status"] == 200:
        result["authenticated"] = True
        result["verified"] = True
        result["reason"] = "Render API authentication verified"
    elif response["status"] in (401, 403):
        result["reason"] = "Render credentials rejected or insufficient"
    else:
        result["reason"] = f"Render API returned HTTP {response['status']}"

    return result


def verify_cloudflare():
    token = os.environ.get("CLOUDFLARE_API_TOKEN")

    result = {
        "provider": "cloudflare",
        "endpoint": "https://api.cloudflare.com/client/v4/user/tokens/verify",
        "network_reachable": False,
        "credentials_present": bool(token),
        "authenticated": False,
        "verified": False,
        "status": None,
        "reason": "",
    }

    headers = {
        "Accept": "application/json",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    response = http_get(
        "https://api.cloudflare.com/client/v4/user/tokens/verify",
        headers=headers,
    )

    result["network_reachable"] = response["reachable"]
    result["status"] = response["status"]

    if not response["reachable"]:
        result["reason"] = "Cloudflare API unreachable"
        return result

    if not token:
        result["reason"] = "CLOUDFLARE_API_TOKEN not configured"
        return result

    if response["status"] == 200:
        result["authenticated"] = True
        result["verified"] = True
        result["reason"] = "Cloudflare API token verified"
    elif response["status"] in (401, 403):
        result["reason"] = "Cloudflare token rejected or insufficient"
    else:
        result["reason"] = f"Cloudflare API returned HTTP {response['status']}"

    return result




def render_deployment_plan():
    """Generate a local read-only Render deployment plan."""
    import json
    from pathlib import Path

    project = Path.cwd()

    print("=== RENDER DEPLOYMENT PLAN ===")

    required = [
        "tools/cloud_host/cloudctl.py",
        "config/cloud/providers.json",
    ]

    missing = [x for x in required if not (project / x).exists()]

    if missing:
        print("PLAN STATUS : NOT_READY")
        print("MISSING     :", ", ".join(missing))
        return 1

    plan = {
        "provider": "render",
        "operation": "deployment_plan_only",
        "deployment_performed": False,
        "remote_write_actions": False,
        "arbitrary_remote_shell": False,
        "runtime": "python",
        "application_target": "SuperPlatform",
        "source": "current_git_repository",
        "authentication": "RENDER_API_KEY",
        "deployment_mode": "explicit_approval_required"
    }

    output = project / "config/cloud/render_deployment_plan.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, indent=2) + "\n")

    print("PLAN STATUS            : READY")
    print("PROVIDER               : Render")
    print("RUNTIME                : Python")
    print("TARGET                 : SuperPlatform")
    print("DEPLOYMENT PERFORMED   : false")
    print("REMOTE WRITE ACTIONS   : false")
    print("ARBITRARY REMOTE SHELL : false")
    print("PLAN FILE              :", output)
    print("APPROVAL REQUIRED      : true")

    return 0

def render_readiness():
    """Read-only Render deployment readiness check."""
    import os
    from pathlib import Path

    print("=== RENDER CLOUD READINESS ===")

    checks = []

    def check(name, passed, detail):
        status = "PASS" if passed else "FAIL"
        checks.append(passed)
        print(f"{name:<22}: {status} | {detail}")

    project = Path.cwd()

    check(
        "PROJECT",
        project.exists() and (project / "tools").exists(),
        str(project),
    )

    check(
        "GIT",
        (project / ".git").exists(),
        "Git repository detected",
    )

    check(
        "PYTHON",
        (project / "tools" / "cloud_host" / "cloudctl.py").exists(),
        "cloudctl.py available",
    )

    render_key = bool(os.environ.get("RENDER_API_KEY"))
    check(
        "RENDER_CREDENTIAL",
        render_key,
        "API credential present",
    )

    render_files = [
        "tools/cloud_host/cloudctl.py",
        "config/cloud/providers.json",
    ]

    missing = [x for x in render_files if not (project / x).exists()]

    check(
        "CLOUD_CONFIG",
        not missing,
        "Required cloud files present"
        if not missing
        else "Missing: " + ", ".join(missing),
    )

    forbidden = [
        ".env",
        ".env.local",
        ".env.production",
    ]

    exposed = [x for x in forbidden if (project / x).exists()]

    check(
        "SECRET_GUARD",
        not exposed,
        "No common environment-secret files detected"
        if not exposed
        else "Review: " + ", ".join(exposed),
    )

    print()
    print("DEPLOYMENT_PERFORMED : false")
    print("REMOTE_WRITE_ACTIONS : false")
    print("ARBITRARY_REMOTE_SHELL: false")

    if all(checks):
        print("OVERALL              : READY")
        return 0

    print("OVERALL              : NOT_READY")
    return 1

def render_services():
    """Read-only discovery of Render services."""
    import json
    import os
    import urllib.error
    import urllib.request

    key = os.environ.get("RENDER_API_KEY")

    print("=== REAL RENDER SERVICE DISCOVERY ===")

    if not key:
        print("CREDENTIALS : NOT CONFIGURED")
        print("RESULT      : FAIL")
        print("REASON      : RENDER_API_KEY not configured")
        return 1

    url = "https://api.render.com/v1/services?limit=100"

    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/json",
            "Authorization": f"Bearer {key}",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            body = response.read().decode()
            data = json.loads(body)

            print("NETWORK      : PASS")
            print("AUTHENTICATED: PASS")
            print("HTTP STATUS  :", response.status)
            print("RESULT       : PASS")

            if isinstance(data, list):
                print("SERVICES     :", len(data))

                for item in data:
                    service = item.get("service", item)

                    print(
                        "-",
                        service.get("name", "unknown"),
                        "|",
                        service.get("type", "unknown"),
                        "|",
                        service.get("id", "unknown"),
                    )

            else:
                print("RESPONSE TYPE:", type(data).__name__)

            return 0

    except urllib.error.HTTPError as e:
        print("NETWORK      : PASS")
        print("HTTP STATUS  :", e.code)
        print("RESULT       : FAIL")
        print("REASON       :", e.reason)
        return 1

    except Exception as e:
        print("RESULT       : FAIL")
        print("REASON       :", type(e).__name__, str(e))
        return 1

def verify_providers():
    print("=== REAL PROVIDER VERIFICATION ===")

    results = [
        verify_render(),
        verify_cloudflare(),
    ]

    for result in results:
        state = "VERIFIED" if result["verified"] else "UNVERIFIED"

        print()
        print(f"PROVIDER       : {result['provider']}")
        print(f"NETWORK        : {'PASS' if result['network_reachable'] else 'FAIL'}")
        print(
            f"CREDENTIALS    : "
            f"{'PRESENT' if result['credentials_present'] else 'NOT CONFIGURED'}"
        )
        print(
            f"AUTHENTICATED  : "
            f"{'PASS' if result['authenticated'] else 'FAIL'}"
        )
        print(f"STATUS         : {result['status']}")
        print(f"RESULT         : {state}")
        print(f"REASON         : {result['reason']}")

    report = {
        "verified_at": now(),
        "deployment_performed": False,
        "arbitrary_remote_shell": False,
        "providers": results,
    }

    CONFIG.mkdir(parents=True, exist_ok=True)

    REPORT_FILE.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    log("Real provider verification completed.")

    return results


def create_package():
    """Create a bounded source archive without recursive runtime artifacts."""
    BACKUPS.mkdir(parents=True, exist_ok=True)

    output = BACKUPS / "superplatform-cloud-source.tar.gz"

    excluded_names = {
        ".git",
        "backups",
        "__pycache__",
        ".venv",
        "venv",
        "node_modules",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        "dist",
        "build",
    }

    excluded_suffixes = (
        ".bak",
        ".backup",
        ".old",
        ".tmp",
        ".log",
        ".pyc",
        ".pyo",
        ".zip",
        ".tar",
        ".gz",
    )

    def should_exclude(path):
        try:
            relative = path.relative_to(ROOT)
        except ValueError:
            return True

        if path == output:
            return True

        if any(part in excluded_names for part in relative.parts):
            return True

        if path.name.endswith(excluded_suffixes):
            return True

        return False

    if output.exists():
        output.unlink()

    def tar_filter(tarinfo):
        source = ROOT / tarinfo.name

        if should_exclude(source):
            return None

        return tarinfo

    with tarfile.open(output, "w:gz") as archive:
        for item in ROOT.iterdir():
            if should_exclude(item):
                continue

            archive.add(
                item,
                arcname=item.name,
                recursive=True,
                filter=tar_filter,
            )

    size = output.stat().st_size

    print("=== CLOUD PACKAGE ===")
    print(f"FILE: {output}")
    print(f"SIZE: {size} bytes")

    log(f"Cloud source package created: {output}")

    return True

def status():
    print("=== SUPERPLATFORM CLOUD ORCHESTRATOR ===")
    print()
    print("LOCAL DEVICE ROLE : CONTROLLER")
    print("CLOUD ROLE         : HEAVY COMPUTE / BUILD / AGENTS")
    print()
    print("PIPELINE:")
    print("COMMAND")
    print("  -> COMMAND ROUTER")
    print("  -> AGENT PLANNER")
    print("  -> PROVIDER DISCOVERY")
    print("  -> CAPABILITY CHECK")
    print("  -> PROVIDER SELECTION")
    print("  -> PACKAGE")
    print("  -> DEPLOY")
    print("  -> HEALTH CHECK")
    print("  -> REVISION VERIFY")
    print("  -> RESULT")
    print()
    print("ARBITRARY REMOTE SHELL : DISABLED")
    print("UNVERIFIED PROVIDER    : NOT DEPLOYED")
    print("AUTO DEPLOY             : AUTH REQUIRED")
    print("ROLLBACK                : REQUIRED")
    print()
    print("Current project:")
    print(ROOT)


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else "status"

    if command == "render-deployment-plan":
        raise SystemExit(render_deployment_plan())

    if command == "render-readiness":
        raise SystemExit(render_readiness())

    if command == "render-services":
        raise SystemExit(render_services())

    if command == "verify":
        sys.exit(0 if local_verify() else 1)

    elif command == "discover":
        discover_providers()

    elif command == "provider-verify":
        results = verify_providers()
        sys.exit(0 if all(r["verified"] for r in results) else 1)

    elif command == "package":
        sys.exit(0 if create_package() else 1)

    elif command == "status":
        status()

    elif command == "all":
        if not local_verify():
            sys.exit(1)

        discover_providers()
        verify_providers()
        create_package()
        status()

    else:
        print("Usage:")
        print("  cloudctl.py verify")
        print("  cloudctl.py discover")
        print("  cloudctl.py provider-verify")
        print("  cloudctl.py package")
        print("  cloudctl.py status")
        print("  cloudctl.py all")
        sys.exit(2)


if __name__ == "__main__":
    main()
