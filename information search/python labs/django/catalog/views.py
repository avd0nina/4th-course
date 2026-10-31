from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.shortcuts import render
from .forms import StudentForm, UniversityForm
from .models import Student, University

def home(request):
    return render(
        request,
        "catalog/home.html",
        {"university_count": University.objects.count(), "student_count": Student.objects.count()},
    )

class UniversityListView(ListView):
    model = University
    context_object_name = "universities"
    template_name = "catalog/university_list.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(Q(full_name__icontains=query) | Q(short_name__icontains=query))
        return queryset

class UniversityDetailView(DetailView):
    model = University
    context_object_name = "university"
    template_name = "catalog/university_detail.html"

class UniversityCreateView(CreateView):
    model = University
    form_class = UniversityForm
    template_name = "catalog/form.html"
    extra_context = {"title": "Добавить университет", "entity_name": "университет"}

    def form_valid(self, form):
        messages.success(self.request, "Университет создан.")
        return super().form_valid(form)

class UniversityUpdateView(UpdateView):
    model = University
    form_class = UniversityForm
    template_name = "catalog/form.html"
    extra_context = {"title": "Изменить университет", "entity_name": "университет"}

    def form_valid(self, form):
        messages.success(self.request, "Данные университета обновлены.")
        return super().form_valid(form)

class UniversityDeleteView(DeleteView):
    model = University
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("university-list")

    def form_valid(self, form):
        messages.success(self.request, "Университет удален.")
        return super().form_valid(form)

class StudentListView(ListView):
    model = Student
    context_object_name = "students"
    template_name = "catalog/student_list.html"
    paginate_by = 20

    def get_queryset(self):
        queryset = Student.objects.select_related("university")
        query = self.request.GET.get("q", "").strip()
        university_id = self.request.GET.get("university", "").strip()
        if query:
            queryset = queryset.filter(
                Q(full_name__icontains=query)
                | Q(university__full_name__icontains=query)
                | Q(university__short_name__icontains=query)
            )
        if university_id.isdigit():
            queryset = queryset.filter(university_id=university_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["universities"] = University.objects.all()
        return context


class StudentDetailView(DetailView):
    model = Student
    context_object_name = "student"
    template_name = "catalog/student_detail.html"

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "catalog/form.html"
    extra_context = {"title": "Добавить студента", "entity_name": "студента"}

    def form_valid(self, form):
        messages.success(self.request, "Студент создан.")
        return super().form_valid(form)

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "catalog/form.html"
    extra_context = {"title": "Изменить студента", "entity_name": "студента"}

    def form_valid(self, form):
        messages.success(self.request, "Данные студента обновлены.")
        return super().form_valid(form)

class StudentDeleteView(DeleteView):
    model = Student
    template_name = "catalog/confirm_delete.html"
    success_url = reverse_lazy("student-list")

    def form_valid(self, form):
        messages.success(self.request, "Студент удален.")
        return super().form_valid(form)
