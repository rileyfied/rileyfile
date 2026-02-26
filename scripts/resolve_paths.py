#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import traceback

from context_hub_common import resolve_paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve and verify Context Hub paths")
    parser.add_argument("--json", action="store_true", help="Print resolved paths as JSON")
    args = parser.parse_args()

    try:
        resolved = resolve_paths(require_existing_root=True)
    except Exception as exc:
        print(f"ERROR: {exc}")
        print(traceback.format_exc())
        return 1

    payload = resolved.as_dict()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        for k, v in payload.items():
            print(f"{k}={v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
