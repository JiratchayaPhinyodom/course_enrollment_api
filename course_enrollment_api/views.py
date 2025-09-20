import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from common.djangoapps.student.models import CourseEnrollment
from social_django.models import UserSocialAuth


User = get_user_model()


@csrf_exempt
def enroll_user(request, course_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        mode = data.get("mode", "honor")
        is_active = data.get("is_active", True)

        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        # 1️⃣ Get or create user
        username = email.split("@")[0]  # crude but works for demo
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "is_active": is_active,
            },
        )

        # 2️⃣ Create empty Google social auth if missing
        if not UserSocialAuth.objects.filter(user=user, provider="google-oauth2").exists():
            UserSocialAuth.objects.create(
                user=user,
                provider="google-oauth2",
                uid=email,
            )

        # 3️⃣ Enroll user in course
        CourseEnrollment.enroll(user, course_id, mode=mode, is_active=is_active)

        return JsonResponse(
            {
                "status": "success",
                "user_created": created,
                "enrolled": True,
                "course_id": course_id,
                "email": email,
            }
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
