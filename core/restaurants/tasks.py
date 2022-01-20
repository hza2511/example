from restaurants.celery import app


@app.task(name='test')
def test():
    print('Test the setup')


@app.task(name='celery_provision_tenant')
def celery_provision_tenant(name, user_email, email=None, description=None, phone_number=None, website=None,
                            street=None, city=None, postal_code=None, host=None, is_staff=False,
                            image=None, country=None):
    """"""
    from restaurants.tenant_tasks import provision_tenant
    from restaurants.models import Restaurant
    from restaurant_info.models import WorkingDay
    from django_tenants.utils import tenant_context
    from collections import namedtuple
    new_tenant_domain, tenant = provision_tenant(name, user_email, email, description, phone_number, website, street,
                                                 city, postal_code, host, is_staff, image, country)
    tenant: Restaurant
    working_day_obj = namedtuple('WorkingDay', 'weekday, name')
    working_days = [
        working_day_obj(1, 'Monday'),
        working_day_obj(2, 'Tuesday'),
        working_day_obj(3, 'Wednesday'),
        working_day_obj(4, 'Thursday'),
        working_day_obj(5, 'Friday'),
        working_day_obj(6, 'Saturday'),
        working_day_obj(7, 'Sunday'),
    ]
    with tenant_context(tenant):
        for working_day in working_days:
            WorkingDay(
                name=working_day.name,
                weekday=working_day.weekday,
                open_24=True    # TODO: TEMPORARY!
                # restaurant=tenant
            ).save()

    tenant.is_created = True
    tenant.save()


@app.task(name='send_verification_mail')
def send_verification_mail(email, host, is_secure):
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import get_template
    from api.views import TokenGenerator
    from restaurants.models import TenantUser
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    from django.conf import settings

    user = TenantUser.objects.get(email=email)
    user.is_active = False
    user.save()
    account_activation_token = TokenGenerator()
    mail_subject = get_template('account_verification/email_subject.html')
    mail_subject = mail_subject.render()
    body_template = get_template('account_verification/email_body.html')
    body_message = body_template.render({
        "token": account_activation_token.make_token(user),
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user,
        "domain": host,
        'protocol': 'https' if is_secure else 'http',
    })
    mail = EmailMultiAlternatives(subject=mail_subject, from_email=settings.DEFAULT_FROM_EMAIL, to=(email,),)
    mail.attach_alternative(body_message, "text/html")
    mail.send()


@app.task(name='send_reset_email')
def send_reset_email(context, email_options, initial_data, domain_override):
    from django.contrib.auth.tokens import default_token_generator
    from rest_framework import serializers
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import get_template
    from django.utils.http import urlsafe_base64_encode
    from django.utils.encoding import force_bytes
    from django.conf import settings
    from django.contrib.auth.forms import PasswordResetForm
    from django.contrib.auth import get_user_model

    reset_form = PasswordResetForm(data=initial_data)
    if not reset_form.is_valid():
        raise serializers.ValidationError(reset_form.errors)
    email = reset_form.cleaned_data["email"]
    site_name = domain = domain_override
    UserModel = get_user_model()
    email_field_name = UserModel.get_email_field_name()

    for user in reset_form.get_users(email):
        user_email = getattr(user, email_field_name)
        context = {
            **email_options,
            'email': user_email,
            'domain': domain,
            'site_name': site_name,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
            'protocol': 'https' if context.get('is_secure') else 'http',
        }

        mail_subject = get_template(email_options.get('subject_template_name'))
        mail_subject = mail_subject.render(context)
        body_template = get_template(email_options.get('html_email_template_name'))
        body_message = body_template.render(context)
        mail = EmailMultiAlternatives(subject=mail_subject, from_email=settings.DEFAULT_FROM_EMAIL, to=(email,),)
        mail.attach_alternative(body_message, "text/html")
        mail.send()
