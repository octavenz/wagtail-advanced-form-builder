from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.middleware.csrf import CsrfViewMiddleware
from django_recaptcha.client import submit
from ninja import NinjaAPI
from ninja.errors import ValidationError
from wagtail_advanced_form_builder.models import FormPage, EmailFormPage
from .schemas import FormPageSchema, EmailFormPageSchema, FormPageUnion, ThanksPageSchema, FormPostSchema, JSONResponse
from .tasks import send_form_page_email

wagtail_advanced_form_builder_api = NinjaAPI(csrf=True, docs_url='/docs', title='Wagtail Advanced Form Builder API')
api = wagtail_advanced_form_builder_api


@api.exception_handler(ValidationError)
def custom_validation_errors(request, exc):
    print(exc.errors)  # <--------------------- !!!!
    print(request.body)
    return api.create_response(request, {"detail": exc.errors}, status=422)


# Retrieve CSRF Token
@api.get("/csrf/")
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({"csrftoken": token})


def validate_csrf(request):
    csrf_middleware = CsrfViewMiddleware(get_response=lambda req: None)
    try:
        csrf_middleware.process_view(request, None, (), {})
        return True
    except PermissionDenied as e:
        print("Error with validating the CSRF token:", e)
        return False


@api.get(
    "/form_by_path/{path:path}",
    response={200: FormPageUnion, 404: JSONResponse, 500: JSONResponse},
    operation_id="get_form_by_path"
)
def form_by_path(request, path):
    try:
        # Search for forms with the given path - combine both form types
        form_pages = list(FormPage.objects.filter(url_path__icontains=path))
        email_form_pages = list(EmailFormPage.objects.filter(url_path__icontains=path))
        all_forms = form_pages + email_form_pages

        # Handle results
        if not all_forms:
            return 404, {"message": "No form found with the specified path"}
        elif len(all_forms) > 1:
            return 500, {"message": f"Found {len(all_forms)} forms with that path. Please use a more specific path."}

        # Get the single form that found
        form_page = all_forms[0]

        # Use the right schema for the right form page
        if isinstance(form_page, EmailFormPage):
            form = EmailFormPageSchema.from_orm(form_page)
        else:
            form = FormPageSchema.from_orm(form_page)
        return 200, form

    except Exception as e:
        print(f"Error retrieving form: {e}")
        return 500, {"message": "Internal server error while getting form"}


@api.post(
    "/form_by_path/",
    response={204: ThanksPageSchema, 403: JSONResponse, 404: JSONResponse, 500: JSONResponse},
    operation_id="post_form_by_path"
)
def form_by_path(request, data: FormPostSchema):
    try:
        # First, validate CSRF token
        if not validate_csrf(request):
            print("CSRF validation failed")
            return 403, {"message": "CSRF validation failed. Please refresh the page and try again."}

        # Checking if reCAPTCHA validation is required
        recaptcha_validation_required = False

        # Search for forms with the given path - try both form types
        form_pages = list(FormPage.objects.filter(url_path__icontains=data.path))
        email_form_pages = list(EmailFormPage.objects.filter(url_path__icontains=data.path))
        all_forms = form_pages + email_form_pages

        # Handle results
        if not all_forms:
            return 404, {"message": "No form found with the specified path"}
        elif len(all_forms) > 1:
            return 500, {"message": f"Found {len(all_forms)} forms with that path. Please use a more specific path."}

        # Get the single form that found
        form_page = all_forms[0]

        # Check if this form requires reCAPTCHA
        if hasattr(form_page, 'use_google_recaptcha') and form_page.use_google_recaptcha:
            recaptcha_validation_required = True

        # Validating reCAPTCHA token if required recaptcha for the form
        if recaptcha_validation_required:
            recaptcha_token = data.recaptcha_token

            # Skip validation if no token is provided but print a warning
            if not recaptcha_token:
                print("WARNING: Form requires reCAPTCHA but no token was provided")
                return 403, {"message": "reCAPTCHA validation required. Please refresh and try again."}

            # Validate the token
            recaptcha_response = submit(
                recaptcha_token,
                settings.RECAPTCHA_PRIVATE_KEY,
                request.META.get('REMOTE_ADDR')
            )

            # For reCAPTCHA v2, check the validity
            if not recaptcha_response.is_valid:
                if 'timeout-or-duplicate' in recaptcha_response.error_codes:
                    return 403, {"message": "reCAPTCHA token has expired or duplicated. Please submit the form again later."}
                return 403, {"message": "reCAPTCHA validation failed. Please try again."}

            # For reCAPTCHA v3, checking score
            has_score = hasattr(recaptcha_response, 'extra_data') and 'score' in recaptcha_response.extra_data
            if has_score and recaptcha_response.extra_data.get('score') < settings.RECAPTCHA_REQUIRED_SCORE:
                return 403, {"message": "reCAPTCHA score too low. Please try again later."}

        # Process the form submission
        form_class = form_page.get_form_class()
        form = form_class(data.form_fields)

        # Letting Frontend handling field required logic
        for field in form.fields.values():
            field.required = False

        # Clean the form data
        form.full_clean()

        # Create submission
        form_page.get_submission_class().objects.create(
            form_data=form.cleaned_data,
            page=form_page,
        )

        # Send the email for the EmailFormPage
        if isinstance(form_page, EmailFormPage):
            email_data = {
                'form_title': form_page.title,
                'subject': form_page.subject,
                'from_address': form_page.from_address,
                'to_address': form_page.to_address,
                'content': form.cleaned_data,
            }
            send_form_page_email.delay(email_data)

        return 204, {
            "thanks_page_title": form_page.thanks_page_title,
            "thanks_page_content": form_page.thanks_page_content
        }
    except Exception as e:
        print(f"Error processing form submission: {e}")
        return 500, {"message": "Internal server error while processing form submission"}
