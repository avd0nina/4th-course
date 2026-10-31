from datetime import date
from django.test import TestCase
from django.urls import reverse
from .models import Student, University

class CrudFlowTests(TestCase):
    def setUp(self):
        self.university = University.objects.create(
            full_name="Новосибирский государственный университет",
            short_name="НГУ",
            founded_date=date(1959, 1, 1),
        )

    def test_university_crud(self):
        response = self.client.get(reverse("university-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Новосибирский государственный университет")
        response = self.client.post(
            reverse("university-create"),
            {
                "full_name": "Тестовый университет",
                "short_name": "ТУ",
                "founded_date": "2000-01-01",
            },
        )
        self.assertEqual(response.status_code, 302)
        university = University.objects.get(short_name="ТУ")
        response = self.client.post(
            reverse("university-update", kwargs={"pk": university.pk}),
            {
                "full_name": "Обновленный университет",
                "short_name": "ОУ",
                "founded_date": "2001-01-01",
            },
        )
        self.assertEqual(response.status_code, 302)
        university.refresh_from_db()
        self.assertEqual(university.short_name, "ОУ")
        response = self.client.post(reverse("university-delete", kwargs={"pk": university.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(University.objects.filter(pk=university.pk).exists())

    def test_student_crud_and_university_relation(self):
        response = self.client.post(
            reverse("student-create"),
            {
                "full_name": "Иванов Иван Иванович",
                "birth_date": "2002-05-10",
                "university": self.university.pk,
                "enrollment_year": 2020,
            },
        )
        self.assertEqual(response.status_code, 302)
        student = Student.objects.get(full_name="Иванов Иван Иванович")
        self.assertEqual(student.university, self.university)
        response = self.client.get(reverse("student-detail", kwargs={"pk": student.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Новосибирский государственный университет")
        response = self.client.post(
            reverse("student-update", kwargs={"pk": student.pk}),
            {
                "full_name": "Петров Петр Петрович",
                "birth_date": "2002-05-10",
                "university": self.university.pk,
                "enrollment_year": 2021,
            },
        )
        self.assertEqual(response.status_code, 302)
        student.refresh_from_db()
        self.assertEqual(student.full_name, "Петров Петр Петрович")
        response = self.client.post(reverse("student-delete", kwargs={"pk": student.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=student.pk).exists())

    def test_student_cannot_be_created_without_university(self):
        response = self.client.post(
            reverse("student-create"),
            {
                "full_name": "Студент Без Университета",
                "birth_date": "2002-05-10",
                "enrollment_year": 2020,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Student.objects.filter(full_name="Студент Без Университета").exists())
