import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from health_buddy_agent.main import app

client = TestClient(app)


class TestRateLimitMiddleware:
    """
    Test cases for the rate limiting middleware.
    """

    @patch.dict(os.environ, {"ENVIRONMENT": "dev"})
    def test_no_rate_limiting_in_non_prod_environment(self):
        """Test that rate limiting is not applied in non-production environments."""
        # Make multiple requests (more than the limit)
        for i in range(10):
            response = client.get("/", headers={"session-id": "test-session"})
            assert response.status_code == 200

    @patch.dict(os.environ, {"ENVIRONMENT": "Prod"})
    def test_rate_limiting_in_prod_environment(self):
        """Test that rate limiting is applied in production environment."""
        session_id = "test-session-prod"
        
        # Make 5 requests (should all succeed)
        for i in range(5):
            response = client.get("/", headers={"session-id": session_id})
            assert response.status_code == 200
        
        # 6th request should be rate limited
        response = client.get("/", headers={"session-id": session_id})
        assert response.status_code == 429
        assert "Rate limit exceeded" in response.json()["error"]

    @patch.dict(os.environ, {"ENVIRONMENT": "Prod"})
    def test_different_sessions_have_separate_limits(self):
        """Test that different sessions have separate rate limits."""
        # First session - make 5 requests
        session1 = "session-1"
        for i in range(5):
            response = client.get("/", headers={"session-id": session1})
            assert response.status_code == 200
        
        # 6th request for session 1 should be rate limited
        response = client.get("/", headers={"session-id": session1})
        assert response.status_code == 429
        
        # But session 2 should still work
        session2 = "session-2"
        response = client.get("/", headers={"session-id": session2})
        assert response.status_code == 200

    @patch.dict(os.environ, {"ENVIRONMENT": "Prod"})
    def test_fallback_to_ip_when_no_session_header(self):
        """Test that IP address is used as fallback when no session ID header is provided."""
        # Make 5 requests without session header
        for i in range(5):
            response = client.get("/")
            assert response.status_code == 200
        
        # 6th request should be rate limited
        response = client.get("/")
        assert response.status_code == 429

    @patch.dict(os.environ, {"ENVIRONMENT": "production"})
    def test_production_case_insensitive(self):
        """Test that environment check is case insensitive."""
        session_id = "test-session-case"
        
        # Make 5 requests (should all succeed)
        for i in range(5):
            response = client.get("/", headers={"session-id": session_id})
            assert response.status_code == 200
        
        # 6th request should be rate limited
        response = client.get("/", headers={"session-id": session_id})
        assert response.status_code == 429

    @patch.dict(os.environ, {"ENVIRONMENT": "Prod"})
    def test_x_session_id_header_works(self):
        """Test that x-session-id header also works for session identification."""
        session_id = "test-x-session"
        
        # Make 5 requests with x-session-id header
        for i in range(5):
            response = client.get("/", headers={"x-session-id": session_id})
            assert response.status_code == 200
        
        # 6th request should be rate limited
        response = client.get("/", headers={"x-session-id": session_id})
        assert response.status_code == 429

    @patch.dict(os.environ, {"ENVIRONMENT": "Prod"})
    def test_rate_limit_response_format(self):
        """Test that the rate limit response has the correct format."""
        session_id = "test-response-format"
        
        # Make 5 requests to reach the limit
        for i in range(5):
            response = client.get("/", headers={"session-id": session_id})
            assert response.status_code == 200
        
        # 6th request should return proper rate limit response
        response = client.get("/", headers={"session-id": session_id})
        assert response.status_code == 429
        
        json_response = response.json()
        assert "error" in json_response
        assert "message" in json_response
        assert "session_id" in json_response
        assert json_response["error"] == "Rate limit exceeded"
        assert "5 requests per session" in json_response["message"]
        assert json_response["session_id"] == session_id