#!/data/data/com.termux/files/usr/bin/bash

# SUPER PLATFORM AGENT POLICY

is_allowed() {
    case "$1" in
        system|network|wifi|storage|status)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}
