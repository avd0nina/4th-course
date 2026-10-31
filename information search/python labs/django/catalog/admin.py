from django.contrib import admin

from .models import Student, University

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ("full_name", "short_name", "founded_date", "student_count")
    search_fields = ("full_name", "short_name")
    list_filter = ("founded_date",)
    date_hierarchy = "founded_date"

    @admin.display(description="студентов")
    def student_count(self, obj):
        return obj.students.count()

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "university", "birth_date", "enrollment_year")
    search_fields = ("full_name", "university__full_name", "university__short_name")
    list_filter = ("university", "enrollment_year")
    list_select_related = ("university",)
