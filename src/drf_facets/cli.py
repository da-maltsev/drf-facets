"""
Command-line interface for DRF Facets package.
"""

import argparse
import sys
from typing import Optional


def main(args: Optional[list[str]] = None) -> int:
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
    elif parsed_args.command == "validate":
        return _validate_setup()
    
    return 0


def _show_info() -> int:
    """
    Show package information.
    
    Returns:
        Exit code
    """
    print("DRF Facets Package Information")
    print("=" * 40)
    print(f"Version: 0.1.0")
    print(f"Author: Your Name")
    print(f"Email: your.email@example.com")
    print(f"Description: A Django package template for DRF extensions")
    print()
    print("Available endpoints:")
    print("- /facets/api/examples/ - ExampleModel CRUD operations")
    print("- /facets/api/examples/active/ - Get active examples")
    print("- /facets/api/examples/stats/ - Get statistics")
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
            print("ERROR: Django settings not configured")
            return 1
        
        # Check if the app is in INSTALLED_APPS
        if "drf_facets" not in settings.INSTALLED_APPS:
            print("WARNING: 'drf_facets' not found in INSTALLED_APPS")
            print("Add 'drf_facets' to your INSTALLED_APPS setting")
        
        # Check if DRF is installed
        try:
            import rest_framework
            print("✓ Django REST Framework is installed")
        except ImportError:
            print("ERROR: Django REST Framework is not installed")
            return 1
        
        print("✓ Package setup validation passed")
        return 0
        
    except ImportError as e:
        print(f"ERROR: Failed to import Django: {e}")
        return 1
    except Exception as e:
        print(f"ERROR: Validation failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 