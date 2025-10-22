from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect

class TeacherRequiredMixin(UserPassesTestMixin):
    """Разрешает доступ только учителям (user.role == 'teacher')."""
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == "teacher"

    def handle_no_permission(self):
        return redirect("no_permission")
