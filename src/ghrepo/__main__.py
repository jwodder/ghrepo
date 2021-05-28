import argparse
import json
import subprocess
import sys
from . import __version__, get_local_repo


def main() -> None:
    parser = argparse.ArgumentParser(description="Show current GitHub repository")
    parser.add_argument("-J", "--json", action="store_true", help="Output JSON")
    parser.add_argument(
        "-r",
        "--remote",
        default="origin",
        help="Parse the GitHub URL from the given remote [default: origin]",
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
    except ValueError as e:
        sys.exit(str(e))
    if args.json:
        print(
            json.dumps(
                {
                    "owner": r.owner,
                    "name": r.name,
                    "fullname": str(r),
                    "api_url": r.api_url,
                    "clone_url": r.clone_url,
                    "git_url": r.git_url,
                    "html_url": r.html_url,
                    "ssh_url": r.ssh_url,
                },
                indent=4,
            )
        )
    else:
        print(r)


if __name__ == "__main__":
    main()  # pragma: no cover
