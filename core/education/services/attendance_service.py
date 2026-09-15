from core.education.models.education_models import AttendanceRecord

class AttendanceService:
    VALID = {"present", "absent", "late", "leave"}

    def __init__(self):
        self.records = []

    def record(self, teacher_id, date, status,
               check_in=None, check_out=None):
        if status not in self.VALID:
            raise ValueError("INVALID_ATTENDANCE_STATUS")

        item = AttendanceRecord(
            teacher_id=teacher_id,
            date=date,
            status=status,
            check_in=check_in,
            check_out=check_out,
        )
        self.records.append(item)
        return item

    def for_teacher(self, teacher_id):
        return [
            r for r in self.records
            if r.teacher_id == teacher_id
        ]
