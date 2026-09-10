#!/data/data/com.termux/files/usr/bin/bash

BASE="$HOME/SuperPlatform/agent"

source "$BASE/policy.sh"
source "$BASE/logger.sh"
source "$BASE/executor.sh"

task="$*"

if [ -z "$task" ]; then
    echo "Usage: agent.sh <task>"
    exit 1
fi

case "$task" in
    system|system\ status)
        module="system"
        ;;
    network|network\ status|ip)
        module="network"
        ;;
    wifi|wifi\ status)
        module="wifi"
        ;;
    storage|storage\ status)
        module="storage"
        ;;
    status|agent\ status)
        module="status"
        ;;
    *)
        echo "Task not supported by current policy."
        echo "Supported: system, network, wifi, storage, status"
        exit 2
        ;;
esac

if ! is_allowed "$module"; then
    echo "BLOCKED BY POLICY"
    log_event "BLOCKED task=$task module=$module"
    exit 3
fi

log_event "START task=$task module=$module"

execute_task "$module"
result=$?

log_event "END task=$task module=$module result=$result"

exit "$result"
