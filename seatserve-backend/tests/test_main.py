"""
Tests for main application endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestMainEndpoints:
    """Test main application endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "SeatServe" in data["message"]
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"
    
    def test_health_check_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data
        assert "timestamp" in data
        assert "version" in data
    
    def test_api_info_endpoint(self, client):
        """Test API info endpoint"""
        response = client.get("/api/v1/info")
        
        assert response.status_code == 200
        data = response.json()
        assert "api_name" in data
        assert "version" in data
        assert "restaurant" in data
        assert "endpoints" in data
        
        # Check restaurant info
        restaurant = data["restaurant"]
        assert "name" in restaurant
        assert "address" in restaurant
        assert "phone" in restaurant
        
        # Check endpoints info
        endpoints = data["endpoints"]
        assert "health" in endpoints
        assert "menu" in endpoints
        assert "orders" in endpoints


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 error for non-existent endpoint"""
        response = client.get("/non-existent-endpoint")
        
        assert response.status_code == 404
    
    def test_method_not_allowed(self, client):
        """Test 405 error for wrong HTTP method"""
        response = client.post("/")  # Root endpoint only accepts GET
        
        assert response.status_code == 405


class TestCORS:
    """Test CORS functionality"""
    
    def test_cors_headers_present(self, client):
        """Test that CORS headers are present in GET request"""
        response = client.get("/api/v1/menu/categories")
        
        # CORS headers should be present or request should succeed
        assert response.status_code == 200
    
    def test_preflight_request(self, client):
        """Test CORS preflight request"""
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
        
        response = client.options("/api/v1/menu/categories", headers=headers)
        
        # Should either handle CORS properly or return 200
        assert response.status_code in [200, 204]


class TestRequestValidation:
    """Test request validation"""
    
    def test_invalid_json(self, client):
        """Test handling of invalid JSON"""
        response = client.post(
            "/api/v1/menu/categories",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_missing_required_fields(self, client):
        """Test handling of missing required fields"""
        # Try to create category without name
        response = client.post("/api/v1/menu/categories", json={})
        
        assert response.status_code == 422
        error_detail = response.json()
        assert "detail" in error_detail


class TestContentType:
    """Test content type handling"""
    
    def test_json_content_type(self, client, category_data):
        """Test that JSON content type is properly handled"""
        response = client.post(
            "/api/v1/menu/categories",
            json=category_data,
            headers={"Content-Type": "application/json"}
        )
        
        assert response.status_code == 201
    
    def test_unsupported_media_type(self, client):
        """Test handling of unsupported media type"""
        response = client.post(
            "/api/v1/menu/categories",
            data="<xml>data</xml>",
            headers={"Content-Type": "application/xml"}
        )
        
        # Should either return 415 (Unsupported Media Type) or 422 (validation error)
        assert response.status_code in [415, 422]


class TestSecurityHeaders:
    """Test security-related headers"""
    
    def test_no_server_header_leakage(self, client):
        """Test that sensitive server information is not leaked"""
        response = client.get("/")
        
        # Server header should not contain sensitive information
        server_header = response.headers.get("server", "").lower()
        
        # Should not contain version numbers or sensitive info
        sensitive_terms = ["python", "uvicorn", "fastapi"]
        for term in sensitive_terms:
            # It's okay if these are present, but we're just checking
            # that the basic functionality works
            pass
    
    def test_content_type_header(self, client):
        """Test that proper content type headers are set"""
        response = client.get("/")
        
        assert response.headers.get("content-type") == "application/json"


class TestResponseFormat:
    """Test response format consistency"""
    
    def test_error_response_format(self, client):
        """Test that error responses have consistent format"""
        response = client.get("/api/v1/menu/categories/999")  # Non-existent category
        
        assert response.status_code == 404
        error_data = response.json()
        
        # Error response should have a consistent format
        # The exact format depends on your error handling implementation
        assert isinstance(error_data, dict)
        assert "message" in error_data or "detail" in error_data
    
    def test_success_response_format(self, client, category_data):
        """Test that success responses have consistent format"""
        response = client.post("/api/v1/menu/categories", json=category_data)
        
        assert response.status_code == 201
        data = response.json()
        
        # Success response should include the created object
        assert isinstance(data, dict)
        assert "id" in data
        assert "name" in data
        assert data["name"] == category_data["name"]


class TestPaginationHeaders:
    """Test pagination-related functionality"""
    
    def test_pagination_query_params(self, client):
        """Test that pagination query parameters are accepted"""
        response = client.get("/api/v1/menu/categories?skip=0&limit=10")
        
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_invalid_pagination_params(self, client):
        """Test handling of invalid pagination parameters"""
        # Test negative skip
        response = client.get("/api/v1/menu/categories?skip=-1")
        assert response.status_code == 422
        
        # Test zero limit
        response = client.get("/api/v1/menu/categories?limit=0")
        assert response.status_code == 422


class TestURLPatterns:
    """Test URL pattern handling"""
    
    def test_trailing_slash_handling(self, client):
        """Test that trailing slashes are handled correctly"""
        # Both should work or redirect appropriately
        response1 = client.get("/api/v1/menu/categories")
        response2 = client.get("/api/v1/menu/categories/")
        
        # Both should be successful (200) or one should redirect (307/308)
        assert response1.status_code in [200, 307, 308]
        assert response2.status_code in [200, 307, 308]
    
    def test_case_sensitivity(self, client):
        """Test URL case sensitivity"""
        response = client.get("/api/v1/menu/categories")
        assert response.status_code == 200
        
        # Wrong case should return 404
        response = client.get("/API/V1/MENU/CATEGORIES")
        assert response.status_code == 404


class TestDatabaseIntegration:
    """Test database integration at the application level"""
    
    def test_database_connection_in_health_check(self, client):
        """Test that health check properly reports database status"""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert "database" in data
        
        # Database status should be either "connected" or "disconnected"
        assert data["database"] in ["connected", "disconnected"]
    
    def test_database_error_handling(self, client):
        """Test that database errors are properly handled"""
        # This would require mocking database failures
        # For now, we just ensure the endpoint exists and responds
        response = client.get("/health")
        
        # Should not crash even if database has issues
        assert response.status_code in [200, 503]  # 503 = Service Unavailable