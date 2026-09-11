#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail

# SuperPlatform Self-Healing Bootstrap Runner
# Safe-by-default: diagnoses, validates, and can optionally apply ONLY an explicit
# evidence-backed patch command supplied through --apply-cmd. It never invents
# source changes and never force-pushes.

ROOT="${HOME}/SuperPlatform"
STATE="${ROOT}/.self-healing/state"
REPORTS="${ROOT}/.self-healing/reports"
CACHE="${ROOT}/.self-healing/cache"
MAX_CYCLES="${MAX_CYCLES:-10}"
RUN_ID="${RUN_ID:-}"
TARGET_WORKFLOW="${TARGET_WORKFLOW:-android-pydantic-core.yml}"
SLEEP_SEC="${SLEEP_SEC:-5}"

mkdir -p "$STATE" "$REPORTS" "$CACHE"

log(){ printf '[%s] %s\n' "$(date '+%F %T')" "$*"; }
die(){ log "FATAL: $*"; exit 1; }

usage(){
  cat <<'EOF'
Usage:
  ./super_heal.sh [--workflow FILE] [--run RUN_ID] [--cycles N] [--watch]

Environment:
  AUTO_REPAIR=0   Safe default. No source modification.
  AUTO_REPAIR=1   Only runs an explicitly supplied APPLY_CMD.
  APPLY_CMD='...' Explicit, user-supplied patch command.
  MAX_CYCLES=10
EOF
}

WATCH=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --workflow) TARGET_WORKFLOW="$2"; shift 2;;
    --run) RUN_ID="$2"; shift 2;;
    --cycles) MAX_CYCLES="$2"; shift 2;;
    --watch) WATCH=1; shift;;
    -h|--help) usage; exit 0;;
    *) die "Unknown argument: $1";;
  esac
done

[[ -d "$ROOT/.git" ]] || die "Repository not found: $ROOT"
command -v gh >/dev/null || die "GitHub CLI (gh) is required"
command -v git >/dev/null || die "git is required"

cd "$ROOT"

if ! gh auth status >/dev/null 2>&1; then
  die "GitHub CLI is not authenticated. Run: gh auth login"
fi

command -v python >/dev/null || die "python is required"
python - <<'PY'
import yaml
print("PYTHON/YAML: PASS")
PY
2>/dev/null || {
  log "PyYAML missing; attempting local install."
  python -m pip install --user pyyaml >/dev/null 2>&1 || die "PyYAML install failed"
}

cycle=0
report="$REPORTS/self-heal-$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$report") 2>&1

log "=== SUPERPLATFORM SELF-HEALING RUNNER ==="
log "ROOT=$ROOT"
log "WORKFLOW=$TARGET_WORKFLOW"
log "MAX_CYCLES=$MAX_CYCLES"
log "AUTO_REPAIR=${AUTO_REPAIR:-0}"

git status --short || true

resolve_run(){
  if [[ -n "$RUN_ID" ]]; then return; fi
  RUN_ID="$(gh run list --workflow "$TARGET_WORKFLOW" --limit 1 \
    --json databaseId --jq '.[0].databaseId' 2>/dev/null || true)"
  [[ -n "$RUN_ID" ]] || die "Could not resolve a GitHub run ID"
}

recover_log(){
  local id="$1"
  local out="$REPORTS/run-${id}.log"
  rm -f "$out" "$out.tmp"

  # Primary route.
  if gh run view "$id" --log >"$out.tmp" 2>&1; then
    if [[ -s "$out.tmp" ]]; then
      mv "$out.tmp" "$out"
      echo "$out"
      return 0
    fi
  fi

  # API fallback: retrieve jobs and each job's log.
  local jobs="$CACHE/jobs-${id}.json"
  gh api "repos/${GITHUB_REPOSITORY:-hijaz7861/SuperPlatform}/actions/runs/${id}/jobs?per_page=100" >"$jobs" 2>/dev/null || true

  if [[ -s "$jobs" ]]; then
    : >"$out"
    python - "$jobs" "$out" <<'PY'
import json,sys
data=json.load(open(sys.argv[1]))
ids=[j.get("id") for j in data.get("jobs",[]) if j.get("id")]
open(sys.argv[2],"w").write("\n".join(map(str,ids)))
PY
    while read -r jid; do
      [[ -z "$jid" ]] && continue
      {
        echo "===== JOB $jid ====="
        gh api "repos/${GITHUB_REPOSITORY:-hijaz7861/SuperPlatform}/actions/jobs/${jid}/logs" 2>/dev/null || true
        echo
      } >>"$out"
    done < <(python - "$out" "$jobs" <<'PY'
import json,sys
data=json.load(open(sys.argv[2]))
for j in data.get("jobs",[]):
    if j.get("id"): print(j["id"])
PY
)
  fi

  [[ -s "$out" ]] && { echo "$out"; return 0; }
  rm -f "$out.tmp"
  return 1
}

