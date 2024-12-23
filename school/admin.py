from django.contrib import admin
from .models import User, Administrator, Teacher, Student, Parent, Material, Task, Homework, Schedule, Attendance, Grade, Subject, Class

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_teacher', 'is_student', 'is_parent')
    search_fields = ('username', 'email')

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    search_fields = ('name',)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'grade_level')
    search_fields = ('name',)

class ParentAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    search_fields = ('name',)

class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('date', 'time', 'subject', 'teacher', 'class_name')
    search_fields = ('class_name', 'subject__subject', 'teacher__name')

admin.site.register(User)
admin.site.register(Administrator)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Material)
admin.site.register(Subject)
admin.site.register(Task)
admin.site.register(Homework)
admin.site.register(Schedule)
admin.site.register(Attendance)
admin.site.register(Grade)
admin.site.register(Class)