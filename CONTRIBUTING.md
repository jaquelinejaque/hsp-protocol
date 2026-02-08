# Contributing to HSP Protocol

Thank you for your interest in contributing to the Human Supervision Protocol!

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Issues

- Check existing issues before creating a new one
- Use the issue templates when available
- Provide clear reproduction steps for bugs
- Include relevant environment details

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`npm test` or `pytest`)
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

### Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring

### Code Style

- Solidity: Follow Solidity style guide
- TypeScript: Use ESLint + Prettier
- Python: Follow PEP 8, use Black formatter

## Development Setup

### Smart Contracts

```bash
cd contracts
npm install
npm run compile
npm run test
```

### JavaScript SDK

```bash
cd sdk/javascript
npm install
npm run build
npm run test
```

### Python SDK

```bash
cd sdk/python
pip install -e ".[dev]"
pytest
```

## Patent Notice

By contributing to this project, you acknowledge that the HSP Protocol is covered by patent application PCT/US26/11908. Contributions are licensed under Apache 2.0.

## Questions?

Open a discussion or reach out to the maintainers.

Thank you for contributing!
