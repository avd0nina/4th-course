from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("universities/", views.UniversityListView.as_view(), name="university-list"),
    path("universities/create/", views.UniversityCreateView.as_view(), name="university-create"),
    path("universities/<int:pk>/", views.UniversityDetailView.as_view(), name="university-detail"),
    path("universities/<int:pk>/update/", views.UniversityUpdateView.as_view(), name="university-update"),
    path("universities/<int:pk>/delete/", views.UniversityDeleteView.as_view(), name="university-delete"),
    path("students/", views.StudentListView.as_view(), name="student-list"),
    path("students/create/", views.StudentCreateView.as_view(), name="student-create"),
    path("students/<int:pk>/", views.StudentDetailView.as_view(), name="student-detail"),
    path("students/<int:pk>/update/", views.StudentUpdateView.as_view(), name="student-update"),
    path("students/<int:pk>/delete/", views.StudentDeleteView.as_view(), name="student-delete"),
]
