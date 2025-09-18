"""
URLs for course_enrollment_api.
"""
from django.urls import re_path  # pylint: disable=unused-import
from django.views.generic import TemplateView  # pylint: disable=unused-import

# urlpatterns = [
#     # : Fill in URL patterns and views here.
#     # re_path(r'', TemplateView.as_view(template_name="course_enrollment_api/base.html")),
# ]

urlpatterns = [
    # Match /course/<course_id>/enrollments
    re_path(r'^course/(?P<course_id>[\w-]+)/enrollments$', views.enroll_user, name='course_enrollments'),
]