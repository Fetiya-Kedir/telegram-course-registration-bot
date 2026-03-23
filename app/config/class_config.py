CLASS_DURATION_MONTHS = {
    "1": 4,  # Exit Exam Preparation
    "2": 4,  # Licensure / COC Exam Preparation
    "3": 4,  # NCLEX Exam Preparation
    "4": 4,  # DHA Exam Preparation
    "5": 4,  # Case to Care Mind Class
    "6": 4,  # Skill Mind Class
}


def get_class_duration_months(class_id: str) -> int:
    return CLASS_DURATION_MONTHS.get(class_id, 1)