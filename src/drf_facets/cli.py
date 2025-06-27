"""
Command-line interface for DRF Facets package.
"""

import argparse
import sys


def main(args: list[str] | None = None) -> int:
    """
    Main CLI entry point.

    Args:
        args: Command line arguments (defaults to sys.argv[1:])

    Returns:
        Exit code

    """
    parser = argparse.ArgumentParser(
        description="DRF Facets - Django package template CLI"
    )

    parser.add_argument(
        "--version",
        action="version",
        version="drf-facets 0.1.0",
    )

    parser.add_argument(
        "command",
        choices=["info", "validate"],
        help="Command to execute",
    )

    parsed_args = parser.parse_args(args)

    if parsed_args.command == "info":
        return _show_info()
    if parsed_args.command == "validate":
        return _validate_setup()

    return 0


def _show_info() -> int:
    """
    Show package information.

    Returns:
        Exit code

    """
    return 0


def _validate_setup() -> int:
    """
    Validate the package setup.

    Returns:
        Exit code (0 for success, 1 for failure)

    """
    try:
        import django
        from django.conf import settings

        # Check if Django is properly configured
        if not settings.configured:
            return 1

        # Check if the app is in INSTALLED_APPS
        if "drf_facets" not in settings.INSTALLED_APPS:
            pass

        # Check if DRF is installed
        try:
            import rest_framework

        except ImportError:
            return 1

        return 0

    except ImportError:
        return 1
    except Exception:
        return 1


if __name__ == "__main__":
    sys.exit(main())