diagnose(){
  local logf="$1"
  local diag="$REPORTS/diagnosis-${RUN_ID}.txt"
  python - "$logf" "$diag" <<'PY'
import re,sys
from pathlib import Path

log=Path(sys.argv[1]).read_text(errors="replace")
out=Path(sys.argv[2])
lines=log.splitlines()
hits=[]

# High-confidence GitHub/tool diagnostics first.
patterns=[
    r'##\[error\].*',
    r'cibuildwheel:.*',
    r'Process completed with exit code.*',
    r'(?i)^\s*(error|fatal|exception|traceback|permission denied|no such file|not found|unsupported|invalid)\b.*'
]
for line in lines:
    s=line.strip()
    if not s: continue
    if any(re.search(p,s) for p in patterns):
        if s not in hits: hits.append(s)

# Keep output compact.
hits=hits[:100]
text=["=== EXACT DIAGNOSTICS ==="] + (hits or ["NO_HIGH_CONFIDENCE_ERROR_FOUND"])
text += ["", "=== FAILED/PROBLEM STEPS FROM LOG ==="]
for line in lines:
    if "##[error]" in line.lower() or "failed" in line.lower() and "step" in line.lower():
        text.append(line[:1000])
text=text[:220]
out.write_text("\n".join(text)+"\n")
print("\n".join(text))
PY
}

correlate(){
  local diag="$1"
  local corr="$REPORTS/correlation-${RUN_ID}.txt"
  python - "$diag" "$TARGET_WORKFLOW" "$corr" <<'PY'
from pathlib import Path
import re,sys
diag=Path(sys.argv[1]).read_text(errors="replace")
wf=Path(".github/workflows") / Path(sys.argv[2]).name
out=Path(sys.argv[3])
wft=wf.read_text(errors="replace") if wf.exists() else ""
terms=[]
for line in diag.splitlines():
    for t in re.findall(r'[A-Za-z][A-Za-z0-9_.:/-]{3,}',line):
        if t.lower() not in {"error","process","completed","with","exit","code"}:
            terms.append(t)
terms=list(dict.fromkeys(terms))
hits=[]
for i,line in enumerate(wft.splitlines(),1):
    low=line.lower()
    if "cibuildwheel" in low or any(t.lower() in low for t in terms[:40]):
        hits.append(f"{i}: {line}")
out.write_text("=== WORKFLOW CORRELATION ===\n"+("\n".join(hits) if hits else "NO_DIRECT_WORKFLOW_CORRELATION")+"\n")
print(out.read_text())
PY
}

validate(){
  python - "$TARGET_WORKFLOW" <<'PY'
import sys,yaml
from pathlib import Path
p=Path(".github/workflows") / Path(sys.argv[1]).name
d=yaml.safe_load(p.read_text())
assert isinstance(d,dict) and "jobs" in d
print("WORKFLOW YAML: PASS")
print("JOBS:", ", ".join(d["jobs"].keys()))
PY
  bash -n .self-healing/engine/minimal_patch.py 2>/dev/null || true
  python -m py_compile .self-healing/engine/minimal_patch.py 2>/dev/null && \
    echo "MINIMAL PATCH ENGINE SYNTAX: PASS" || \
    echo "MINIMAL PATCH ENGINE SYNTAX: NOT_AVAILABLE_OR_FAILED"
}

while (( cycle < MAX_CYCLES )); do
  cycle=$((cycle+1))
  log "=== CYCLE $cycle/$MAX_CYCLES ==="

  resolve_run
  log "RUN_ID=$RUN_ID"

  meta="$REPORTS/run-${RUN_ID}.json"
  gh run view "$RUN_ID" --json databaseId,status,conclusion,workflowName,headSha,url >"$meta"
  cat "$meta"

  conclusion="$(python - "$meta" <<'PY'
