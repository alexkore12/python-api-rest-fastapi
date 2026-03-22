# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.1.x   | ✅                 |
| 2.0.x   | ✅                 |
| 1.x     | ❌                 |

## Reporting a Vulnerability

If you discover a security vulnerability within this FastAPI application, please send an e-mail to the maintainer. All security vulnerabilities will be promptly addressed.

Please include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

## Security Features Implemented

### Authentication & Authorization
- ✅ JWT tokens with configurable expiry
- ✅ OAuth2 Password Flow
- ✅ Role-based access control
- ✅ Password hashing (bcrypt)

### API Security
- ✅ Rate limiting (100 req/min public, 60 req/min authenticated)
- ✅ CORS configuration
- ✅ Helmet headers
- ✅ Input validation with Pydantic
- ✅ Request size limiting

### Data Protection
- ✅ SQL injection prevention (parameterized queries)
- ✅ XSS protection (output encoding)
- ✅ CSRF protection
- ✅ Secure password storage

### Logging & Monitoring
- ✅ Request logging
- ✅ Error tracking
- ✅ Security event logging

## Security Best Practices

### For Production Deployment

1. **Use HTTPS**
   - Configure reverse proxy (nginx, traefik)
   - Enable TLS 1.2+
   - Use valid certificates

2. **Environment Variables**
   ```bash
   SECRET_KEY=<strong-random-key>
   DATABASE_URL=postgresql://...
   CORS_ORIGINS=https://yourdomain.com
   ```

3. **Rate Limiting**
   - Adjust limits based on traffic
   - Consider API gateway for scaling

4. **Logging**
   - Send logs to centralized system
   - Monitor for anomalies
   - Set up alerts

5. **Database**
   - Use connection pooling
   - Enable SSL for database connections
   - Regular backups

### Dependency Management

```bash
# Check for vulnerabilities
pip install safety
safety check

# Update dependencies
pip list --outdated
pip install -U <package>
```

## Vulnerability Disclosure

We appreciate responsible disclosure. Please contact us before publishing any vulnerabilities publicly.

---

*Last updated: 2026-03-22*
