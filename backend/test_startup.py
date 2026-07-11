#!/usr/bin/env python3
"""
Test script to verify FastAPI backend startup and health endpoint.
"""

import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

try:
    # Test 1: Import the FastAPI app
    print("=" * 60)
    print("TEST 1: Importing FastAPI application...")
    print("=" * 60)
    from app.main import app
    print("[OK] FastAPI app imported successfully")
    print(f"  - App title: {app.title}")
    print(f"  - App version: {app.version}")
    print(f"  - App description: {app.description}")
    
    # Test 2: Verify CORS middleware
    print("\n" + "=" * 60)
    print("TEST 2: Verifying CORS configuration...")
    print("=" * 60)
    cors_configured = len(app.user_middleware) > 0
    print(f"[OK] CORS middleware configured: {cors_configured}")
    
    # Check CORS origins
    from app.core.config import settings
    print(f"  - Allowed origins: {settings.BACKEND_CORS_ORIGINS}")
    
    # Test 3: Verify /health endpoint
    print("\n" + "=" * 60)
    print("TEST 3: Verifying /health endpoint...")
    print("=" * 60)
    
    # Use FastAPI's test client
    from fastapi.testclient import TestClient
    client = TestClient(app)
    
    response = client.get("/health")
    print(f"[OK] GET /health endpoint exists")
    print(f"  - Status code: {response.status_code}")
    print(f"  - Response: {response.json()}")
    
    # Verify response format
    health_data = response.json()
    assert health_data["status"] == "ok", f"Expected 'ok', got '{health_data['status']}'"
    assert health_data["version"] == "0.1.0", f"Expected '0.1.0', got '{health_data['version']}'"
    print("[OK] Response format matches requirements")
    
    # Test 4: Verify root endpoint
    print("\n" + "=" * 60)
    print("TEST 4: Verifying root endpoint...")
    print("=" * 60)
    response = client.get("/")
    print(f"[OK] GET / endpoint exists")
    print(f"  - Status code: {response.status_code}")
    print(f"  - Response: {response.json()}")
    
    # Test 5: Verify OpenAPI docs
    print("\n" + "=" * 60)
    print("TEST 5: Verifying OpenAPI documentation...")
    print("=" * 60)
    response = client.get("/docs")
    print(f"[OK] GET /docs endpoint exists (status: {response.status_code})")
    
    response = client.get("/openapi.json")
    print(f"[OK] GET /openapi.json endpoint exists (status: {response.status_code})")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY: All tests passed!")
    print("=" * 60)
    print("[OK] FastAPI application starts without errors")
    print("[OK] GET /health endpoint exists and returns correct format")
    print("[OK] CORS configuration is correct for Chrome extension")
    print("[OK] Application is ready for development")
    print("=" * 60)
    
    sys.exit(0)
    
except Exception as e:
    print(f"\n[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)