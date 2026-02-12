
Prashanth Kumar
1:03 PM (0 minutes ago)
to me

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./test.db" # fallback for tests (CI)
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if "sqlite" in DATABASE_URL
    else {}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 🔥 This creates tables automatically (important for CI)
Base.metadata.create_all(bind=engine)