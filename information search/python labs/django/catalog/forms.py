from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Student, University

class DateInput(forms.DateInput):
    input_type = "date"

class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ["full_name", "short_name", "founded_date"]
        widgets = {"founded_date": DateInput(format="%Y-%m-%d")}

    def clean_founded_date(self):
        value = self.cleaned_data["founded_date"]
        if value > timezone.localdate():
            raise ValidationError("Дата создания не может быть в будущем.")
        return value

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["full_name", "birth_date", "university", "enrollment_year"]
        widgets = {"birth_date": DateInput(format="%Y-%m-%d")}

    def clean(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get("birth_date")
        enrollment_year = cleaned_data.get("enrollment_year")
        if birth_date and birth_date > timezone.localdate():
            self.add_error("birth_date", "Дата рождения не может быть в будущем.")
        if birth_date and enrollment_year and enrollment_year < birth_date.year:
            self.add_error(
                "enrollment_year",
                "Год поступления не может быть раньше года рождения.",
            )
        return cleaned_data
