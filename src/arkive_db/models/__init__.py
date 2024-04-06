from __future__ import annotations

import uuid
from datetime import datetime
from typing import List

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ENUM, JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from ..enums import SignInProvider


class Base(DeclarativeBase):
    pass


tag_post_association = Table(
    "tag_post",
    Base.metadata,
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tag.id"), primary_key=True),
    Column("post_id", UUID(as_uuid=True), ForeignKey("post.id"), primary_key=True),
)


class Post(Base):
    __tablename__ = "post"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4()
    )
    title: Mapped[str] = mapped_column(Text(), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    url: Mapped[str] = mapped_column(String(), nullable=False)
    banner: Mapped[str] = mapped_column(String(), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(), nullable=False)
    extra_metadata: Mapped[dict] = mapped_column(JSONB(), nullable=True)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    tags: Mapped[List[Tag]] = relationship(
        "Tag", back_populates="posts", secondary=tag_post_association, lazy="selectin"
    )


class Tag(Base):
    __tablename__ = "tag"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4()
    )
    name: Mapped[str] = mapped_column(String(), nullable=False, unique=True)
    extra_metadata: Mapped[dict] = mapped_column(JSONB(), nullable=True)
    posts: Mapped[List[Post]] = relationship(
        "Post", back_populates="tags", secondary=tag_post_association, lazy="selectin"
    )
    __table_args__ = (UniqueConstraint("name", name="tag_name_unique"),)


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4()
    )
    full_name: Mapped[str] = mapped_column(String(), nullable=False)
    first_name: Mapped[str] = mapped_column(String(), nullable=False)
    last_name: Mapped[str] = mapped_column(String(), nullable=True)
    email: Mapped[str] = mapped_column(String(), nullable=False)
    password: Mapped[str] = mapped_column(
        String(), nullable=True  # TODO: add password encryption later
    )
    display_picture_url: Mapped[str] = mapped_column(String(), nullable=True)
    signin_provider: Mapped[SignInProvider] = mapped_column(
        ENUM(SignInProvider), nullable=False
    )
    extra_metadata: Mapped[dict] = mapped_column(JSONB(), nullable=True)
