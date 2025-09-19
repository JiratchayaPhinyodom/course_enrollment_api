import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

LMS_HOST = "learn2.ku.th"  # Replace with your LMS domain

@csrf_exempt
def enroll_user(request, course_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    try:
        data = json.loads(request.body)
        email = data.get("email")
        mode = data.get("mode", "honor")
        is_active = data.get("is_active", True)  # Read from request

        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        # Call the internal LMS enrollment API over HTTPS
        api_url = f"https://{LMS_HOST}/api/enrollment/v1/enrollment"
        payload = {
            "email": email,
            "course_id": course_id,
            "mode": mode,
            "is_active": is_active
        }

        # verify=True ensures SSL certificate is checked; set verify=False if self-signed
        resp = requests.post(api_url, json=payload, verify=True)

        return JsonResponse(resp.json(), status=resp.status_code)

    except requests.exceptions.SSLError:
        return JsonResponse({"error": "SSL verification failed. Check your LMS certificate."}, status=500)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
