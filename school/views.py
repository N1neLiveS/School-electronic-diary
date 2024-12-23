from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Schedule, Student, Teacher, Parent, Grade

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно!")
            return redirect('login')
        else:
            messages.error(request, "Ошибка в форме.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Вы успешно вошли в систему!")
            return redirect('base')

        else:
            messages.error(request, "Ошибка входа. Проверьте имя пользователя и пароль.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

@login_required
def schedule_view(request):
    schedule = []

    if hasattr(request.user, 'teacher'):
        teacher = Teacher.objects.filter(user=request.user).first()
        print("Teacher:", teacher)  # Отладка
        schedule = Schedule.objects.filter(teacher=teacher)
    elif hasattr(request.user, 'student'):
        student = Student.objects.filter(user=request.user).first()
        print("Student:", student)  # Отладка
        schedule = Schedule.objects.filter(student=student)
    elif hasattr(request.user, 'parent'):
        parent = Parent.objects.filter(user=request.user).first()
        print("Parent:", parent)  # Отладка
        students = Student.objects.filter(parent=parent)
        schedule = Schedule.objects.filter(student__in=students)
    else:
        print("Unknown role")
        schedule = None

    # Подсчет пропущенных занятий для каждого студента в расписании
    if schedule:
        for entry in schedule:
            if entry.student:
                entry.absences_count = entry.student.count_absences()
            else:
                entry.absences_count = 0  # Если студента нет, то 0

    print("Schedule:", schedule)  # Отладка
    return render(request, 'schedule.html', {'schedule': schedule})



class CustomLogoutView(View):
    next_page = 'login'
    def post(self, request):
        logout(request)
        return redirect(self.next_page)
    def get(self, request):
        return redirect(self.next_page)
    def dispatch(self, request, *args, **kwargs):
        self.next_page = kwargs.get('next_page', self.next_page)
        return super().dispatch(request, *args, **kwargs)

@login_required
def homework(request):
    return render(request, 'homework.html')

@login_required
def grades_view(request):
    grades = Grade.objects.all()  # Все оценки
    is_teacher = hasattr(request.user, 'teacher_profile')  # Проверяем, является ли пользователь учителем

    for grade in grades:
        print(f"Grade ID: {grade.grade_id}, Student: {grade.student}, Subject: {grade.subject.name}, Score: {grade.score}")
    print("Is teacher:", is_teacher)
    context = {
        'grades': grades,
        'is_teacher': is_teacher
    }

    return render(request, 'grades.html', context)

def is_teacher(user):
    return hasattr(user, 'teacher_profile')  # Проверяем, является ли пользователь учителем

@login_required
@user_passes_test(is_teacher)
def edit_grade(request, grade_id):
    grade = get_object_or_404(Grade, grade_id=grade_id)

    if request.method == 'POST':
        new_score = request.POST.get('score')
        grade.score = float(new_score)
        grade.save()
        return redirect('grades_view')  # Перенаправляем на страницу с оценками

    return render(request, 'edit_grade.html', {'grade': grade})

@login_required
def materials(request):
    return render(request, 'materials.html')
def base(request):
    return render(request, 'base.html')