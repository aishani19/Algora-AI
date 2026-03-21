import time
import traceback
print("Starting passlib test...")
start = time.time()
try:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    print("Hashing password...")
    h = pwd_context.hash("password123")
    print(f"Hash complete in {time.time() - start:.2f}s: {h}")
    print("Verifying...")
    v = pwd_context.verify("password123", h)
    print(f"Verify complete in {time.time() - start:.2f}s: {v}")
except Exception as e:
    traceback.print_exc()
