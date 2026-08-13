import json, sys
from pathlib import Path
from .validator import validate

def main():
    path = Path(sys.argv[1])
    result = validate(json.loads(path.read_text()))
    if result.ok:
        print("READY: contract satisfies Manufact Cloud platform requirements")
        return 0
    print("BLOCKED")
    for item in result.violations:
        print(f"- {item}")
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
