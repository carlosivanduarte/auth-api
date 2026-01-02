# Changelog

All notable changes to this project will be documented in this file.

### Added
- **GET /token endpoint** for JWT token validation
  - Validates Bearer tokens via Authorization header
  - Returns 200 OK for valid tokens, 401 Unauthorized for invalid/expired tokens
  - Follows security best practices with minimal response payloads

### Fixed
- Fixed JWT token encoding issue in `/token` endpoint
  - Removed `.decode('utf-8')` call from JWT token response as newer PyJWT versions return strings directly
  - Changed `return jsonify(token=token.decode('utf-8'))` to `return jsonify(token=token)`

### Environment
- **Missing dependency resolved**: `requests` package was missing from .venv virtual environment
- Installed `requests` package into .venv using pip to resolve import error
- Installed required Python packages locally:
  - `flask` - Web framework
  - `pyjwt` - JWT token handling
  - `requests` - HTTP client library (was missing, now added to .venv)
  - Dependencies: `markupsafe`, `click`, `jinja2`, `itsdangerous`, `werkzeug`, `blinker`, `certifi`, `idna`, `urllib3`, `charset-normalizer`

### Testing
- Verified `/health` endpoint returns `{"healthy":true}`
- Verified `/token` POST endpoint authentication flow:
  - Valid credentials return JWT token with 30-second expiration
  - Invalid password returns 401 error
  - Non-existent user returns 404 error
- Verified `/token` GET endpoint validation flow:
  - Valid tokens return 200 OK with empty body
  - Invalid/expired/missing tokens return 401 Unauthorized with empty body
- App successfully runs on port 5001 (port 5000 was occupied by AirPlay Receiver)
