# ======================================================
# data/questions.py
# ملف الدمج - يجمع جميع الأسئلة من الملفات الخمسة
# ======================================================

from data.questions_part1 import QUESTIONS_PART1
from data.questions_part2 import QUESTIONS_PART2
from data.questions_part3 import QUESTIONS_PART3
from data.questions_part4 import QUESTIONS_PART4
from data.questions_part5 import QUESTIONS_PART5

# دمج القوائم الخمسة في قائمة واحدة (600 سؤال)
ALL_QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2 + QUESTIONS_PART3 + QUESTIONS_PART4 + QUESTIONS_PART5

# التحقق من عدم تكرار معرفات الأسئلة (IDs)
def validate_unique_ids(questions_list):
    """يتحقق من عدم تكرار معرفات الأسئلة."""
    ids = [q['id'] for q in questions_list]
    duplicates = [x for x in ids if ids.count(x) > 1]
    if duplicates:
        unique_duplicates = list(set(duplicates))
        raise ValueError(f"توجد معرفات أسئلة مكررة: {unique_duplicates}")
    return True

validate_unique_ids(ALL_QUESTIONS)

QUESTIONS = ALL_QUESTIONS