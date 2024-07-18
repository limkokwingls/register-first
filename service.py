import logging

from config.firebase import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_student_number(doc_id: str, std_num):
    doc_ref = db.collection("registrations").document(doc_id)
    doc_ref.update({"stdNo": int(std_num)})
    logger.info(f"Updated student number for {doc_id} to {std_num}")
    return True
