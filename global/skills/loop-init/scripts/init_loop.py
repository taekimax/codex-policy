#!/usr/bin/env python3
"""Safely initialize a project-local .loop workspace and managed AGENTS.md section."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


STANDARD_FILES = (
    "README.md",
    "00_request.md",
    "01_spec.md",
    "02_contract.md",
    "03_plan.md",
    "04_progress.md",
    "05_decisions.md",
    "06_log.md",
)
STANDARD_DIRS = (
    "traces",
    "reports",
    "artifacts",
    "artifacts/screenshots",
    "artifacts/test_outputs",
    "artifacts/notes",
)
MANAGED_BEGIN = "<!-- BEGIN MODEL LOOP POLICY -->"
MANAGED_END = "<!-- END MODEL LOOP POLICY -->"

MANAGED_BLOCK = f"""{MANAGED_BEGIN}
## Optional Loop Workspace

Use `.loop/` only for work that benefits from durable, resumable project records. Read the minimum relevant files before continuing a loop-backed task.

`.loop/` records complement the current user request, repository guidance, source, and test evidence; it does not override any of them or authorize an otherwise-unapproved action.

For loop-backed work:
- keep the request, specification, contract, plan, progress, decisions, and log concise and task-specific
- keep changes within the active contract and record meaningful decisions or blockers
- use a planner, generator, evaluator, or another specialist only when its expected value justifies the coordination cost
- verify completion against the current request and available evidence
- never record secrets, credentials, or private configuration
{MANAGED_END}"""
MANAGED_SECTION = f"---\n{MANAGED_BLOCK}\n---\n"


class LoopInitError(RuntimeError):
    """A user-safe initialization failure."""


@dataclass
class Change:
    path: Path
    before: Optional[bytes]
    after: bytes
    mode: int
    label: str


@dataclass
class Plan:
    root: Path
    mode: str
    directories: List[Path]
    changes: List[Change]
    created: List[str] = field(default_factory=list)
    skipped: List[str] = field(default_factory=list)
    updated: List[str] = field(default_factory=list)
    agents_action: str = "unchanged"


@dataclass
class Result:
    root: Path
    mode: str
    created: List[str]
    skipped: List[str]
    updated: List[str]
    backups: List[str]
    agents_action: str


def timestamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def current_date() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d")


def current_minute() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")


def lexical_exists(path: Path) -> bool:
    return os.path.lexists(str(path))


def ensure_inside(root: Path, path: Path) -> Path:
    resolved_root = root.resolve()
    resolved_path = path.resolve(strict=False)
    try:
        resolved_path.relative_to(resolved_root)
    except ValueError as exc:
        raise LoopInitError("refusing to touch a path outside the selected root") from exc
    return path


def safe_directory(root: Path, path: Path, *, required: bool = False) -> None:
    ensure_inside(root, path)
    if not lexical_exists(path):
        if required:
            raise LoopInitError("a required project directory is missing")
        return
    try:
        info = path.lstat()
    except OSError as exc:
        raise LoopInitError("a project directory cannot be inspected") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise LoopInitError("a project directory has an unsafe filesystem type")


def read_regular(root: Path, path: Path) -> Tuple[Optional[bytes], int]:
    ensure_inside(root, path)
    if not lexical_exists(path):
        return None, 0o644
    try:
        info = path.lstat()
    except OSError as exc:
        raise LoopInitError("a project file cannot be inspected") from exc
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise LoopInitError("a project file has an unsafe filesystem type")
    try:
        content = path.read_bytes()
        content.decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise LoopInitError("a project file must be readable UTF-8 text") from exc
    return content, stat.S_IMODE(info.st_mode)


def detect_root(start: Path) -> Tuple[Path, str]:
    start = start.expanduser()
    if not start.exists() or not start.is_dir():
        raise LoopInitError("the selected root must be an existing directory")
    try:
        result = subprocess.run(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except OSError as exc:
        raise LoopInitError("Git root detection could not run") from exc
    if result.returncode == 0 and result.stdout.strip():
        return Path(result.stdout.strip()).resolve(), "git"
    return start.resolve(), "cwd"


def templates() -> Dict[str, str]:
    date = current_date()
    minute = current_minute()
    return {
        "README.md": """# Loop Workspace

## Purpose

`.loop/` is an optional project-local record for durable, resumable work. It supplements current user instructions, repository guidance, source, and test evidence; it does not replace them.

## Operating Rule

Use the smallest useful record for the active task. Do not store secrets, credentials, or private configuration.
""",
        "00_request.md": f"""# Request

