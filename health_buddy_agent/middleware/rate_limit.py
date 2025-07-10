import os
import time
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Dict, Tuple


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware that restricts requests per session.
    
    In production environment (ENVIRONMENT=Prod), allows only 5 requests per session.
    In other environments, allows unlimited requests.
    """
    
    def __init__(self, app, max_requests: int = 5, time_window: int = 3600):
        super().__init__(app)
        self.max_requests = max_requests
        self.time_window = time_window  # Time window in seconds (default: 1 hour)
        self.request_counts: Dict[str, Tuple[int, float]] = {}  # session_id -> (count, timestamp)
    
    def _get_session_id(self, request: Request) -> str:
        """
        Extract session ID from request. Uses session-id header or falls back to client IP.
        """
        # Try to get session ID from headers
        session_id = request.headers.get("session-id") or request.headers.get("x-session-id")
        
        if session_id:
            return session_id
        
        # Fallback to client IP
        client_ip = request.client.host if request.client else "unknown"
        return f"ip:{client_ip}"
    
    def _is_production_environment(self) -> bool:
        """
        Check if the current environment is production.
        """
        env = os.getenv("ENVIRONMENT", "").lower()
        return env == "prod" or env == "production"
    
    def _cleanup_expired_entries(self):
        """
        Remove expired entries from request_counts to prevent memory leaks.
        """
        current_time = time.time()
        expired_keys = [
            key for key, (_, timestamp) in self.request_counts.items()
            if current_time - timestamp > self.time_window
        ]
        for key in expired_keys:
            del self.request_counts[key]
    
    def _check_rate_limit(self, session_id: str) -> bool:
        """
        Check if the session has exceeded the rate limit.
        Returns True if request should be allowed, False if rate limited.
        """
        if not self._is_production_environment():
            # No rate limiting in non-production environments
            return True
        
        current_time = time.time()
        
        # Clean up expired entries periodically
        self._cleanup_expired_entries()
        
        if session_id not in self.request_counts:
            # First request for this session
            self.request_counts[session_id] = (1, current_time)
            return True
        
        count, timestamp = self.request_counts[session_id]
        
        # Check if the time window has expired
        if current_time - timestamp > self.time_window:
            # Reset the counter for a new time window
            self.request_counts[session_id] = (1, current_time)
            return True
        
        # Check if the request count is within the limit
        if count < self.max_requests:
            # Increment the counter
            self.request_counts[session_id] = (count + 1, timestamp)
            return True
        
        # Rate limit exceeded
        return False
    
    async def dispatch(self, request: Request, call_next):
        """
        Process the request and apply rate limiting if necessary.
        """
        session_id = self._get_session_id(request)
        
        if not self._check_rate_limit(session_id):
            # Rate limit exceeded
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Maximum {self.max_requests} requests per session allowed in production environment",
                    "session_id": session_id
                }
            )
        
        # Process the request normally
        response = await call_next(request)
        return response