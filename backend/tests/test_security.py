import os
import importlib
import pytest
from app.core import security

def test_password_hash_and_verify():
    pwd = "secret-password-123"
    hashed = security.get_password_hash(pwd)
    assert security.verify_password(pwd, hashed)
    assert not security.verify_password("wrong-password", hashed)

def test_jwt_create_and_decode():
    payload = {"sub": "12345678-1234-1234-1234-123456789abc", "role": "FARMER"}
    token = security.create_access_token(payload)
    decoded = security.decode_access_token(token)
    assert decoded is not None
    assert decoded["sub"] == payload["sub"]
    assert decoded["role"] == "FARMER"

def test_jwt_tampered_token_fails():
    payload = {"sub": "12345678-1234-1234-1234-123456789abc"}
    token = security.create_access_token(payload)
    parts = token.split(".")
    tampered_payload = parts[1][:-2] + "AA"
    tampered_token = f"{parts[0]}.{tampered_payload}.{parts[2]}"
    assert security.decode_access_token(tampered_token) is None

def test_jwt_secret_unset_fails_loudly(monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    with pytest.raises(RuntimeError, match="CRITICAL SECURITY ERROR: JWT_SECRET"):
        importlib.reload(security)
    # Restore valid test secret
    monkeypatch.setenv("JWT_SECRET", "test-secret-key-1234567890-secure")
    importlib.reload(security)
