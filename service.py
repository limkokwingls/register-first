import logging
from datetime import datetime

from sqlalchemy.orm import Session

from models import Student

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_student_number(
    session: Session, doc_id: str, std_num: str, std: Student = None
):
    if not doc_id and std:
        std.std_no = int(std_num)
        std.created_at = datetime.utcnow()
        session.add(std)
    else:
        student = session.get(Student, doc_id)
        if student:
            student.std_no = int(std_num)
            student.created_at = datetime.utcnow()

    session.commit()
    logger.info(f"Updated student number for {doc_id} to {std_num}")
