from django.urls import path
from .views import CustomLogoutView
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('schedule/', views.schedule_view, name='schedule'),
    path('logout/', CustomLogoutView.as_view(next_page='login'), name='logout'),
    path('homework/', views.homework, name='homework'),
    path('grades/', views.grades_view, name='grades_view'),
    path('grades/edit/<int:grade_id>/', views.edit_grade, name='edit_grade'),
    path('materials/', views.materials, name='materials'),
]
