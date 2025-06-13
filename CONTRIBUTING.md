<div align="center">

# 🤝 Contributing to Mallouka Motors

### *Building the Future of Motor Management Together*

[![Contributors Welcome](https://img.shields.io/badge/Contributors-Welcome-brightgreen?style=for-the-badge)](https://github.com/fekikarim/Mallouka_Motors/graphs/contributors)
[![Code of Conduct](https://img.shields.io/badge/Code%20of%20Conduct-Enforced-blue?style=for-the-badge)](CODE_OF_CONDUCT.md)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

---

</div>

## 🎯 Welcome Contributors!

Thank you for your interest in contributing to **Mallouka Motors**! We're excited to collaborate with developers, designers, and enthusiasts who share our vision of revolutionizing motor dealership management through innovative technology.

> 💡 **Our Mission**: Create a world-class, open-source motor management system that empowers businesses worldwide.

---

## 📋 Table of Contents

- [🚀 Getting Started](#-getting-started)
- [🛠️ Development Setup](#️-development-setup)
- [📝 Contribution Guidelines](#-contribution-guidelines)
- [🐛 Bug Reports](#-bug-reports)
- [✨ Feature Requests](#-feature-requests)
- [💻 Code Standards](#-code-standards)
- [🔄 Pull Request Process](#-pull-request-process)
- [🧪 Testing Guidelines](#-testing-guidelines)
- [📚 Documentation](#-documentation)
- [🏆 Recognition](#-recognition)

---

## 🚀 Getting Started

### 📋 Prerequisites

Before contributing, ensure you have:

- **Python 3.8+** installed
- **Git** for version control
- **Code editor** (VS Code recommended)
- **Virtual environment** knowledge
- Basic understanding of **Flet framework**

### 🔧 First-Time Setup

```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork locally
git clone https://github.com/YOUR_USERNAME/Mallouka_Motors.git
cd Mallouka_Motors

# 3. Add upstream remote
git remote add upstream https://github.com/fekikarim/Mallouka_Motors.git

# 4. Create virtual environment
python -m venv venv

# 5. Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 6. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# 7. Verify installation
python src/main.py
```

---

## 🛠️ Development Setup

### 🏗️ Project Structure

```
📁 Mallouka Motors/
├── 📁 src/                    # Source code
│   ├── 📄 main.py            # Application entry point
│   ├── 📄 MainApp.py         # Main application class
│   ├── 📄 Dashboard.py       # Dashboard module
│   ├── 📄 Motors.py          # Motors management
│   ├── 📄 Clients.py         # Client management
│   ├── 📄 Billings.py        # Billing system
│   ├── 📄 Settings.py        # Settings & configuration
│   ├── 📄 db.py              # Database operations
│   └── 📁 assets/            # Static assets
├── 📁 storage/               # Data storage
├── 📄 requirements.txt       # Dependencies
├── 📄 pyproject.toml        # Project configuration
└── 📄 README.md             # Project documentation
```

### 🔄 Development Workflow

```bash
# 1. Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# 2. Create feature branch
git checkout -b feature/your-feature-name

# 3. Make changes and test
python src/main.py

# 4. Commit changes
git add .
git commit -m "feat: add your feature description"

# 5. Push to your fork
git push origin feature/your-feature-name

# 6. Create Pull Request on GitHub
```

---

## 📝 Contribution Guidelines

### 🎯 Types of Contributions

| Type | Description | Examples |
|------|-------------|----------|
| 🐛 **Bug Fixes** | Fix existing issues | UI bugs, data validation, crashes |
| ✨ **Features** | Add new functionality | New modules, API endpoints, UI components |
| 📚 **Documentation** | Improve docs | README updates, code comments, tutorials |
| 🎨 **UI/UX** | Design improvements | Theme enhancements, responsive design |
| ⚡ **Performance** | Optimize code | Database queries, memory usage, speed |
| 🧪 **Testing** | Add/improve tests | Unit tests, integration tests, E2E tests |

### 🌟 Contribution Areas

- **Frontend Development** (Flet UI components)
- **Backend Development** (Python business logic)
- **Database Design** (SQLite optimization)
- **PDF Generation** (ReportLab enhancements)
- **Testing & QA** (Automated testing)
- **Documentation** (Technical writing)
- **Localization** (Multi-language support)
- **Performance Optimization**

---

## 🐛 Bug Reports

### 📋 Before Reporting

1. **Search existing issues** to avoid duplicates
2. **Update to latest version** and test again
3. **Reproduce the bug** consistently
4. **Gather system information**

### 📝 Bug Report Template

```markdown
## 🐛 Bug Description
A clear description of the bug.

## 🔄 Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## ✅ Expected Behavior
What should happen.

## ❌ Actual Behavior
What actually happens.

## 🖥️ Environment
- OS: [e.g., Windows 11, macOS 12.0]
- Python Version: [e.g., 3.9.7]
- Flet Version: [e.g., 0.25.2]
- App Version: [e.g., 0.1.0]

## 📸 Screenshots
If applicable, add screenshots.

## 📋 Additional Context
Any other relevant information.
```

---

## ✨ Feature Requests

### 💡 Feature Request Template

```markdown
## 🚀 Feature Description
Clear description of the proposed feature.

## 🎯 Problem Statement
What problem does this solve?

## 💭 Proposed Solution
Detailed description of your solution.

## 🔄 Alternative Solutions
Other approaches you've considered.

## 📈 Benefits
How this improves the application.

## 🏗️ Implementation Ideas
Technical approach (optional).
```

---

## 💻 Code Standards

### 🐍 Python Style Guide

- Follow **PEP 8** conventions
- Use **type hints** where applicable
- Write **docstrings** for functions and classes
- Keep functions **small and focused**
- Use **meaningful variable names**

### 📝 Code Examples

```python
# ✅ Good Example
def calculate_total_revenue(billing_data: List[Dict]) -> float:
    """
    Calculate total revenue from billing data.
    
    Args:
        billing_data: List of billing dictionaries
        
    Returns:
        Total revenue as float
    """
    return sum(float(bill.get('total_price', 0)) for bill in billing_data)

# ❌ Bad Example
def calc(data):
    total = 0
    for d in data:
        total += float(d['total_price'])
    return total
```

### 🎨 UI/UX Guidelines

- Follow **Material Design** principles
- Ensure **accessibility** compliance
- Support both **light and dark** themes
- Maintain **responsive design**
- Use **consistent spacing** and typography

### 📱 Flet Best Practices

```python
# ✅ Good: Proper component structure
Container(
    content=Column([
        Text("Title", style=TextThemeStyle.HEADLINE_MEDIUM),
        Divider(),
        # Content here
    ]),
    padding=padding.all(16),
    border_radius=8,
)

# ❌ Bad: Inline styling and poor structure
Container(Text("Title"), padding=10, bgcolor="blue")
```

---

## 🔄 Pull Request Process

### 📋 PR Checklist

- [ ] **Branch** created from latest `main`
- [ ] **Code** follows style guidelines
- [ ] **Tests** added/updated and passing
- [ ] **Documentation** updated if needed
- [ ] **Self-review** completed
- [ ] **Descriptive title** and description
- [ ] **Screenshots** included for UI changes

### 📝 PR Template

```markdown
## 📋 Description
Brief description of changes.

## 🎯 Type of Change
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 💥 Breaking change
- [ ] 📚 Documentation update

## 🧪 Testing
- [ ] Unit tests pass
- [ ] Manual testing completed
- [ ] No regression issues

## 📸 Screenshots
Include screenshots for UI changes.

## 📝 Additional Notes
Any additional information.
```

### 🔍 Review Process

1. **Automated checks** must pass
2. **Code review** by maintainers
3. **Testing** in development environment
4. **Approval** from project maintainers
5. **Merge** into main branch

---

## 🧪 Testing Guidelines

### 🔬 Testing Strategy

```python
# Unit Test Example
import unittest
from src.db import calculate_total_revenue

class TestBillingCalculations(unittest.TestCase):
    def test_calculate_total_revenue(self):
        """Test revenue calculation with valid data."""
        billing_data = [
            {'total_price': '100.50'},
            {'total_price': '250.75'},
        ]
        result = calculate_total_revenue(billing_data)
        self.assertEqual(result, 351.25)
        
    def test_calculate_total_revenue_empty(self):
        """Test revenue calculation with empty data."""
        result = calculate_total_revenue([])
        self.assertEqual(result, 0.0)
```

### 🚀 Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_billing.py

# Run with coverage
python -m pytest --cov=src

# Run integration tests
python -m pytest tests/integration/
```

---

## 📚 Documentation

### 📝 Documentation Standards

- **Clear and concise** language
- **Code examples** for complex features
- **Screenshots** for UI documentation
- **API documentation** for functions
- **Changelog** updates for releases

### 🔧 Documentation Tools

- **Markdown** for general documentation
- **Docstrings** for code documentation
- **Screenshots** for visual guides
- **Diagrams** for architecture

---

## 🏆 Recognition

### 🌟 Contributor Levels

| Level | Contributions | Benefits |
|-------|---------------|----------|
| 🥉 **Bronze** | 1-5 PRs merged | Listed in contributors |
| 🥈 **Silver** | 6-15 PRs merged | Special mention in releases |
| 🥇 **Gold** | 16+ PRs merged | Collaborator access |
| 💎 **Diamond** | Major features | Core team invitation |

### 🎉 Hall of Fame

Contributors who make significant impacts will be featured in:
- **README.md** contributors section
- **Release notes** acknowledgments
- **Project website** (when available)
- **Social media** shoutouts

---

<div align="center">

## 🤝 Join Our Community!

[![Discord](https://img.shields.io/badge/Discord-Join_Chat-7289DA?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/mallouka-motors)
[![GitHub Discussions](https://img.shields.io/badge/GitHub-Discussions-181717?style=for-the-badge&logo=github)](https://github.com/fekikarim/Mallouka_Motors/discussions)

---

**Thank you for contributing to Mallouka Motors!** 🚗✨

*Together, we're building the future of motor management.*

---

## 🔒 Security Guidelines

### 🛡️ Reporting Security Issues

If you discover a security vulnerability, please **DO NOT** open a public issue. Instead:

1. **Email**: [security@mallouka-motors.com](mailto:security@mallouka-motors.com)
2. **Include**: Detailed description and steps to reproduce
3. **Wait**: For acknowledgment before public disclosure

### 🔐 Security Best Practices

- **Never commit** sensitive data (passwords, API keys)
- **Use environment variables** for configuration
- **Validate all inputs** to prevent injection attacks
- **Follow OWASP** security guidelines
- **Keep dependencies** up to date

---

## 🌍 Internationalization (i18n)

### 🗣️ Adding Language Support

We welcome translations to make Mallouka Motors accessible globally:

```python
# Example: Adding French translations
TRANSLATIONS = {
    'en': {
        'dashboard': 'Dashboard',
        'motors': 'Motors',
        'clients': 'Clients',
    },
    'fr': {
        'dashboard': 'Tableau de Bord',
        'motors': 'Moteurs',
        'clients': 'Clients',
    }
}
```

### 📝 Translation Guidelines

- **Maintain context** and meaning
- **Use appropriate** cultural references
- **Test UI layout** with translated text
- **Follow locale** formatting conventions

---

## 📊 Performance Guidelines

### ⚡ Optimization Principles

- **Database queries**: Use efficient SQLite queries
- **Memory usage**: Avoid memory leaks in long-running operations
- **UI responsiveness**: Keep UI thread free from heavy operations
- **Caching**: Implement appropriate caching strategies

### 📈 Performance Testing

```python
# Example: Performance test
import time
import cProfile

def profile_function(func):
    """Profile function performance."""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

@profile_function
def load_motors_data():
    # Your function implementation
    pass
```

---

## 🎨 Design System

### 🎯 UI Components

Our design system follows Material Design 3 principles:

- **Colors**: Primary, Secondary, Surface variants
- **Typography**: Consistent font scales and weights
- **Spacing**: 8px grid system
- **Elevation**: Consistent shadow and depth
- **Motion**: Smooth transitions and animations

### 🖼️ Asset Guidelines

- **Icons**: Use Material Design icons or SVG format
- **Images**: Optimize for web (WebP preferred)
- **Logos**: Maintain aspect ratio and brand guidelines
- **Screenshots**: High resolution, consistent styling

---

## 🚀 Release Process

### 📋 Version Numbering

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### 🔄 Release Workflow

1. **Feature freeze** for release candidate
2. **Testing phase** with community feedback
3. **Documentation** updates and review
4. **Release notes** preparation
5. **Tag and publish** release
6. **Announcement** to community

---

## 📞 Getting Help

### 🤔 Where to Ask Questions

- **💬 GitHub Discussions**: General questions and ideas
- **🐛 GitHub Issues**: Bug reports and feature requests
- **📧 Email**: [contribute@mallouka-motors.com](mailto:contribute@mallouka-motors.com)
- **💼 LinkedIn**: [Karim Feki](https://www.linkedin.com/in/karimfeki/)

### 📚 Learning Resources

- **[Flet Documentation](https://flet.dev/docs/)**: Official Flet framework docs
- **[Python Guide](https://docs.python-guide.org/)**: Python best practices
- **[SQLite Tutorial](https://www.sqlitetutorial.net/)**: Database optimization
- **[Material Design](https://m3.material.io/)**: UI/UX guidelines

---

## 📜 Code of Conduct

### 🤝 Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of:

- **Background**: Race, ethnicity, nationality
- **Identity**: Gender, sexual orientation, religion
- **Experience**: Skill level, age, education
- **Perspective**: Political views, personal opinions

### ✅ Expected Behavior

- **Be respectful** and considerate
- **Use inclusive** language
- **Accept constructive** criticism gracefully
- **Focus on collaboration** and learning
- **Help others** grow and succeed

### ❌ Unacceptable Behavior

- **Harassment** or discrimination
- **Trolling** or inflammatory comments
- **Personal attacks** or insults
- **Publishing private** information
- **Inappropriate** sexual content

### 🚨 Enforcement

Violations may result in:
1. **Warning** and guidance
2. **Temporary** suspension
3. **Permanent** ban from project

Report issues to: [conduct@mallouka-motors.com](mailto:conduct@mallouka-motors.com)

---

<div align="center">

## 🎉 Ready to Contribute?

[![Start Contributing](https://img.shields.io/badge/Start-Contributing-success?style=for-the-badge&logo=github)](https://github.com/fekikarim/Mallouka_Motors/fork)
[![View Issues](https://img.shields.io/badge/View-Issues-blue?style=for-the-badge&logo=github)](https://github.com/fekikarim/Mallouka_Motors/issues)
[![Join Discussion](https://img.shields.io/badge/Join-Discussion-purple?style=for-the-badge&logo=github)](https://github.com/fekikarim/Mallouka_Motors/discussions)

**Every contribution matters, no matter how small!** 🌟

*Let's build something amazing together.*

</div>
