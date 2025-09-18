from django.urls import re_path
from . import views

urlpatterns = [
    re_path(
        r"^course/(?P<course_id>[\w-]+)/enrollments$",
        views.enroll_user,
        name="course_enrollments",
    ),
]
