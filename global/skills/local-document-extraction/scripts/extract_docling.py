#!/usr/bin/env python3
"""Convert local documents into structured output with an offline Docling runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from typing import Iterable, List, Optional, Sequence


FORMATS = {
    "markdown": ("markdown", ".md"),
    "md": ("markdown", ".md"),
    "json": ("json", ".json"),
    "text": ("text", ".txt"),
    "txt": ("text", ".txt"),
    "html": ("html", ".html"),
    "doctags": ("doctags", ".doctags"),
}
DEFAULT_MAX_FILE_MB = 512.0
DEFAULT_MAX_PAGES = 1000


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def positive_float(value: str) -> float:
    parsed = float(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def normalize_format(value: str) -> tuple:
    try:
        return FORMATS[value.strip().lower()]
    except KeyError as exc:
        raise ValueError("unsupported output format: {}".format(value)) from exc


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("--input", action="append", required=True, help="local file; repeat for a batch")
    result.add_argument("--out", required=True, type=Path, help="new or existing real output directory")
    result.add_argument("--format", default="markdown", choices=sorted(FORMATS))
    result.add_argument("--from", dest="from_formats", action="append")
    result.add_argument("--manifest", type=Path)
    result.add_argument("--overwrite", action="store_true")
    result.add_argument("--continue-on-error", action="store_true")
    result.add_argument("--max-file-size-mb", type=positive_float, default=DEFAULT_MAX_FILE_MB)
    result.add_argument("--max-pages", type=positive_int, default=DEFAULT_MAX_PAGES)
    result.add_argument("--document-timeout", type=positive_float)
    result.add_argument("--num-threads", type=positive_int)
    result.add_argument("--device", choices=("auto", "cpu", "cuda", "mps", "xpu"))
    return result


def unique_sources(values: Iterable[str]) -> List[Path]:
    result = []
    seen = set()
    for value in values:
        if "://" in value:
            raise ValueError("remote URLs are not accepted; download to a local staging path first")
        path = Path(value).expanduser()
        if not path.is_file():
            raise ValueError("input is not a readable regular file: {}".format(path))
        resolved = path.resolve()
        key = str(resolved)
        if key not in seen:
            seen.add(key)
            result.append(resolved)
    return result


def validate_output_dir(path: Path) -> Path:
    expanded = path.expanduser()
    if expanded.exists():
        if expanded.is_symlink() or not expanded.is_dir():
            raise ValueError("output must be a real directory")
    return expanded.resolve()


def slug(value: str) -> str:
    normalized = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-._")
    return normalized[:80] or "document"


def output_path(source: Path, output_dir: Path, suffix: str) -> Path:
    identity = hashlib.sha256(str(source).encode("utf-8")).hexdigest()[:8]
    return output_dir / "{}-{}{}".format(slug(source.stem), identity, suffix)


def ensure_available(path: Path, overwrite: bool) -> None:
    if path.exists() and not overwrite:
        raise ValueError("output already exists; use a new directory or --overwrite: {}".format(path))


def atomic_write_text(path: Path, text: str) -> None:
    descriptor, temporary = tempfile.mkstemp(prefix=".local-document-", dir=str(path.parent))
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            os.unlink(temporary)
        except OSError:
            pass
        raise


def export_document(document, output_format: str) -> str:
    if output_format == "markdown":
        return document.export_to_markdown()
    if output_format == "json":
        return json.dumps(document.export_to_dict(), ensure_ascii=False, indent=2)
    if output_format == "text":
        return document.export_to_text()
    if output_format == "html":
        return document.export_to_html()
    if output_format == "doctags":
        return document.export_to_doctags()
    raise ValueError("unsupported output format: {}".format(output_format))


def parse_input_formats(values: Optional[Sequence[str]]):
    if not values:
        return None
    from docling.datamodel.base_models import InputFormat

    aliases = {
        "markdown": "md",
        "jpg": "image",
        "jpeg": "image",
        "png": "image",
        "tiff": "image",
        "txt": "md",
    }
    by_value = {item.value: item for item in InputFormat}
    selected = []
    seen = set()
    for raw in values:
        for part in raw.split(","):
            name = aliases.get(part.strip().lower(), part.strip().lower())
            if not name:
                continue
            if name not in by_value:
                raise ValueError(
                    "unsupported --from format: {}. Choose: {}".format(
                        part, ", ".join(sorted(by_value))
                    )
                )
            if name not in seen:
                seen.add(name)
                selected.append(by_value[name])
    return selected or None


def build_converter(args: argparse.Namespace):
    from docling.datamodel.accelerator_options import AcceleratorOptions
    from docling.datamodel.base_models import InputFormat
    from docling.datamodel.pipeline_options import PdfPipelineOptions
    from docling.document_converter import DocumentConverter, ImageFormatOption, PdfFormatOption

    pipeline_values = {
        "enable_remote_services": False,
        "allow_external_plugins": False,
    }
    artifacts = os.environ.get("DOCLING_ARTIFACTS_PATH")
    if artifacts:
        pipeline_values["artifacts_path"] = artifacts
    accelerator_values = {}
    if args.num_threads is not None:
        accelerator_values["num_threads"] = args.num_threads
    if args.device is not None:
        accelerator_values["device"] = args.device
    if accelerator_values:
        pipeline_values["accelerator_options"] = AcceleratorOptions(**accelerator_values)
    if args.document_timeout is not None:
        pipeline_values["document_timeout"] = args.document_timeout
    pdf_options = PdfPipelineOptions(**pipeline_values)
    return DocumentConverter(
        allowed_formats=parse_input_formats(args.from_formats),
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_options),
            InputFormat.IMAGE: ImageFormatOption(pipeline_options=pdf_options),
        },
    )


def write_manifest(path: Optional[Path], records: List[dict], overwrite: bool) -> None:
    if path is None:
        return
    if path.exists() and not overwrite:
        raise ValueError("manifest already exists; use a new path or --overwrite: {}".format(path))
    if path.exists() and path.is_symlink():
        raise ValueError("manifest cannot be a symlink")
    path.parent.mkdir(parents=True, exist_ok=True)
    atomic_write_text(path, json.dumps(records, ensure_ascii=False, indent=2) + "\n")


def main(argv: Optional[List[str]] = None) -> int:
    args = parser().parse_args(argv)
    try:
        output_format, suffix = normalize_format(args.format)
        sources = unique_sources(args.input)
        output_dir = validate_output_dir(args.out)
        manifest_path = args.manifest.expanduser() if args.manifest else None
        max_file_size = int(args.max_file_size_mb * 1024 * 1024)
        for source in sources:
            if source.stat().st_size > max_file_size:
                raise ValueError(
                    "input exceeds --max-file-size-mb={:g}: {}".format(
                        args.max_file_size_mb, source
                    )
                )
        destinations = [output_path(source, output_dir, suffix) for source in sources]
        if len(set(destinations)) != len(destinations):
            raise ValueError("selected inputs resolve to colliding output names")
        for destination in destinations:
            ensure_available(destination, args.overwrite)
        if manifest_path is not None:
            if manifest_path.resolve() in destinations:
                raise ValueError("manifest path collides with a document output")
            ensure_available(manifest_path, args.overwrite)
    except (OSError, ValueError) as exc:
        print("ERROR: {}".format(exc), file=sys.stderr)
        return 64

    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    try:
        converter = build_converter(args)
    except Exception as exc:
        print("ERROR: pinned offline Docling failed to initialize: {}".format(exc), file=sys.stderr)
        return 78
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        print("ERROR: unable to create output directory: {}".format(exc), file=sys.stderr)
        return 64

    records = []
    for index, (source, destination) in enumerate(zip(sources, destinations), 1):
        started = time.monotonic()
        record = {
            "source": str(source),
            "output": str(destination),
            "index": index,
            "engine": "docling",
            "status": "ok",
        }
        try:
            converted = converter.convert(
                str(source),
                max_num_pages=args.max_pages,
                max_file_size=max_file_size,
            )
            atomic_write_text(destination, export_document(converted.document, output_format))
        except Exception as exc:
            record["status"] = "error"
            record["error"] = str(exc)
        record["elapsed_ms"] = int((time.monotonic() - started) * 1000)
        records.append(record)
        if record["status"] == "error" and not args.continue_on_error:
            try:
                write_manifest(manifest_path, records, args.overwrite)
            except (OSError, ValueError) as manifest_exc:
                print("ERROR: {}".format(manifest_exc), file=sys.stderr)
                return 64
            print("ERROR: {}".format(record["error"]), file=sys.stderr)
            return 1

    try:
        write_manifest(manifest_path, records, args.overwrite)
    except (OSError, ValueError) as exc:
        print("ERROR: {}".format(exc), file=sys.stderr)
        return 64
    summary = {
        "total": len(records),
        "ok": sum(1 for item in records if item["status"] == "ok"),
        "errors": sum(1 for item in records if item["status"] == "error"),
    }
    print(json.dumps(summary, sort_keys=True))
    return 1 if summary["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
