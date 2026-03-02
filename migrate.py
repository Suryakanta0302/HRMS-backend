"""Utility for applying database migrations/indexes outside of the
FastAPI application runtime.

This can be useful when you want to prepare a remote MongoDB instance
(before pointing the FastAPI server at it) or to run a one-off maintenance
step.

Usage example:

```bash
# set the URI you want to act against, then run the script
export MONGO_URI="mongodb://mongo:...@turntable.proxy.rlwy.net:36886/hrms"
python migrate.py
```

The script creates the same indexes that `main.startup_event` normally
ensures when the application boots.  It does not touch actual data.
"""

import os
import asyncio

# guard against missing dependencies when script is run outside a virtual
# environment; produce a helpful error rather than a raw Traceback.
try:
    from motor.motor_asyncio import AsyncIOMotorClient
except ImportError as imp_err:
    raise ImportError(
        "required dependency 'motor' is not installed. "
        "run `pip install -r requirements.txt` or activate your virtual env."
    ) from imp_err

async def run_migration(uri: str):
    # mirror main.py logic to support MONGO_USER/MONGO_PASSWORD if the given
    # uri doesn't already include credentials.
    user = os.getenv("MONGO_USER")
    pwd = os.getenv("MONGO_PASSWORD")
    if user and pwd and "@" not in uri.split("//", 1)[-1]:
        from urllib.parse import quote_plus
        suffix = uri.split("//", 1)[-1]
        uri = f"mongodb://{quote_plus(user)}:{quote_plus(pwd)}@{suffix}"
    client = AsyncIOMotorClient(uri)
    db = client.hrms

    print(f"connecting to {uri}")
    try:
        # create indexes exactly as the application does
        await db.employees.create_index("employeeId", unique=True)
        await db.attendance.create_index("date")
        print("indexes created")
    except Exception as exc:
        print("failed to apply migration:", exc)
        raise

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Apply indexes to HRMS MongoDB")
    parser.add_argument(
        "--uri",
        help="MongoDB connection string (overrides MONGO_URI env var)",
    )
    args = parser.parse_args()

    uri = args.uri or os.getenv("MONGO_URI", "mongodb://mongo:BcJAZbGdWrCrhbvgUPsrVVMalICDMKDR@turntable.proxy.rlwy.net:36886/hrms")

    try:
        asyncio.run(run_migration(uri))
        print("migration complete")
    except Exception as exc:
        print("migration failed:", exc)
        raise