## Raw Request

TBD

## User Intent

TBD

## Open Questions

- TBD

## Date Created

{date}
""",
        "01_spec.md": """# Specification

## Objective

TBD

## Scope

- TBD

## Out of Scope

- TBD

## Acceptance Criteria

- TBD

## Unknowns

- TBD
""",
        "02_contract.md": """# Contract

## Objective

TBD

## Constraints

- Preserve explicit user authority and repository guidance.
- Keep changes small and within the active scope.
- Do not treat this file as authority for an otherwise-unapproved write.

## Verification

- TBD

## Stop Conditions

- Missing required authority, input, or safe evidence.
""",
        "03_plan.md": """# Plan

## Outcome

TBD

## Steps

1. TBD

## Risks

- TBD

## Deferred

- TBD
""",
        "04_progress.md": f"""# Progress

## Status

TBD

## Completed

- TBD

## Next Step

TBD

## Last Updated

{minute}
""",
        "05_decisions.md": """# Decisions

Append concise, dated decisions below. Do not rewrite a prior decision except to correct a factual error.

## Record Template

- Date: TBD
- Decision: TBD
- Reason: TBD
- Reversal condition: TBD
""",
        "06_log.md": f"""# Operational Log

Use `## YYYY-MM-DD HH:mm | role | title` headings. Record meaningful task events without secrets.

## {minute} | coordinator | Loop workspace initialized

