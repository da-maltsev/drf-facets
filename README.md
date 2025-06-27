# DRF Facets

A Django package template for building Django REST Framework extensions and utilities.

## Features

- Django 4.0+ compatible
- Django REST Framework integration
- Modern Python packaging with uv
- Comprehensive testing setup
- Code quality tools (black, flake8, mypy)
- Pre-commit hooks

## Installation

### Using uv (recommended)

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install the package
uv add drf-facets
```

### Using pip

```bash
pip install drf-facets
```

## Quick Start

1. Add the app to your Django settings:

```python
INSTALLED_APPS = [
    # ... other apps
    'drf_facets',
]
```

2. Include the URLs in your main URLconf:

```python
from django.urls import include, path

urlpatterns = [
    # ... other URL patterns
    path('facets/', include('drf_facets.urls')),
]
```

## Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/drf-facets.git
cd drf-facets
```

2. Install development dependencies:
```bash
uv sync --group dev
```

3. Install pre-commit hooks:
```bash
pre-commit install
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=drf_facets

# Run specific test file
uv run pytest tests/test_example.py
```

### Code Quality

```bash
# Format code
uv run black .

# Sort imports
uv run isort .

# Lint code
uv run flake8 .

# Type checking
uv run mypy .
```

### Building

```bash
# Build the package
uv build

# Build and publish (requires authentication)
uv publish
```

## Project Structure

```
drf-facets/
├── src/
│   └── drf_facets/
│       ├── __init__.py
│       ├── apps.py
│       ├── models.py
│       ├── views.py
│       ├── urls.py
│       ├── serializers.py
│       └── cli.py
├── tests/
│   ├── __init__.py
│   ├── settings.py
│   ├── test_models.py
│   ├── test_views.py
│   └── test_serializers.py
├── pyproject.toml
├── README.md
├── LICENSE
├── MANIFEST.in
└── .gitignore
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `uv run pytest`
5. Commit your changes: `git commit -m 'Add amazing feature'`
6. Push to the branch: `git push origin feature/amazing-feature`
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### 0.1.0 (2024-01-01)

- Initial release
- Basic Django package template structure
- Testing and development setup 