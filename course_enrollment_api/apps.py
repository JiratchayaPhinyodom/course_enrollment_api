"""
course_enrollment_api Django application initialization.
"""

from django.apps import AppConfig
from edx_django_utils.plugins import PluginURLs


class CourseEnrollmentApiConfig(AppConfig):
    """
    Configuration for the course_enrollment_api Django application.
    """

    name = "course_enrollment_api"

    plugin_app = {
        PluginURLs.CONFIG: {
            # Hook into LMS
            "lms.djangoapp": {
                PluginURLs.NAMESPACE: "course_enrollment_api",
                PluginURLs.REGEX: r"^api/enrollment/",
                PluginURLs.RELATIVE_PATH: "urls",
            },
            # Hook into CMS if you want (optional)
            "cms.djangoapp": {
                PluginURLs.NAMESPACE: "course_enrollment_api",
                PluginURLs.REGEX: r"^api/enrollment/",
                PluginURLs.RELATIVE_PATH: "urls",
            },
        },
        # (Optional: You can add PluginSettings or PluginSignals later if needed)
    }