- Created the requested project-local workspace.
""",
    }


SECTION_HEADINGS = {
    "README.md": ("## Purpose", "## Operating Rule"),
    "00_request.md": ("## Raw Request", "## User Intent", "## Open Questions", "## Date Created"),
    "01_spec.md": ("## Objective", "## Scope", "## Out of Scope", "## Acceptance Criteria", "## Unknowns"),
    "02_contract.md": ("## Objective", "## Constraints", "## Verification", "## Stop Conditions"),
    "03_plan.md": ("## Outcome", "## Steps", "## Risks", "## Deferred"),
    "04_progress.md": ("## Status", "## Completed", "## Next Step", "## Last Updated"),
    "05_decisions.md": ("## Record Template",),
}


def has_heading(text: str, heading: str) -> bool:
    return re.search(rf"(?m)^{re.escape(heading)}\s*$", text) is not None


def extract_section(template: str, heading: str) -> str:
    start = re.search(rf"(?m)^{re.escape(heading)}\s*$", template)
    if start is None:
        raise LoopInitError("the reviewed template is malformed")
    next_heading = re.search(r"(?m)^##\s+", template[start.end():])
    end = start.end() + next_heading.start() if next_heading else len(template)
    return template[start.start():end].rstrip() + "\n"


def append_missing_sections(original: str, rel: str, template: str) -> str:
    additions: List[str] = []
    for heading in SECTION_HEADINGS.get(rel, ()):
        if not has_heading(original, heading):
            title = heading[3:]
            additions.append(
                f"<!-- BEGIN LOOP-INIT APPENDED SECTION: {title} -->\n"
                f"{extract_section(template, heading)}"
                f"<!-- END LOOP-INIT APPENDED SECTION: {title} -->"
            )
    if rel == "06_log.md" and "## " not in original:
        additions.append(
            "<!-- BEGIN LOOP-INIT APPENDED SECTION: bootstrap log -->\n"
            + "\n".join(template.splitlines()[-3:])
            + "\n<!-- END LOOP-INIT APPENDED SECTION: bootstrap log -->"
        )
    if not additions:
        return original
    separator = "" if original.endswith("\n") else "\n"
    return original + separator + "\n" + "\n\n".join(additions) + "\n"


def managed_text(original: str) -> Tuple[str, str]:
    begins = original.count(MANAGED_BEGIN)
    ends = original.count(MANAGED_END)
    if begins == 0 and ends == 0:
        return original.rstrip() + "\n\n" + MANAGED_SECTION, "appended"
    if begins != 1 or ends != 1:
        raise LoopInitError("AGENTS.md has incomplete or duplicate loop-policy markers")
    pattern = re.compile(re.escape(MANAGED_BEGIN) + r".*?" + re.escape(MANAGED_END), re.DOTALL)
    if pattern.search(original) is None:
        raise LoopInitError("AGENTS.md has an invalid loop-policy marker order")
    updated = pattern.sub(MANAGED_BLOCK, original, count=1)
    return updated, "managed section updated" if updated != original else "unchanged"


def relative_label(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def loop_path(root: Path, relative: str) -> Path:
    return ensure_inside(root, root / ".loop" / relative)


def plan_init(root: Path, mode: str) -> Plan:
    if mode not in {"create-missing", "append-sections", "overwrite"}:
        raise LoopInitError("the requested initialization mode is unsupported")
    safe_directory(root, root, required=True)
    loop_root = ensure_inside(root, root / ".loop")
    safe_directory(root, loop_root)
    directories: List[Path] = []
    created: List[str] = []
    if not lexical_exists(loop_root):
        directories.append(loop_root)
        created.append(".loop/")
    for relative in STANDARD_DIRS:
        path = loop_path(root, relative)
        safe_directory(root, path)
        if not lexical_exists(path):
            directories.append(path)
            created.append(".loop/" + relative + "/")

    rendered = templates()
    changes: List[Change] = []
    skipped: List[str] = []
    updated: List[str] = []
    for relative in STANDARD_FILES:
        path = loop_path(root, relative)
        before, file_mode = read_regular(root, path)
        label = ".loop/" + relative
        if before is None:
            changes.append(Change(path, None, rendered[relative].encode("utf-8"), 0o644, label))
            created.append(label)
            continue
        if mode == "create-missing":
            skipped.append(label)
            continue
        after_text = rendered[relative] if mode == "overwrite" else append_missing_sections(
            before.decode("utf-8"), relative, rendered[relative]
        )
        after = after_text.encode("utf-8")
        if after == before:
            skipped.append(label)
        else:
            changes.append(Change(path, before, after, file_mode, label))
            updated.append(label)

    agents = ensure_inside(root, root / "AGENTS.md")
    before_agents, agents_mode = read_regular(root, agents)
    agents_action = "unchanged"
    if before_agents is None:
        changes.append(Change(agents, None, MANAGED_SECTION.encode("utf-8"), 0o644, "AGENTS.md"))
        agents_action = "created"
    else:
        after_agents, agents_action = managed_text(before_agents.decode("utf-8"))
        after = after_agents.encode("utf-8")
        if after != before_agents:
            changes.append(Change(agents, before_agents, after, agents_mode, "AGENTS.md"))
        else:
            agents_action = "unchanged"
    return Plan(root, mode, directories, changes, created, skipped, updated, agents_action)


def inspect_state(root: Path) -> Dict[str, object]:
    plan = plan_init(root, "create-missing")
    loop_root = root / ".loop"
    existing_files = [
        ".loop/" + relative for relative in STANDARD_FILES if lexical_exists(loop_root / relative)
    ]
    missing_files = [
        ".loop/" + relative for relative in STANDARD_FILES if not lexical_exists(loop_root / relative)
    ]
    existing_dirs = [
        ".loop/" + relative + "/" for relative in STANDARD_DIRS if lexical_exists(loop_root / relative)
    ]
    missing_dirs = [
        ".loop/" + relative + "/" for relative in STANDARD_DIRS if not lexical_exists(loop_root / relative)
    ]
    additional: List[str] = []
    if lexical_exists(loop_root):
        for candidate in loop_root.rglob("*"):
            if candidate.is_file() and candidate.relative_to(loop_root).parts[0] != "backups":
                relative = candidate.relative_to(loop_root).as_posix()
                if relative not in STANDARD_FILES:
                    additional.append(".loop/" + relative)
    return {
        "loop_exists": lexical_exists(loop_root),
        "existing_files": existing_files,
        "missing_files": missing_files,
        "existing_dirs": existing_dirs,
        "missing_dirs": missing_dirs,
        "additional": sorted(additional),
        "agents_state": plan.agents_action if plan.agents_action != "unchanged" else "managed section current",
    }


def print_list(title: str, values: Sequence[str]) -> None:
    print(title)
    for value in values or ("(none)",):
        print("- " + value)


def print_inspection(root: Path, source: str) -> None:
    state = inspect_state(root)
    print("Candidate project root: " + str(root))
    print("Root detection: " + source)
    print(".loop exists: " + ("yes" if state["loop_exists"] else "no"))
    print_list("Existing standard loop files:", state["existing_files"])  # type: ignore[arg-type]
    print_list("Missing standard loop files:", state["missing_files"])  # type: ignore[arg-type]
    print_list("Existing standard loop directories:", state["existing_dirs"])  # type: ignore[arg-type]
    print_list("Missing standard loop directories:", state["missing_dirs"])  # type: ignore[arg-type]
    print_list("Additional .loop files:", state["additional"])  # type: ignore[arg-type]
    print("AGENTS.md action if initialized: " + str(state["agents_state"]))
    print("No files were changed.")


def write_atomic(path: Path, content: bytes, mode: int) -> None:
    try:
        with tempfile.NamedTemporaryFile(dir=str(path.parent), prefix=".loop-init-", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    except OSError as exc:
        try:
            if "temporary" in locals() and temporary.exists():
                temporary.unlink()
        except OSError:
            pass
        raise LoopInitError("a project file could not be written") from exc


def create_directories(root: Path, directories: Sequence[Path]) -> List[Path]:
    created: List[Path] = []
    for directory in directories:
        ensure_inside(root, directory)
        if lexical_exists(directory):
            continue
        try:
            directory.mkdir()
        except OSError as exc:
            raise LoopInitError("a project directory could not be created") from exc
        created.append(directory)
    return created


def backup_destination(root: Path, change: Change, stamp: str) -> Path:
    backup_root = ensure_inside(root, root / ".loop" / "backups" / stamp)
    relative = Path("AGENTS.md") if change.label == "AGENTS.md" else Path(change.label).relative_to(".loop")
    return ensure_inside(root, backup_root / relative)


def rollback(
    root: Path,
    applied: Sequence[Change],
    backup_paths: Sequence[Path],
    created_dirs: Sequence[Path],
) -> None:
    for change in reversed(applied):
        try:
            if change.before is None:
                if lexical_exists(change.path) and change.path.lstat() and stat.S_ISREG(change.path.lstat().st_mode):
                    change.path.unlink()
            else:
                write_atomic(change.path, change.before, change.mode)
        except (LoopInitError, OSError):
            pass
    for backup in reversed(backup_paths):
        try:
            ensure_inside(root, backup)
            if lexical_exists(backup) and stat.S_ISREG(backup.lstat().st_mode):
                backup.unlink()
        except (LoopInitError, OSError):
            pass
    for directory in reversed(created_dirs):
        try:
            ensure_inside(root, directory)
            directory.rmdir()
        except (LoopInitError, OSError):
            pass


def apply_init(root: Path, mode: str) -> Result:
    plan = plan_init(root, mode)
    stamp = timestamp()
    changed_existing = [change for change in plan.changes if change.before is not None]
    backup_dirs: List[Path] = []
    if changed_existing:
        backup_dirs.append(ensure_inside(root, root / ".loop" / "backups"))
        backup_dirs.append(ensure_inside(root, root / ".loop" / "backups" / stamp))
    created_dirs: List[Path] = []
    applied: List[Change] = []
    backup_paths: List[Path] = []
    backups: List[str] = []
    try:
        created_dirs = create_directories(root, list(plan.directories) + backup_dirs)
        for change in changed_existing:
            destination = backup_destination(root, change, stamp)
            parent = destination.parent
            if not lexical_exists(parent):
                created_dirs.extend(create_directories(root, [parent]))
            write_atomic(destination, change.before or b"", change.mode)
            backup_paths.append(destination)
            backups.append(relative_label(root, destination))
        for change in plan.changes:
            write_atomic(change.path, change.after, change.mode)
            applied.append(change)
    except LoopInitError:
        rollback(root, applied, backup_paths, created_dirs)
        raise
    return Result(plan.root, plan.mode, plan.created, plan.skipped, plan.updated, backups, plan.agents_action)


def print_summary(result: Result) -> None:
    print("Loop initialization summary")
    print("Selected project root: " + str(result.root))
    print("Initialization confirmed: yes")
    print("Mode: " + result.mode)
    print_list(".loop/ files created:", result.created)
    print_list(".loop/ files skipped because they already existed:", result.skipped)
    print_list(".loop/ files updated:", result.updated)
    print_list("Backups created:", result.backups)
    print("AGENTS.md action: " + result.agents_action)
    print("Recommended next action: record the current request, contract, and plan only if this task benefits from durable continuation.")


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect", help="inspect without writing")
    inspect.add_argument("--root", default=".", help="candidate project root")
    apply = commands.add_parser("apply", help="initialize after user confirmation")
    apply.add_argument("--root", default=".", help="candidate project root")
    apply.add_argument("--mode", choices=("create-missing", "append-sections", "overwrite"), default="create-missing")
    apply.add_argument("--yes", action="store_true", help="confirm the user approved this root and mode")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    try:
        root, source = detect_root(Path(args.root))
        if args.command == "inspect":
            print_inspection(root, source)
            return 0
        if not args.yes:
            print_inspection(root, source)
            print("[ERROR] Refusing to modify files without --yes after user confirmation.")
            return 2
        print_summary(apply_init(root, args.mode))
        return 0
    except LoopInitError as exc:
        print("loop-init: " + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
