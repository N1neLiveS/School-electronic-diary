from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

# Custom User model
class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True
    )

    classes = models.ManyToManyField('Class', blank=True, related_name="teachers")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.is_teacher and not Teacher.objects.filter(user=self).exists():
            Teacher.objects.get_or_create(user=self, name=self.get_full_name())
        else:
            Teacher.objects.filter(user=self).delete()

        if self.is_student and not Student.objects.filter(user=self).exists():
            Student.objects.get_or_create(user=self, name=self.get_full_name())
        else:
            Student.objects.filter(user=self).delete()

        if self.is_parent and not Parent.objects.filter(user=self).exists():
            Parent.objects.get_or_create(user=self, name=self.get_full_name())
        else:
            Parent.objects.filter(user=self).delete()


class Administrator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="teacher_profile")
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    grade_level = models.CharField(max_length=10)

    def count_absences(self):
        return Attendance.objects.filter(student=self, status=False).count()

    def __str__(self):
        return self.name


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Material(models.Model):
    material_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.subject.name


class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    description = models.TextField()
    deadline = models.DateField()

    def __str__(self):
        return str(self.task_id)


class Homework(models.Model):
    homework_id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateField()

    def __str__(self):
        return str(self.homework_id)


class Class(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    day = models.DateField(default=timezone.now)
    time = models.CharField(max_length=20)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='schedules', null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_schedules', null=True, blank=True)
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='schedules', null=True)

    def __str__(self):
        return f"{self.subject.name} - {self.class_name.name} ({self.day})"


class Attendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.BooleanField()
    reason_for_absence = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.name} - {self.date}"


class Grade(models.Model):
    grade_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="grades")
    score = models.FloatField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.name}: {self.score} ({self.subject.name})"
