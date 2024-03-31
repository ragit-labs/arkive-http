from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    DateTime,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB, ENUM
import uuid
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from ..enums import SignInProvider


class Base(DeclarativeBase):
    pass


user_post_association = Table(
    "user_post",
    Base.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id"), primary_key=True),
    Column("post_id", UUID(as_uuid=True), ForeignKey("post.id"), primary_key=True),
)

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
    users: Mapped[List[User]] = relationship(
        "User", back_populates="posts", secondary=user_post_association, lazy="selectin"
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
    posts: Mapped[List[Post]] = relationship(
        "Post", back_populates="users", secondary=user_post_association, lazy="selectin"
    )
