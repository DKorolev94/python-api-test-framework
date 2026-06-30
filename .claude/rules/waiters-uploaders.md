---
# Waiters & Uploaders

Rules for polling/retry/sleep logic and complex upload protocols.
No path restriction — architectural rules for the whole project.

## Wait / Retry / Sleep

Do not put in `service/`. Service is for synchronous successful actions.

**Bad:**
```python
class UserService:
    def wait_for_user_active(self, user_id: int) -> UserResponse:
        for _ in range(10):
            user = self.get_user(user_id)
            if user.status == "active":
                return user
            time.sleep(1)
        raise TimeoutError("User not active")
```

**Good — extract to `waiters/`:**
```python
# waiters/user_waiter.py
def wait_for_user_active(user_service: UserService, user_id: int, timeout: int = 10) -> UserResponse:
    """Polls until user status is 'active'. Raises TimeoutError on timeout."""
    for _ in range(timeout):
        user = user_service.get_user(user_id)
        if user.status == "active":
            return user
        time.sleep(1)
    raise TimeoutError(f"User {user_id} not active after {timeout}s")
```

Waiter **can** use service. Service **must not** contain waiter logic.

## Upload logic

If upload is simple — keep in service:

```python
def upload_file(self, path: str) -> FileResponse:
    with open(path, "rb") as f:
        response = self.api.upload(files={"file": f})
    response.raise_for_status()
    return FileResponse.model_validate(response.json())
```

If upload is complex (chunk/resumable/multi-step protocol) — extract to `uploaders/`:

```python
# uploaders/resumable_uploader.py
class ResumableUploader:
    def __init__(self, api):
        self.api = api

    def upload(self, path: str) -> UploadResult:
        session = self._create_session(path)
        for chunk in self._split_file(path):
            self._upload_chunk(session.id, chunk)
        return self._finalize(session.id)
```

Service must not know the details of chunk protocol.

## Where what lives

| What | Where |
|---|---|
| Simple 1-2 line poll | directly in test or fixture |
| Reusable polling | `waiters/` |
| Simple upload | in `service` |
| Chunk/resumable upload | `uploaders/` |
