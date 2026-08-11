#!/usr/bin/env python3
"""Extract text, Markdown, tables, images, or metadata from a local PDF or image."""

from __future__ import annotations

import argparse
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import List, Optional


REVIEWED_PYMUPDF_VERSION = "1.28.2"
REVIEWED_PYMUPDF4LLM_VERSION = "1.28.2"
DEFAULT_MAX_FILE_MB = 512.0
DEFAULT_MAX_PAGES = 1000


def package_version(name: str) -> Optional[str]:
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def tesseract_languages(binary: Optional[str]) -> List[str]:
    if not binary:
        return []
    try:
        result = subprocess.run(
            [binary, "--list-langs"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return []
    if result.returncode != 0:
        return []
    lines = [line.strip() for line in result.stdout.splitlines()]
    return sorted(line for line in lines if line and "available languages" not in line)


def requested_languages(value: str) -> List[str]:
    languages = [part.strip() for part in value.split("+") if part.strip()]
    if not languages:
        raise argparse.ArgumentTypeError("at least one OCR language is required")
    return languages


def runtime_status(ocr_language: str) -> dict:
    pymupdf_version = package_version("PyMuPDF")
    pymupdf4llm_version = package_version("pymupdf4llm")
    tesseract = shutil.which("tesseract")
    languages = tesseract_languages(tesseract)
    requested = requested_languages(ocr_language)
    missing_languages = sorted(set(requested) - set(languages))
    return {
        "ready": pymupdf_version == REVIEWED_PYMUPDF_VERSION,
        "pymupdf": pymupdf_version,
        "reviewed_pymupdf": REVIEWED_PYMUPDF_VERSION,
        "markdown_ready": pymupdf4llm_version == REVIEWED_PYMUPDF4LLM_VERSION,
        "pymupdf4llm": pymupdf4llm_version,
        "reviewed_pymupdf4llm": REVIEWED_PYMUPDF4LLM_VERSION,
        "tesseract": tesseract,
        "ocr_languages": languages,
        "requested_ocr_languages": requested,
        "missing_ocr_languages": missing_languages,
        "ocr_ready": bool(tesseract) and not missing_languages,
    }


def parse_pages(value: str) -> List[int]:
    pages = set()
    for part in value.split(","):
        item = part.strip()
        if not item:
            continue
        if "-" in item:
            start_text, end_text = item.split("-", 1)
            start, end = int(start_text), int(end_text)
            if start < 0 or end < start:
                raise argparse.ArgumentTypeError(
                    "page ranges must be non-negative and ascending"
                )
            pages.update(range(start, end + 1))
        else:
            page = int(item)
            if page < 0:
                raise argparse.ArgumentTypeError("page numbers must be non-negative")
            pages.add(page)
    if not pages:
        raise argparse.ArgumentTypeError("at least one page is required")
    return sorted(pages)


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return parsed


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument("input", nargs="?", type=Path)
    result.add_argument("--check", action="store_true", help="report runtime readiness only")
    result.add_argument(
        "--require-ocr",
        action="store_true",
        help="make OCR readiness part of --check",
    )
    result.add_argument("--markdown", action="store_true")
    result.add_argument("--tables", action="store_true")
    result.add_argument("--images", type=Path, metavar="DIR")
    result.add_argument("--overwrite", action="store_true")
    result.add_argument("--metadata", action="store_true")
    result.add_argument("--pages", type=parse_pages, help="zero-based pages, e.g. 0-4,7")
    result.add_argument("--ocr-mode", choices=("off", "auto", "force"), default="off")
    result.add_argument("--ocr-language", default="eng", help="Tesseract codes, e.g. kor+eng")
    result.add_argument("--ocr-dpi", type=int, default=300)
    result.add_argument("--tessdata", type=Path)
    result.add_argument("--max-file-mb", type=float, default=DEFAULT_MAX_FILE_MB)
    result.add_argument("--max-pages", type=positive_int, default=DEFAULT_MAX_PAGES)
    return result


def validate_input(args: argparse.Namespace) -> Path:
    if args.input is None:
        raise ValueError("INPUT is required unless --check is used")
    raw = str(args.input)
    if "://" in raw:
        raise ValueError("remote URLs are not accepted; download to a local staging path first")
    path = args.input.expanduser()
    if not path.is_file():
        raise ValueError("input is not a readable regular file: {}".format(path))
    if args.max_file_mb <= 0:
        raise ValueError("--max-file-mb must be greater than zero")
    if path.stat().st_size > args.max_file_mb * 1024 * 1024:
        raise ValueError("input exceeds --max-file-mb={:g}".format(args.max_file_mb))
    if not 72 <= args.ocr_dpi <= 600:
        raise ValueError("--ocr-dpi must be between 72 and 600")
    actions = sum(bool(value) for value in (args.markdown, args.tables, args.images, args.metadata))
    if actions > 1:
        raise ValueError("choose only one of --markdown, --tables, --images, or --metadata")
    if args.ocr_mode != "off" and (args.tables or args.images or args.metadata):
        raise ValueError("--ocr-mode applies only to text or Markdown extraction")
    if args.images and args.images.exists():
        if not args.images.is_dir() or args.images.is_symlink():
            raise ValueError("image output must be a real directory")
        if any(args.images.iterdir()) and not args.overwrite:
            raise ValueError("image output directory is not empty; use a new directory or --overwrite")
    return path


def selected_pages(doc, pages: Optional[List[int]], max_pages: int) -> List[int]:
    selected = list(range(len(doc))) if pages is None else pages
    invalid = [page for page in selected if page >= len(doc)]
    if invalid:
        raise ValueError("page indexes out of range for {} pages: {}".format(len(doc), invalid))
    if len(selected) > max_pages:
        raise ValueError("selected pages exceed --max-pages={}".format(max_pages))
    return selected


def ocr_text(page, mode: str, language: str, dpi: int, tessdata: Optional[Path]) -> str:
    native = page.get_text()
    if mode == "off" or (mode == "auto" and native.strip()):
        return native
    kwargs = {"language": language, "dpi": dpi, "full": mode == "force"}
    if tessdata is not None:
        kwargs["tessdata"] = str(tessdata)
    text_page = page.get_textpage_ocr(**kwargs)
    return page.get_text(textpage=text_page)


def extract_text(path: Path, pages: Optional[List[int]], args: argparse.Namespace) -> None:
    import pymupdf

    with pymupdf.open(path) as doc:
        for page_index in selected_pages(doc, pages, args.max_pages):
            print("\n--- Page {}/{} ---\n".format(page_index + 1, len(doc)))
            print(
                ocr_text(
                    doc[page_index],
                    args.ocr_mode,
                    args.ocr_language,
                    args.ocr_dpi,
                    args.tessdata,
                )
            )


def extract_markdown(path: Path, pages: Optional[List[int]], args: argparse.Namespace) -> None:
    import pymupdf
    import pymupdf4llm

    with pymupdf.open(path) as doc:
        selected = selected_pages(doc, pages, args.max_pages)
    markdown = pymupdf4llm.to_markdown(
        str(path),
        pages=selected,
        use_ocr=args.ocr_mode != "off",
        force_ocr=args.ocr_mode == "force",
        ocr_language=args.ocr_language,
        ocr_dpi=args.ocr_dpi,
    )
    print(markdown)


def extract_tables(path: Path, pages: Optional[List[int]], max_pages: int) -> None:
    import pymupdf

    with pymupdf.open(path) as doc:
        for page_index in selected_pages(doc, pages, max_pages):
            tables = doc[page_index].find_tables()
            for table_index, table in enumerate(tables.tables, 1):
                print("\n--- Page {}, Table {} ---\n".format(page_index + 1, table_index))
                print(table.to_markdown())


def extract_images(
    path: Path,
    output_dir: Path,
    pages: Optional[List[int]],
    max_pages: int,
) -> None:
    import pymupdf

    output_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    with pymupdf.open(path) as doc:
        for page_index in selected_pages(doc, pages, max_pages):
            for image_index, image in enumerate(doc[page_index].get_images(full=True), 1):
                pixmap = pymupdf.Pixmap(doc, image[0])
                if pixmap.n >= 5:
                    pixmap = pymupdf.Pixmap(pymupdf.csRGB, pixmap)
                output = output_dir / "page{}_img{}.png".format(page_index + 1, image_index)
                pixmap.save(output)
                count += 1
    print(json.dumps({"images": count, "output_dir": str(output_dir)}, sort_keys=True))


def show_metadata(path: Path) -> None:
    import pymupdf

    with pymupdf.open(path) as doc:
        metadata = doc.metadata or {}
        payload = {
            "pages": len(doc),
            **{
                key: metadata.get(key, "")
                for key in ("title", "author", "subject", "creator", "producer", "format")
            },
        }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


def main(argv: Optional[List[str]] = None) -> int:
    args = parser().parse_args(argv)
    try:
        status = runtime_status(args.ocr_language)
    except argparse.ArgumentTypeError as exc:
        print(str(exc), file=sys.stderr)
        return 64
    if args.check:
        print(json.dumps(status, ensure_ascii=False, sort_keys=True))
        ready = bool(status["ready"]) and (not args.require_ocr or bool(status["ocr_ready"]))
        return 0 if ready else 78

    try:
        path = validate_input(args)
        if not status["ready"]:
            raise RuntimeError("reviewed PyMuPDF {} is unavailable".format(REVIEWED_PYMUPDF_VERSION))
        if args.markdown and not status["markdown_ready"]:
            raise RuntimeError(
                "reviewed PyMuPDF4LLM {} is unavailable".format(REVIEWED_PYMUPDF4LLM_VERSION)
            )
        if args.ocr_mode != "off" and not status["ocr_ready"]:
            missing = ", ".join(status["missing_ocr_languages"]) or "Tesseract"
            raise RuntimeError("requested local OCR runtime is unavailable: {}".format(missing))

        if args.metadata:
            show_metadata(path)
        elif args.tables:
            extract_tables(path, args.pages, args.max_pages)
        elif args.images:
            extract_images(path, args.images, args.pages, args.max_pages)
        elif args.markdown:
            extract_markdown(path, args.pages, args)
        else:
            extract_text(path, args.pages, args)
    except (OSError, RuntimeError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 78 if isinstance(exc, RuntimeError) else 64
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
