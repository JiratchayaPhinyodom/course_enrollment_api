from django.apps import AppConfig
from edx_django_utils.plugins import PluginURLs

class CourseEnrollmentApiConfig(AppConfig):
    """
    Configuration for the course_enrollment_api Django application.
    """

    name = "course_enrollment_api"

    plugin_app = {
        PluginURLs.CONFIG: {
            "lms.djangoapp": {
                PluginURLs.NAMESPACE: "course_enrollment_api",
                PluginURLs.REGEX: r"^plugin/enrollment-api/",
                PluginURLs.RELATIVE_PATH: "urls",
            },
        },
    }
