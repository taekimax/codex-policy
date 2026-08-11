#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-${HOME}/.codex}"
RUNTIME_ROOT="${LOCAL_DOCUMENT_RUNTIME_ROOT:-${CODEX_HOME_DIR}/runtimes/local-document-extraction}"
PYTHON_BIN="${LOCAL_DOCUMENT_DOCLING_PYTHON:-${RUNTIME_ROOT}/docling/bin/python}"
ARTIFACTS_PATH="${DOCLING_ARTIFACTS_PATH:-${RUNTIME_ROOT}/docling-models}"
MANIFEST_PATH="${RUNTIME_ROOT}/runtime-manifest.json"
REVIEWED_VERSION="2.119.0"
CONVERTER="${SCRIPT_DIR}/extract_docling.py"

runtime_check() {
  if [[ ! -x "${PYTHON_BIN}" ]]; then
    echo '{"ready":false,"reason":"missing isolated Docling runtime"}'
    return 78
  fi
  "${PYTHON_BIN}" - "${REVIEWED_VERSION}" "${ARTIFACTS_PATH}" "${MANIFEST_PATH}" <<'PY'
import json
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

reviewed = sys.argv[1]
artifacts = Path(sys.argv[2])
manifest_path = Path(sys.argv[3])
try:
    installed = version("docling")
except PackageNotFoundError:
    installed = None
try:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
except Exception:
    manifest = None
manifest_ready = (
    isinstance(manifest, dict)
    and manifest.get("schema") == 1
    and manifest.get("docling") == reviewed
    and manifest.get("pymupdf") == "1.28.2"
    and manifest.get("pymupdf4llm") == "1.28.2"
)
artifacts_ready = artifacts.is_dir() and any(artifacts.iterdir())
python_ready = sys.version_info >= (3, 10)
version_ready = installed == reviewed
ready = python_ready and version_ready and artifacts_ready and manifest_ready
payload = {
    "ready": ready,
    "python_version": ".".join(map(str, sys.version_info[:3])),
    "python_ready": python_ready,
    "docling": installed,
    "reviewed_docling": reviewed,
    "version_ready": version_ready,
    "artifacts_ready": artifacts_ready,
    "manifest_ready": manifest_ready,
    "offline": True,
    "remote_services": False,
    "external_plugins": False,
}
print(json.dumps(payload, sort_keys=True))
raise SystemExit(0 if ready else 78)
PY
}

if [[ "${1:-}" == "--runtime-check" ]]; then
  runtime_check
  exit $?
fi

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    exec python3 "${CONVERTER}" "$@"
  fi
  exec python "${CONVERTER}" "$@"
fi

runtime_check >/dev/null || {
  echo "[local-document-extraction] Docling runtime check failed" >&2
  exit 78
}

export DOCLING_ARTIFACTS_PATH="${ARTIFACTS_PATH}"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
unset HF_TOKEN HUGGING_FACE_HUB_TOKEN || true
unset OPENAI_API_KEY ANTHROPIC_API_KEY GOOGLE_API_KEY GEMINI_API_KEY AZURE_OPENAI_API_KEY || true
exec "${PYTHON_BIN}" "${CONVERTER}" "$@"
