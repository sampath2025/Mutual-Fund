# Contributing to Mutual Fund NAV Tracker

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Git
- Basic knowledge of Python, React, and FastAPI

### Setting Up Development Environment

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/Mutual-Fund.git
   cd Mutual-Fund
   ```

2. **Backend Setup**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## 📁 Project Structure

```
Mutual-Fund/
├── backend/              # Python backend
│   ├── src/
│   │   ├── agent/        # AI agent core
│   │   ├── api/          # FastAPI endpoints
│   │   ├── backtest/     # Backtesting engine
│   │   ├── services/     # Business logic services
│   │   ├── config.py     # Configuration
│   │   └── database.py   # Database models
│   ├── scripts/          # Utility scripts
│   ├── tests/            # Backend tests
│   └── requirements.txt
├── frontend/             # React frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── App.jsx
│   │   └── main.jsx
│   └── package.json
├── docs/                 # Documentation
├── examples/             # Example code
└── README.md
```

## 🔀 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Write clean, readable code
- Follow existing code style
- Add comments for complex logic
- Update documentation if needed

### 3. Test Your Changes

**Backend:**
```bash
python -m pytest tests/
```

**Frontend:**
```bash
cd frontend
npm test
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add new feature description"
```

**Commit Message Format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### 5. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## 📝 Coding Standards

### Python

- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for functions/classes
- Maximum line length: 100 characters

### JavaScript/React

- Use ES6+ features
- Follow React best practices
- Use functional components with hooks
- Keep components small and focused

### General

- Write meaningful variable/function names
- Add comments for complex logic
- Keep functions small and focused
- Write tests for new features

## 🧪 Testing

### Backend Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_agent.py

# Run with coverage
pytest --cov=src tests/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📚 Documentation

- Update README.md if adding new features
- Add docstrings to Python functions
- Update API documentation if changing endpoints
- Add examples in `examples/` folder

## 🐛 Reporting Bugs

1. Check if bug already exists in Issues
2. Create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details
   - Screenshots if applicable

## 💡 Suggesting Features

1. Check if feature already exists in Issues
2. Create a new issue with:
   - Clear description
   - Use case
   - Proposed solution (if any)

## 🔍 Code Review Process

1. All PRs require at least one review
2. Address review comments promptly
3. Keep PRs focused and small
4. Update documentation as needed

## 📋 Checklist Before Submitting PR

- [ ] Code follows style guidelines
- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] No console errors/warnings
- [ ] Commit messages are clear
- [ ] PR description is complete

## 🤝 Community Guidelines

- Be respectful and inclusive
- Help others learn
- Share knowledge
- Give constructive feedback

## 📞 Getting Help

- Open an issue for questions
- Check existing documentation
- Review closed issues/PRs

Thank you for contributing! 🎉

