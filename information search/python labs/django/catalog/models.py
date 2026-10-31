from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

class University(models.Model):
    full_name = models.CharField("полное название", max_length=255, unique=True)
    short_name = models.CharField("сокращенное название", max_length=50, unique=True)
    founded_date = models.DateField("дата создания")

    class Meta:
        ordering = ["full_name"]
        verbose_name = "университет"
        verbose_name_plural = "университеты"

    def __str__(self):
        return f"{self.short_name} — {self.full_name}"

    def get_absolute_url(self):
        return reverse("university-detail", kwargs={"pk": self.pk})

class Student(models.Model):
    full_name = models.CharField("ФИО", max_length=255)
    birth_date = models.DateField("дата рождения")
    university = models.ForeignKey(
        University,
        on_delete=models.PROTECT,
        related_name="students",
        verbose_name="университет",
    )
    enrollment_year = models.PositiveSmallIntegerField(
        "год поступления",
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
    )

    class Meta:
        ordering = ["full_name"]
        verbose_name = "студент"
        verbose_name_plural = "студенты"

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})
