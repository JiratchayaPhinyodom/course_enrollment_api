import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from lms.djangoapps.enrollments.models import CourseEnrollment

User = get_user_model()

@csrf_exempt
def enroll_user(request, course_id):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        is_active = data.get("is_active", True)
        mode = data.get("mode", "honor")

        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        # Get or create the user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split("@")[0]}
        )

        # Optionally create a blank social auth if new user
        if created:
            from social_django.models import UserSocialAuth
            UserSocialAuth.objects.get_or_create(user=user, provider="", uid="")

        # Enroll the user
        CourseEnrollment.enroll(user, course_id, mode=mode, is_active=is_active)

        return JsonResponse({"status": "success", "user_created": created})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
