#!/bin/bash
set -e
# Find uvicorn wherever pip installed it
UVICORN=$(find / -name "uvicorn" -type f 2>/dev/null | head -1)
if [ -z "$UVICORN" ]; then
    pip install uvicorn fastapi
    UVICORN=$(find / -name "uvicorn" -type f 2>/dev/null | head -1)
fi
exec $UVICORN services.api.main:app --host 0.0.0.0 --port ${PORT:-8000}
