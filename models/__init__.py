from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Program(Base):
    __tablename__ = "programs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    code: Mapped[str] = mapped_column(String(20))
    students: Mapped[list["Student"]] = relationship(back_populates="program")


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    reference: Mapped[str] = mapped_column(String(50), unique=True)
    national_id: Mapped[str] = mapped_column(String(50), unique=True)
    names: Mapped[str] = mapped_column(String(100))
    std_no: Mapped[Optional[int]] = mapped_column(Integer, unique=True, nullable=True)
    program_id: Mapped[int] = mapped_column(ForeignKey("programs.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    program: Mapped[Program] = relationship(back_populates="students")

    def to_dict(self):
        return {
            "id": self.id,
            "reference": self.reference,
            "nationalId": self.national_id,
            "names": self.names,
            "stdNo": self.std_no,
            "program": {"name": self.program.name, "code": self.program.code},
            "createdAt": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict, id: int = None):
        return cls(
            id=id,
            reference=data.get("reference"),
            national_id=data.get("nationalId"),
            names=data.get("names"),
            std_no=data.get("stdNo"),
            program_id=data.get("program_id"),
        )
