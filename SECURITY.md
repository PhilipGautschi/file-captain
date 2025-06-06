# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.0   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please send an email to [mail@philipgautschi.ch](mailto:mail@philipgautschi.ch).

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge receipt within 48 hours and provide a detailed response within 5 business days.

## Security Considerations

### Pickle Files
**WARNING**: This library can load pickle files, which can execute arbitrary code. Only load pickle files from trusted sources. See our [README](README.md#security-considerations) for more details.
