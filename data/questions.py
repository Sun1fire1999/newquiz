# ======================================================
# data/questions.py
# ملف الدمج - يجمع جميع الأسئلة من الملفات الأربعة
# ======================================================

from data.questions_part1 import QUESTIONS_PART1
from data.questions_part2 import QUESTIONS_PART2
from data.questions_part3 import QUESTIONS_PART3
from data.questions_part4 import QUESTIONS_PART4

# دمج القوائم الأربعة في قائمة واحدة (400 سؤال)
ALL_QUESTIONS = QUESTIONS_PART1 + QUESTIONS_PART2 + QUESTIONS_PART3 + QUESTIONS_PART4

# التحقق من عدم تكرار معرفات الأسئلة (IDs)
def validate_unique_ids(questions_list):
    """
    تتحقق هذه الدالة من أن جميع معرفات الأسئلة (id) فريدة ولا يوجد أي تكرار.
    إذا وجدت تكراراً، يتم رفع خطأ (ValueError) يمنع تشغيل التطبيق.
    """
    ids = [q['id'] for q in questions_list]
    duplicates = [x for x in ids if ids.count(x) > 1]
    
    if duplicates:
        # إزالة التكرارات لعرض الأرقام المكررة فقط
        unique_duplicates = list(set(duplicates))
        raise ValueError(f"توجد معرفات أسئلة مكررة: {unique_duplicates}")
    
    return True

# استدعاء دالة التحقق (سيتوقف التطبيق إذا كان هناك تكرار)
validate_unique_ids(ALL_QUESTIONS)

# القائمة النهائية التي سيتم استيرادها في التطبيق الرئيسي (app.py)
QUESTIONS = ALL_QUESTIONS