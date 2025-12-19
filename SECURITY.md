# Security Guidelines

This document outlines security best practices and considerations for the MT5 Portfolio Analyzer.

## Input Validation

### Implemented Validations

The application implements comprehensive input validation to prevent invalid or malicious data:

1. **Strategy Metrics Validation**
   - `name`: Must be a non-empty string
   - `equity`: Must be non-negative (≥ 0)
   - `drawdown`: Must be negative or zero (≤ 0)
   - `correlation`: Must be between -1 and 1 (inclusive)
   - `recovery`: Must be non-negative (≥ 0)
   - `profit`: Any numeric value (can be negative)

2. **Portfolio Validation**
   - Minimum: 1 strategy required
   - Maximum: 10 strategies allowed per request
   - Prevents resource exhaustion from oversized requests

### Data Sanitization

All numeric inputs are explicitly cast to `float` with error handling:
```python
equity=float(strategy_data.get('equity', 0))
```

This prevents:
- Type confusion attacks
- Non-numeric data injection
- NaN or Infinity values causing issues

## API Security

### Authentication

**Current Status:** No authentication implemented (development mode)

**Production Recommendations:**
1. Implement API key authentication
2. Use JWT tokens for session management
3. Consider OAuth2 for third-party integrations

Example implementation (not included):
```python
from functools import wraps
from flask import request, jsonify

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or not verify_api_key(api_key):
            return jsonify({"error": "Invalid API key"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/portfolio/analyze', methods=['POST'])
@require_api_key
def analyze_portfolio():
    # ... existing code
```

### Rate Limiting

**Current Status:** No rate limiting implemented

**Why It's Important:**
- Prevents API abuse
- Protects against DoS attacks
- Controls OpenAI API costs
- Ensures fair resource allocation

**Recommended Implementation:**

#### Option 1: Flask-Limiter
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

@app.route('/api/portfolio/analyze', methods=['POST'])
@limiter.limit("5 per minute")  # More restrictive for expensive operations
def analyze_portfolio():
    # ... existing code
```

Add to `requirements.txt`:
```
flask-limiter==3.5.0
```

#### Option 2: Custom Rate Limiting
```python
from collections import defaultdict
from datetime import datetime, timedelta
import threading

# Simple in-memory rate limiter (use Redis in production)
class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)
        self.lock = threading.Lock()
    
    def is_allowed(self, client_id, max_requests=5, time_window=60):
        """Check if client can make request (max_requests per time_window seconds)"""
        with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(seconds=time_window)
            
            # Remove old requests
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if req_time > cutoff
            ]
            
            # Check limit
            if len(self.requests[client_id]) >= max_requests:
                return False
            
            # Add new request
            self.requests[client_id].append(now)
            return True

rate_limiter = RateLimiter()

@app.route('/api/portfolio/analyze', methods=['POST'])
def analyze_portfolio():
    client_id = request.remote_addr
    if not rate_limiter.is_allowed(client_id, max_requests=5, time_window=60):
        return jsonify({
            "success": False,
            "error": "Rate limit exceeded. Please try again later."
        }), 429
    # ... existing code
```

### CORS Configuration

**Current Configuration:**
```python
CORS(app)  # Allows all origins
```

**Production Configuration:**
```python
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://yourdomain.com",
            "https://www.yourdomain.com"
        ],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type", "X-API-Key"]
    }
})
```

## API Key Management

### Environment Variables

**✅ GOOD:** API keys stored in `.env` file (never committed)
```bash
OPENAI_API_KEY=your_key_here
```

**❌ BAD:** API keys in source code
```python
api_key = "sk-proj-abc123..."  # NEVER DO THIS
```

### Best Practices

1. **Use Environment Variables**
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   api_key = os.getenv('OPENAI_API_KEY')
   ```

2. **Validate on Startup**
   ```python
   if not api_key:
       raise ValueError("OPENAI_API_KEY not set in environment")
   ```

3. **Never Log API Keys**
   ```python
   logger.info("API initialized")  # ✅ Good
   logger.info(f"Using key: {api_key}")  # ❌ Bad
   ```

4. **Rotate Keys Regularly**
   - Change API keys every 90 days
   - Immediately rotate if exposed
   - Use separate keys for dev/staging/production

## HTTPS/TLS

**Development:** HTTP is acceptable
**Production:** HTTPS is **REQUIRED**

### Setting up HTTPS

#### Option 1: Using Nginx as Reverse Proxy
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Option 2: Let's Encrypt with Certbot
```bash
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## Logging and Monitoring

### Current Implementation

The application logs:
- API requests and responses
- Validation errors
- Processing times
- OpenAI API errors

### Security Considerations

1. **Don't Log Sensitive Data**
   - ❌ User API keys
   - ❌ Full request bodies with potentially sensitive strategy data
   - ✅ Request IDs, timestamps, error types
   - ✅ Processing times, status codes

2. **Log Rotation**
   ```python
   from logging.handlers import RotatingFileHandler
   
   handler = RotatingFileHandler(
       'app.log',
       maxBytes=10485760,  # 10MB
       backupCount=10
   )
   logger.addHandler(handler)
   ```

3. **Monitor for Suspicious Activity**
   - Repeated validation failures
   - High request rates from single IP
   - Unusual error patterns

## Deployment Checklist

### Pre-Deployment

- [ ] Remove debug mode (`DEBUG=False`)
- [ ] Set strong API keys
- [ ] Configure CORS for specific domains
- [ ] Implement rate limiting
- [ ] Add authentication
- [ ] Set up HTTPS/TLS
- [ ] Configure proper logging
- [ ] Review error messages (don't expose internal details)
- [ ] Test input validation
- [ ] Set up monitoring and alerts

### Environment Variables for Production

```bash
# Application
FLASK_ENV=production
DEBUG=False
PORT=5000

# API Keys
OPENAI_API_KEY=your_production_key_here

# Security
SECRET_KEY=your_random_secret_key_here
API_KEY_HASH=hashed_api_key_for_client_auth

# Rate Limiting
RATE_LIMIT_PER_MINUTE=5
RATE_LIMIT_PER_HOUR=50
RATE_LIMIT_PER_DAY=200

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Vulnerability Reporting

If you discover a security vulnerability, please:

1. **DO NOT** open a public issue
2. Email the maintainer directly at [security contact]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Security Updates

- Review dependencies monthly: `pip list --outdated`
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Monitor security advisories for Flask, OpenAI SDK, and other dependencies
- Subscribe to GitHub security alerts for the repository

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [OpenAI API Best Practices](https://platform.openai.com/docs/guides/safety-best-practices)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security.html)

---

**Last Updated:** December 2024
