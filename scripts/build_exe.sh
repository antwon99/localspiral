#!/usr/bin/env bash
# Build a standalone localspiral binary using PyInstaller.
set -e
PYINSTALLER=$(python - <<'PY'
try:
    import PyInstaller  # noqa: F401
    print('ok')
except ImportError:
    print('missing')
PY)
if [ "$PYINSTALLER" = "missing" ]; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi
pyinstaller --onefile -n localspiral -m localspiral

