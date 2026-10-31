from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db
from app.forms import LoginForm, RegistrationForm, StudentForm, UniversityForm
from app.models import Student, University, User

@app.route("/")
def index():
    return render_template(
        "index.html",
        university_count=db.session.query(University).count(),
        student_count=db.session.query(Student).count(),
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        if db.session.scalar(db.select(User).where(User.username == username)):
            form.username.errors.append("Пользователь с таким логином уже существует.")
        else:
            user = User(username=username)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Регистрация завершена. Теперь войдите в аккаунт.", "success")
            return redirect(url_for("login"))
    return render_template(
        "auth_form.html", form=form, title="Регистрация", submit_label="Зарегистрироваться"
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            db.select(User).where(User.username == form.username.data.strip())
        )
        if user is None or not user.check_password(form.password.data):
            flash("Неверный логин или пароль.", "danger")
        else:
            login_user(user)
            return redirect(url_for("index"))
    return render_template("auth_form.html", form=form, title="Вход", submit_label="Войти")

@app.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта.", "success")
    return redirect(url_for("index"))

@app.get("/universities")
def universities():
    items = db.session.scalars(db.select(University).order_by(University.full_name)).all()
    return render_template("universities/list.html", universities=items)

@app.route("/universities/new", methods=["GET", "POST"])
@login_required
def university_create():
    form = UniversityForm()
    if form.validate_on_submit():
        if _university_duplicate_exists(form):
            return render_template("universities/form.html", form=form, title="Добавить университет")
        university = University(
            full_name=form.full_name.data.strip(),
            short_name=form.short_name.data.strip(),
            foundation_date=form.foundation_date.data,
        )
        db.session.add(university)
        db.session.commit()
        flash("Университет добавлен.", "success")
        return redirect(url_for("universities"))
    return render_template("universities/form.html", form=form, title="Добавить университет")

@app.route("/universities/<int:university_id>/edit", methods=["GET", "POST"])
@login_required
def university_update(university_id):
    university = db.get_or_404(University, university_id)
    form = UniversityForm(obj=university)
    if form.validate_on_submit():
        if _university_duplicate_exists(form, university.id):
            return render_template(
                "universities/form.html", form=form, title="Изменить университет"
            )
        form.populate_obj(university)
        university.full_name = university.full_name.strip()
        university.short_name = university.short_name.strip()
        db.session.commit()
        flash("Университет изменен.", "success")
        return redirect(url_for("universities"))
    return render_template("universities/form.html", form=form, title="Изменить университет")

def _university_duplicate_exists(form, excluded_id=None):
    query = db.select(University).where(
        db.or_(
            db.func.lower(University.full_name) == form.full_name.data.strip().lower(),
            db.func.lower(University.short_name) == form.short_name.data.strip().lower(),
        )
    )
    if excluded_id is not None:
        query = query.where(University.id != excluded_id)
    if db.session.scalar(query):
        form.form_errors.append("Полное или сокращенное название уже используется.")
        return True
    return False

@app.post("/universities/<int:university_id>/delete")
def university_delete(university_id):
    university = db.get_or_404(University, university_id)
    db.session.delete(university)
    db.session.commit()
    flash("Университет и связанные студенты удалены.", "success")
    return redirect(url_for("universities"))

@app.get("/students")
def students():
    items = db.session.scalars(
        db.select(Student).join(Student.university).order_by(Student.full_name)
    ).all()
    return render_template("students/list.html", students=items)

@app.route("/students/new", methods=["GET", "POST"])
@login_required
def student_create():
    form = StudentForm()
    _set_university_choices(form)
    if form.validate_on_submit():
        student = Student(
            full_name=form.full_name.data.strip(),
            birth_date=form.birth_date.data,
            university_id=form.university_id.data,
            admission_year=form.admission_year.data,
        )
        db.session.add(student)
        db.session.commit()
        flash("Студент добавлен.", "success")
        return redirect(url_for("students"))
    return render_template("students/form.html", form=form, title="Добавить студента")

@app.route("/students/<int:student_id>/edit", methods=["GET", "POST"])
@login_required
def student_update(student_id):
    student = db.get_or_404(Student, student_id)
    form = StudentForm(obj=student)
    _set_university_choices(form)
    if form.validate_on_submit():
        form.populate_obj(student)
        student.full_name = student.full_name.strip()
        db.session.commit()
        flash("Данные студента изменены.", "success")
        return redirect(url_for("students"))
    return render_template("students/form.html", form=form, title="Изменить студента")

def _set_university_choices(form):
    universities = db.session.scalars(db.select(University).order_by(University.full_name)).all()
    form.university_id.choices = [
        (university.id, university.full_name) for university in universities
    ]

@app.post("/students/<int:student_id>/delete")
def student_delete(student_id):
    student = db.get_or_404(Student, student_id)
    db.session.delete(student)
    db.session.commit()
    flash("Студент удален.", "success")
    return redirect(url_for("students"))
