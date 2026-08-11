#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CODEX_HOME_DIR="${CODEX_HOME:-${HOME}/.codex}"
RUNTIME_ROOT="${LOCAL_DOCUMENT_RUNTIME_ROOT:-${CODEX_HOME_DIR}/runtimes/local-document-extraction}"
PYTHON_BIN="${LOCAL_DOCUMENT_OCR_PYTHON:-${RUNTIME_ROOT}/ocr/bin/python}"

if [[ ! -x "${PYTHON_BIN}" ]]; then
  echo "[local-document-extraction] missing isolated OCR runtime" >&2
  exit 78
fi

if [[ -z "${TESSDATA_PREFIX:-}" ]]; then
  for candidate in \
    /opt/homebrew/share/tessdata \
    /usr/local/share/tessdata \
    /usr/share/tesseract-ocr/5/tessdata \
    /usr/share/tesseract-ocr/4.00/tessdata \
    /usr/share/tesseract/tessdata
  do
    if [[ -d "${candidate}" ]]; then
      export TESSDATA_PREFIX="${candidate}"
      break
    fi
  done
fi

exec "${PYTHON_BIN}" "${SCRIPT_DIR}/extract_ocr.py" "$@"
