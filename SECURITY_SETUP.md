# Security Setup Guide

## Overview
Your API now includes comprehensive security features to protect against abuse and unauthorized access.

## Security Features Implemented

### ✅ 1. Rate Limiting
- **Per minute limit**: 10 requests/minute for most endpoints
- **Per hour limit**: 100 requests/hour for batch operations
- **Purpose**: Prevents DoS attacks and API abuse
- **Configuration**: Adjust `RATE_LIMIT_PER_MINUTE` and `RATE_LIMIT_PER_HOUR` in `.env`

### ✅ 2. API Key Authentication
- **Header**: `X-API-Key`
- **Purpose**: Controls who can access your API
- **Configuration**: 
  - Set `REQUIRE_API_KEY=true` in production
  - Add valid keys to `API_KEYS` (comma-separated)
  - Generate secure keys: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

### ✅ 3. File Upload Validation
- **Max file size**: 5MB (configurable)
- **Allowed types**: PDF, DOCX, DOC, TXT
- **MIME type verification**: Ensures file content matches extension
- **Filename sanitization**: Prevents path traversal attacks

### ✅ 4. Input Validation
- **Text length limits**: 50,000 characters max
- **Batch size limits**: 10 files max per batch
- **Empty input checks**: Rejects empty or whitespace-only inputs
- **Pydantic validation**: Type checking and field validation

### ✅ 5. CORS Configuration
- **Specific origins only**: No more `allow_origins=["*"]`
- **Configure**: Set `ALLOWED_ORIGINS` in `.env` with your frontend URLs

### ✅ 6. Error Handling
- **No information leakage**: Generic error messages for users
- **Detailed logging**: Internal logs for debugging
- **HTTP status codes**: Proper status codes for different errors

### ✅ 7. Request Size Limits
- **Max request size**: 10MB
- **Prevents memory exhaustion**

## Configuration

### Development Setup (Default)
```bash
# .env file for development
REQUIRE_API_KEY=false  # Disabled for easy testing
RATE_LIMIT_ENABLED=true
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Production Setup
```bash
# .env file for production
REQUIRE_API_KEY=true
API_KEYS=your-secure-key-1,your-secure-key-2
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_PER_HOUR=100
ALLOWED_ORIGINS=https://your-production-domain.com
MAX_FILE_SIZE_MB=5
MAX_BATCH_SIZE=10
```

## Generating API Keys

```bash
# Generate a secure API key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate multiple keys
python -c "import secrets; [print(secrets.token_urlsafe(32)) for _ in range(3)]"
```

## Using API Keys (Frontend)

### JavaScript/React Example
```javascript
const response = await fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': 'your-api-key-here'
  },
  body: JSON.stringify({
    resume_text: resumeText,
    job_description: jobDescription
  })
});
```

### cURL Example
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key-here" \
  -d '{"resume_text": "...", "job_description": "..."}'
```

## Installation

### Install new dependencies
```bash
cd backend
pip install -r requirements.txt
```

## Testing

### Test without API key (development)
```bash
# Make sure REQUIRE_API_KEY=false in .env
curl http://localhost:8000/health
```

### Test with API key
```bash
curl -H "X-API-Key: dev-api-key-for-testing-only" http://localhost:8000/health
```

### Test rate limiting
```bash
# Run this multiple times quickly to trigger rate limit
for i in {1..15}; do curl http://localhost:8000/health; done
```

### Test file upload validation
```bash
# Upload a file that's too large (will be rejected)
curl -X POST http://localhost:8000/api/analyze-file \
  -H "X-API-Key: your-key" \
  -F "resume_file=@large_file.pdf" \
  -F "job_description=Software Engineer position"
```

## Error Responses

### 401 Unauthorized (Missing API Key)
```json
{
  "detail": "API key required. Please provide X-API-Key header."
}
```

### 403 Forbidden (Invalid API Key)
```json
{
  "detail": "Invalid API key"
}
```

### 413 Request Entity Too Large
```json
{
  "detail": "File too large. Maximum size is 5MB"
}
```

### 429 Too Many Requests (Rate Limit)
```json
{
  "detail": "Rate limit exceeded: 10 per 1 minute"
}
```

### 400 Bad Request (Invalid Input)
```json
{
  "detail": "File type not allowed. Allowed types: .pdf, .docx, .doc, .txt"
}
```

## Security Best Practices

### For Production Deployment:

1. **Enable Authentication**
   - Set `REQUIRE_API_KEY=true`
   - Use strong, randomly-generated API keys
   - Rotate keys periodically

2. **Configure CORS Properly**
   - Only allow your actual frontend domain
   - Never use `allow_origins=["*"]` in production

3. **Adjust Rate Limits**
   - Start conservative, increase if needed
   - Monitor for abuse patterns

4. **File Upload Security**
   - Keep file size limits reasonable
   - Consider adding virus scanning
   - Validate file contents, not just extensions

5. **Logging & Monitoring**
   - Monitor failed authentication attempts
   - Track rate limit violations
   - Set up alerts for suspicious activity

6. **HTTPS Only**
   - Use HTTPS in production
   - Add security headers (HSTS, etc.)

7. **Environment Variables**
   - Never commit `.env` to git
   - Use secrets management in production
   - Rotate API keys if compromised

## Monitoring

### Check Security Config
```bash
# View current security settings (no auth required for this endpoint)
curl http://localhost:8000/
```

Response includes:
```json
{
  "security": {
    "rate_limit_enabled": true,
    "rate_limit_per_minute": 10,
    "max_file_size_mb": 5,
    "max_text_length": 50000,
    "max_batch_size": 10,
    "api_key_required": true
  }
}
```

## Troubleshooting

### API returns 401 or 403 errors
- Check if `REQUIRE_API_KEY=true` in `.env`
- Verify you're sending the `X-API-Key` header
- Confirm your API key is in the `API_KEYS` list

### Rate limit errors in development
- Set higher limits in `.env`
- Or disable: `RATE_LIMIT_ENABLED=false`

### CORS errors
- Add your frontend URL to `ALLOWED_ORIGINS`
- Include the protocol (`http://` or `https://`)
- Check browser console for specific CORS error

### File upload fails
- Check file size (must be < `MAX_FILE_SIZE_MB`)
- Verify file type is allowed
- Ensure file is not corrupted

## Next Steps

1. **Update Frontend**: Add API key to requests
2. **Test All Endpoints**: Verify security works correctly
3. **Generate Production Keys**: Create strong API keys for production
4. **Deploy**: Update production environment variables
5. **Monitor**: Watch logs for security issues
