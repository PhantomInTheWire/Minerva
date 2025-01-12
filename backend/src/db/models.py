import sqlalchemy.dialects.postgresql as pg
from typing import Optional
from sqlmodel import SQLModel, Field, Column
import uuid
from datetime import datetime

class PDFDocument(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str = Field(max_length=255, nullable=False)
    upload_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    file_content: str = Field(sa_column=Column(pg.TEXT, default=""))

    def __repr__(self) -> str:
        return f"<User {self.name}>"
