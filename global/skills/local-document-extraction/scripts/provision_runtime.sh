#!/usr/bin/env bash
set -euo pipefail

if [[ "${1:-}" != "--yes" || "$#" -ne 1 ]]; then
  echo "usage: provision_runtime.sh --yes" >&2
  echo "This performs networked package and model installation into an isolated Codex runtime." >&2
  exit 64
fi

CODEX_HOME_DIR="${CODEX_HOME:-${HOME}/.codex}"
RUNTIME_ROOT="${LOCAL_DOCUMENT_RUNTIME_ROOT:-${CODEX_HOME_DIR}/runtimes/local-document-extraction}"
RUNTIME_PARENT="$(dirname "${RUNTIME_ROOT}")"
UV_BIN="${LOCAL_DOCUMENT_UV:-$(command -v uv || true)}"

if [[ -z "${UV_BIN}" || ! -x "${UV_BIN}" ]]; then
  echo "[local-document-extraction] uv is required for isolated provisioning" >&2
  exit 78
fi
if [[ -e "${RUNTIME_ROOT}" ]]; then
  echo "[local-document-extraction] runtime already exists; preserve or remove it explicitly before reprovisioning" >&2
  exit 73
fi

BOOTSTRAP_PYTHON="${LOCAL_DOCUMENT_BOOTSTRAP_PYTHON:-}"
if [[ -z "${BOOTSTRAP_PYTHON}" ]]; then
  for candidate in python3.12 python3.11 python3.10; do
    if command -v "${candidate}" >/dev/null 2>&1; then
      BOOTSTRAP_PYTHON="$(command -v "${candidate}")"
      break
    fi
  done
fi
if [[ -z "${BOOTSTRAP_PYTHON}" || ! -x "${BOOTSTRAP_PYTHON}" ]]; then
  echo "[local-document-extraction] an existing Python 3.10-3.12 interpreter is required" >&2
  exit 78
fi
"${BOOTSTRAP_PYTHON}" - <<'PY'
import sys
if not (3, 10) <= sys.version_info[:2] <= (3, 12):
    raise SystemExit("bootstrap Python must be 3.10, 3.11, or 3.12")
PY

mkdir -p "${RUNTIME_PARENT}"
STAGING_ROOT="$(mktemp -d "${RUNTIME_PARENT}/.local-document-extraction.stage.XXXXXX")"
cleanup() {
  if [[ -n "${STAGING_ROOT:-}" && -d "${STAGING_ROOT}" ]]; then
    rm -rf -- "${STAGING_ROOT}"
  fi
}
trap cleanup EXIT

"${UV_BIN}" venv --no-config --python "${BOOTSTRAP_PYTHON}" "${STAGING_ROOT}/ocr"
env -u UV_INDEX -u UV_DEFAULT_INDEX -u UV_INDEX_URL -u UV_EXTRA_INDEX_URL \
  -u PIP_INDEX_URL -u PIP_EXTRA_INDEX_URL \
  "${UV_BIN}" pip install --no-config --default-index https://pypi.org/simple \
  --python "${STAGING_ROOT}/ocr/bin/python" \
  "PyMuPDF==1.28.2" "pymupdf4llm==1.28.2"
"${STAGING_ROOT}/ocr/bin/python" - <<'PY'
from importlib.metadata import version
if version("PyMuPDF") != "1.28.2" or version("pymupdf4llm") != "1.28.2":
    raise SystemExit("reviewed OCR package versions were not installed")
PY

"${UV_BIN}" venv --no-config --python "${BOOTSTRAP_PYTHON}" "${STAGING_ROOT}/docling"
env -u UV_INDEX -u UV_DEFAULT_INDEX -u UV_INDEX_URL -u UV_EXTRA_INDEX_URL \
  -u PIP_INDEX_URL -u PIP_EXTRA_INDEX_URL \
  "${UV_BIN}" pip install --no-config --default-index https://pypi.org/simple \
  --python "${STAGING_ROOT}/docling/bin/python" "docling==2.119.0"
"${STAGING_ROOT}/docling/bin/python" - <<'PY'
from importlib.metadata import version
if version("docling") != "2.119.0":
    raise SystemExit("reviewed Docling version was not installed")
PY
env -u HF_TOKEN -u HUGGING_FACE_HUB_TOKEN HF_HUB_DISABLE_TELEMETRY=1 \
  "${STAGING_ROOT}/docling/bin/docling-tools" models download \
  --output-dir "${STAGING_ROOT}/docling-models"

"${STAGING_ROOT}/docling/bin/python" - \
  "${STAGING_ROOT}" "${STAGING_ROOT}/runtime-manifest.json" "${UV_BIN}" <<'PY'
import hashlib
import json
from importlib.metadata import version
from pathlib import Path
import platform
import subprocess
import sys

root = Path(sys.argv[1])
manifest_path = Path(sys.argv[2])
uv = sys.argv[3]
freeze = subprocess.run(
    [uv, "pip", "freeze", "--no-config", "--python", str(root / "docling" / "bin" / "python")],
    check=True,
    capture_output=True,
    text=True,
).stdout
(root / "docling-freeze.txt").write_text(freeze, encoding="utf-8")
ocr_freeze = subprocess.run(
    [uv, "pip", "freeze", "--no-config", "--python", str(root / "ocr" / "bin" / "python")],
    check=True,
    capture_output=True,
    text=True,
).stdout
(root / "ocr-freeze.txt").write_text(ocr_freeze, encoding="utf-8")
payload = {
    "schema": 1,
    "python": platform.python_version(),
    "platform": platform.platform(),
    "pymupdf": "1.28.2",
    "pymupdf4llm": "1.28.2",
    "docling": version("docling"),
    "ocr_freeze_sha256": hashlib.sha256(ocr_freeze.encode()).hexdigest(),
    "docling_freeze_sha256": hashlib.sha256(freeze.encode()).hexdigest(),
    "models_prefetched": True,
    "package_index": "https://pypi.org/simple",
    "model_source": "docling-tools default official set",
    "remote_services": False,
    "external_plugins": False,
}
manifest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
PY

mv "${STAGING_ROOT}" "${RUNTIME_ROOT}"
STAGING_ROOT=""
trap - EXIT
echo "[local-document-extraction] isolated runtime provisioned"
if command -v tesseract >/dev/null 2>&1; then
  tesseract --list-langs 2>/dev/null || true
else
  echo "[local-document-extraction] Tesseract is not installed; native extraction works but OCR does not" >&2
fi
