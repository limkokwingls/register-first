from datetime import datetime
from enum import StrEnum
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Gender(StrEnum):
    MALE = "Male"
    FEMALE = "Female"


class Religion(StrEnum):
    CHRISTIAN = "Christian"
    MUSLIM = "Muslim"
    HINDU = "Hindu"
    BUDDHIST = "Buddhist"
    OTHER = "Other"


class MaritalStatus(StrEnum):
    SINGLE = "Single"
    MARRIED = "Married"
    DIVORCED = "Divorced"
    WIDOWED = "Widowed"
    OTHER = "Other"


class NextOfKinRelationship(StrEnum):
    FATHER = "Father"
    MOTHER = "Mother"
    BROTHER = "Brother"
    SISTER = "Sister"
    SPOUSE = "Spouse"
    CHILD = "Child"
    OTHER = "Other"


class Student(Base):
    __tablename__: str = "students"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    std_no: Mapped[str] = mapped_column(String)
    national_id: Mapped[str] = mapped_column(String, nullable=False)
    reference: Mapped[Optional[str]] = mapped_column(String)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    phone1: Mapped[str] = mapped_column(String, nullable=False)
    phone2: Mapped[Optional[str]] = mapped_column(String)
    religion: Mapped[Religion] = mapped_column(nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    gender: Mapped[Gender] = mapped_column(nullable=False)
    marital_status: Mapped[MaritalStatus] = mapped_column(nullable=False)
    birth_place: Mapped[str] = mapped_column(String, nullable=False)
    home_town: Mapped[str] = mapped_column(String, nullable=False)
    high_school: Mapped[str] = mapped_column(String, nullable=False)
    next_of_kin_name: Mapped[str] = mapped_column(String, nullable=False)
    next_of_kin_phone: Mapped[str] = mapped_column(String, nullable=False)
    next_of_kin_relationship: Mapped[NextOfKinRelationship] = mapped_column(
        nullable=False
    )
    paid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    __table_args__ = (
        Index("student_email_idx", "email"),
        Index("student_national_id_idx", "national_id"),
        Index("student_name_idx", "name"),
    )