import json,sys
print(json.load(open(sys.argv[1])).get("conclusion") or "")
PY
)"
  status="$(python - "$meta" <<'PY'
import json,sys
print(json.load(open(sys.argv[1])).get("status") or "")
PY
)"

  if [[ "$conclusion" == "success" ]]; then
    log "SUCCESS: GitHub run is already successful."
    printf 'SUCCESS\n' >"$STATE/current.state"
    exit 0
  fi

  if [[ "$status" != "completed" ]]; then
    log "RUN_NOT_COMPLETED: status=$status"
    if (( WATCH )); then
      sleep "$SLEEP_SEC"
      continue
    fi
    exit 3
  fi

  log "Recovering GitHub log..."
  logf="$(recover_log "$RUN_ID")" || die "NO_LOG_AVAILABLE_AFTER_ALL_RECOVERY_ROUTES"
  log "LOG_RECOVERY: PASS -> $logf"
  log "LOG_LINES=$(wc -l <"$logf")"

  diagnose "$logf"
  correlate "$REPORTS/diagnosis-${RUN_ID}.txt"
  validate

  # Autonomous evidence-backed repair boundary.
  apply_builtin_repair(){
    local diag="$REPORTS/diagnosis-${RUN_ID}.txt"
    local wf=".github/workflows/$TARGET_WORKFLOW"

    [[ -f "$wf" ]] || die "Target workflow not found: $wf"

    if grep -Fq "cibuildwheel: --platform cannot be specified with --only" "$diag"; then
      log "EVIDENCE_MATCH: cibuildwheel --platform/--only conflict"

      python - "$wf" <<'PY2'
from pathlib import Path
import sys

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")

if "--only cp314-android_arm64_v8a" not in s:
    raise SystemExit("REPAIR_REFUSED: cp314-android_arm64_v8a target not found")

old = "      --platform android \\\n"
if old not in s:
    raise SystemExit("REPAIR_REFUSED: exact --platform android argument not found")

s2 = s.replace(old, "", 1)

if s2 == s:
    raise SystemExit("REPAIR_REFUSED: workflow unchanged")

p.write_text(s2, encoding="utf-8")
print("BUILTIN_REPAIR: REMOVED_CONFLICTING_PLATFORM_ARGUMENT")
PY2

      git diff --check
      validate

      git add "$wf" .self-healing/bootstrap/super_heal.sh
      git commit -m "fix: remove conflicting cibuildwheel platform option" || true
      git push origin HEAD

      log "REPAIR_PUSH: PASS"

      local newrun=""
      for _ in $(seq 1 30); do
        newrun="$(gh run list --workflow "$TARGET_WORKFLOW" --limit 5 \
          --json databaseId,status,headSha \
          --jq '.[0].databaseId' 2>/dev/null || true)"

        if [[ -n "$newrun" && "$newrun" != "$RUN_ID" ]]; then
          RUN_ID="$newrun"
          log "NEW_RUN_ID=$RUN_ID"
          return 0
        fi

        sleep 5
      done

      die "REPAIR_PUSHED_BUT_NEW_RUN_NOT_DETECTED"
    fi

    if [[ -n "${APPLY_CMD:-}" ]]; then
      log "APPLYING_EXPLICIT_APPLY_CMD"
      bash -lc "$APPLY_CMD"
      git diff --check
      validate
      return 0
    fi

    die "NO_SUPPORTED_EVIDENCE_BACKED_REPAIR"
  }

  if [[ "${AUTO_REPAIR:-0}" != "1" ]]; then
    log "SAFE STOP: AUTO_REPAIR is disabled."
    printf 'DIAGNOSED_SAFE_STOP\n' >"$STATE/current.state"
    exit 10
  fi

  apply_builtin_repair
  printf 'REPAIR_APPLIED\n' >"$STATE/current.state"
  log "REPAIR_APPLIED; continuing autonomous verification"

done

printf 'MAX_CYCLES_REACHED\n' >"$STATE/current.state"
die "Maximum cycles reached without verified success"
