#!/usr/bin/env bash
# HermiEditor Linux/macOS Quick Setup
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "=== Setting up HermiEditor for Hermes Agent ==="

# Check Node.js
if ! command -v node >/dev/null 2>&1; then
    echo "Node.js is required. Please install Node.js 18+ (https://nodejs.org)."
    exit 1
fi

# Run Node setup
node setup.mjs
