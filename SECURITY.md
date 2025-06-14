# Security Policy

## Supported Versions

| Version | Supported          |
|---------| ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please send an email to [philips.python.projects@gmail.com](mailto:philips.python.projects@gmail.com).

**Please DO NOT open a public issue for security vulnerabilities.**

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)
- Your contact information for follow-up

We will acknowledge receipt within 48 hours and provide a detailed response within 5 business days.

## Security Considerations

### Pickle Files
**WARNING**: This library can load pickle files, which can execute arbitrary code. Only load pickle files from trusted sources. See our [README](README.md#security-considerations) for more details.

## Security Updates

Security updates will be released as patch versions and documented in our [CHANGELOG](CHANGELOG.md). Users are encouraged to update to the latest version promptly.
