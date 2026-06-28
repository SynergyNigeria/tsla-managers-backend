from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import ManagerApplication


def frontend_page(request, page):
    return render(request, page)


def with_cors(response):
    return response


def validate_file(file, allowed_types, field_name):
    if file.content_type not in allowed_types and not any(
        file.content_type.startswith(prefix) for prefix in allowed_types if prefix.endswith("/")
    ):
        return f"{field_name} has an unsupported file type."

    if file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
        return f"{field_name} is too large."

    return ""


@csrf_exempt
@require_POST
def create_application(request):
    required_fields = [
        "firstName",
        "lastName",
        "email",
        "phone",
        "city",
        "state",
        "showroom",
        "networth",
        "education",
        "managementYears",
        "onlineInterview",
    ]
    missing_field = next((field for field in required_fields if not request.POST.get(field)), None)

    if missing_field:
        return with_cors(JsonResponse({"error": f"{missing_field} is required."}, status=400))

    id_proof = request.FILES.get("idProof")
    cv = request.FILES.get("cv")

    if not id_proof:
        return with_cors(JsonResponse({"error": "ID proof is required."}, status=400))

    id_error = validate_file(id_proof, ["image/", "application/pdf"], "ID proof")

    if id_error:
        return with_cors(JsonResponse({"error": id_error}, status=400))

    if cv:
        cv_error = validate_file(cv, ["application/pdf"], "CV")

        if cv_error:
            return with_cors(JsonResponse({"error": cv_error}, status=400))

    try:
        networth = int(request.POST["networth"])
    except ValueError:
        return with_cors(JsonResponse({"error": "networth must be a number."}, status=400))

    application = ManagerApplication.objects.create(
        first_name=request.POST["firstName"].strip(),
        last_name=request.POST["lastName"].strip(),
        email=request.POST["email"].strip().lower(),
        phone=request.POST["phone"].strip(),
        city=request.POST["city"].strip(),
        state=request.POST["state"].strip(),
        showroom=request.POST["showroom"].strip(),
        networth=networth,
        education=request.POST["education"].strip(),
        management_years=request.POST["managementYears"].strip(),
        management_history=request.POST.get("managementHistory", "").strip(),
        online_interview=request.POST["onlineInterview"].strip(),
        id_proof=id_proof,
        cv=cv,
    )

    return with_cors(JsonResponse({"application": application.public_payload()}, status=201))


@require_GET
def application_status(request, application_id):
    email = request.GET.get("email", "").strip().lower()

    if not email:
        return with_cors(JsonResponse({"error": "Email is required."}, status=400))

    try:
        application = ManagerApplication.objects.get(
            application_id=application_id.upper(),
            email=email,
        )
    except ManagerApplication.DoesNotExist:
        return with_cors(JsonResponse({"error": "Application not found."}, status=404))

    return with_cors(JsonResponse({"application": application.public_payload()}))


@csrf_exempt
@require_POST
def update_car_capacity(request, application_id):
    email = request.POST.get("email", "").strip().lower()

    if not email:
        return with_cors(JsonResponse({"error": "Email is required."}, status=400))

    try:
        capacity = int(request.POST.get("carCapacity", ""))
    except ValueError:
        return with_cors(JsonResponse({"error": "Car capacity must be a number."}, status=400))

    if capacity < 50 or capacity > 500:
        return with_cors(JsonResponse({"error": "Car capacity must be between 50 and 500."}, status=400))

    try:
        application = ManagerApplication.objects.get(
            application_id=application_id.upper(),
            email=email,
        )
    except ManagerApplication.DoesNotExist:
        return with_cors(JsonResponse({"error": "Application not found."}, status=404))

    if application.status != "Accepted":
        return with_cors(JsonResponse({"error": "Only accepted applicants can submit showroom capacity."}, status=403))

    application.car_capacity = capacity
    application.save(update_fields=["car_capacity", "updated_at"])

    return with_cors(JsonResponse({"application": application.public_payload()}))
