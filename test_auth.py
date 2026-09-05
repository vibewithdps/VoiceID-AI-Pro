from app.auth.auth_manager import AuthManager
auth = AuthManager()
print(auth.register("Test User", "testuser", "test@test.com", "Password123!", "Password123!"))
