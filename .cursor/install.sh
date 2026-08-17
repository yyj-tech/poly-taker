#!/usr/bin/env bash
# Idempotent dependency setup for poly-taker.
#
# Ubuntu 24.04 marks the system Python as externally managed (PEP 668), so we install
# into a project-local virtual environment. Re-running this script is safe: the venv is
# reused and pip only updates what changed.
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python3}"
VENV_DIR=".venv"

# The default image's system Python may ship without the venv/ensurepip module.
# Install it once (baked into the environment snapshot) if it is missing.
if ! "${PYTHON}" -c "import ensurepip" >/dev/null 2>&1; then
  echo "Installing python venv support via apt ..."
  PY_MINOR="$("${PYTHON}" -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
  sudo apt-get update -y
  sudo apt-get install -y --no-install-recommends "python${PY_MINOR}-venv"
fi

if [ ! -x "${VENV_DIR}/bin/python" ]; then
  echo "Creating virtual environment in ${VENV_DIR} ..."
  "${PYTHON}" -m venv "${VENV_DIR}"
fi

# shellcheck disable=SC1091
source "${VENV_DIR}/bin/activate"

python -m pip install --upgrade pip
python -m pip install -e ".[dev]"

echo "poly-taker install complete. Activate with: source ${VENV_DIR}/bin/activate"
