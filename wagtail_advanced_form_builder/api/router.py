from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from ninja import NinjaAPI
from ninja.errors import ValidationError
from wagtail_advanced_form_builder.models import FormPage, EmailFormPage
from .schemas import FormPageSchema, EmailFormPageSchema, FormPageUnion, ThanksPageSchema, FormPostSchema, JSONResponse
from .tasks import send_form_page_email

wagtail_advanced_form_builder_api = NinjaAPI(docs_url='/docs', title='Wagtail Advanced Form Builder API')
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
    response={204: ThanksPageSchema, 422: JSONResponse, 403: JSONResponse, 404: JSONResponse, 500: JSONResponse},
    operation_id="post_form_by_path"
)
def form_by_path(request, data: FormPostSchema):
    try:
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

        # Process the form submission
        form_class = form_page.get_form_class()
        form = form_class(data.form_fields)

        # Validation
        if form.is_valid():
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
        else:
            return 422, {"detail": form.errors}
    except PermissionDenied as e:
        return 403, {"message": "CSRF validation failed. Please refresh the page and try again."}
    except Exception as e:
        print(f"Error processing form submission: {e}")
        return 500, {"message": "Internal server error while processing form submission"}



