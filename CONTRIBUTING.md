# Contributing to Diabetic Retinopathy Detection

First off, thank you for considering contributing to the Diabetic Retinopathy Detection project! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [issue list](https://github.com/GajendraSahani/diabetic-retinopathy-detection-/issues) as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots and animated GIFs if possible**
* **Include your environment details** (OS, Python version, etc.)

### Suggesting Enhancements

Enhancement suggestions are tracked as [GitHub issues](https://github.com/GajendraSahani/diabetic-retinopathy-detection-/issues). When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python styleguides (see below)
* End all files with a newline
* Avoid platform-dependent code

## Development Setup

### Prerequisites
- Python 3.8+
- Git
- Virtual environment manager (venv, conda, etc.)

### Setting Up Your Development Environment

1. **Fork the Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/diabetic-retinopathy-detection-.git
   cd diabetic-retinopathy-detection-
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r core-engine/requirements.txt
   pip install -r api-service/requirements.txt
   pip install -r web-ui/requirements.txt
   ```

4. **Install Development Tools**
   ```bash
   pip install black flake8 pytest pytest-cov
   ```

5. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Styleguides

### Python Styleguide

We follow PEP 8 with some modifications. Use [Black](https://github.com/psf/black) for code formatting.

```bash
# Format your code
black --line-length 100 your_file.py

# Check for style issues
flake8 your_file.py
```

**Key Guidelines:**
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to functions and classes
- Use type hints where possible

### Example Function with Type Hints
```python
from typing import Tuple, Optional
import numpy as np

def preprocess_image(
    image_path: str,
    target_size: Tuple[int, int] = (512, 512),
    apply_clahe: bool = True
) -> Optional[np.ndarray]:
    """
    Preprocess fundus image for model inference.
    
    Args:
        image_path: Path to the image file
        target_size: Target image dimensions (height, width)
        apply_clahe: Whether to apply CLAHE enhancement
    
    Returns:
        Preprocessed image array or None if preprocessing fails
    
    Raises:
        FileNotFoundError: If image file not found
        ValueError: If image cannot be read
    """
    # Implementation here
    pass
```

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* Consider starting the commit message with an applicable emoji:
  * 🎨 `:art:` when improving the format/structure of the code
  * 🐛 `:bug:` when fixing a bug
  * ✨ `:sparkles:` when introducing a new feature
  * 📚 `:books:` when writing documentation
  * 🎓 `:mortar_board:` when adding educational content
  * ⚡ `:zap:` when improving performance
  * ✅ `:white_check_mark:` when adding tests
  * 🐳 `:whale:` when working with Docker

Example:
```
✨ Add CLAHE preprocessing to image pipeline

- Implement CLAHE enhancement for improved contrast
- Add configuration parameters for clip limit
- Update data pipeline tests

Fixes #123
```

## Documentation Styleguide

* Use Markdown for documentation
* Reference functions and classes using backticks: `function_name()`
* Reference files using relative paths: `/path/to/file.py`
* Include code examples where helpful
* Keep documentation up-to-date with code changes

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=./

# Run specific test file
pytest tests/test_model.py

# Run with verbose output
pytest -v
```

### Writing Tests

Place tests in a `tests/` directory with the same structure as the main code:

```python
import pytest
from core_engine.predictor import ProductionPredictor

def test_predictor_initialization():
    """Test ProductionPredictor initialization."""
    predictor = ProductionPredictor(model_path="path/to/model.keras")
    assert predictor is not None

@pytest.fixture
def sample_image():
    """Fixture providing sample test image."""
    return np.random.rand(512, 512, 3)

def test_prediction(sample_image):
    """Test image prediction."""
    predictor = ProductionPredictor()
    result = predictor.predict(sample_image)
    assert result is not None
    assert 0 <= result["prediction"] <= 4
```

## Code Review Process

1. **Submit your pull request** with a clear description of changes
2. **Wait for review** from project maintainers
3. **Address feedback** and push updates to your branch
4. **Once approved**, your PR will be merged

## Release Process

Releases follow [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## Questions?

Feel free to open an issue with the `question` label or start a discussion.

---

Thank you for contributing! 🎉
