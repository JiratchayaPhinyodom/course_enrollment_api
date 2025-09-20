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
        is_active = data.get("is_active", True)

        if not email:
            return JsonResponse({"error": "Email is required"}, status=400)

        # LMS enrollment API
        api_url = f"https://{LMS_HOST}/api/enrollment/v1/enrollment"
        payload = {
            "email": email,
            "course_id": course_id,
            "mode": mode,
            "is_active": is_active,
        }

        # Forward Authorization header if present
        headers = {"Content-Type": "application/json"}
        auth_header = request.headers.get("Authorization")
        if auth_header:
            headers["Authorization"] = auth_header

        # Call LMS API
        resp = requests.post(api_url, json=payload, headers=headers, verify=True)

        try:
            response_data = resp.json()
        except ValueError:
            response_data = {"error": "Invalid response from LMS", "text": resp.text}

        return JsonResponse(response_data, status=resp.status_code)

    except requests.exceptions.SSLError:
        return JsonResponse(
            {"error": "SSL verification failed. Check your LMS certificate."},
            status=500,
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
