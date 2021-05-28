import argparse
import json
import subprocess
import sys
from . import __version__, get_local_repo


def main() -> None:
    parser = argparse.ArgumentParser(description="Show current GitHub repository")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument(
        "-r", "--remote", default="origin", help="Set Git remote [default: origin]"
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("dirpath", nargs="?")
    args = parser.parse_args()
    try:
        r = get_local_repo(args.dirpath, remote=args.remote)
    except subprocess.CalledProcessError:
        sys.exit(1)
    if args.json:
        print(json.dumps({"owner": r.owner, "name": r.name, "fullname": str(r)}))
    else:
        print(r)


if __name__ == "__main__":
    main()  # pragma: no cover
