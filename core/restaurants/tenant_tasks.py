import random
import string
import time
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import InMemoryUploadedFile
from tenant_users.compat import (get_tenant_model, TENANT_SCHEMAS, get_public_schema_name,
                                 get_tenant_domain_model, schema_context)
from tenant_users.tenants.models import InactiveError, ExistsError
from rest_framework import serializers
from restaurants.serializers import DomainSerializer
from api.serializers import BinaryImageSerializer
from restaurants.models import Restaurant, Domain   # Country


def provision_tenant(name, user_email, email=None, description=None, phone_number=None, website=None, street=None, city=None,
                     postal_code=None, host=None, is_staff=False, image=None, country=None):
    """
    Override method tenant_users.tenants.tasks.provision_tenant()
    Create a tenant with default roles and permissions

    Returns:
        Restaurant, Domain
    The FQDN for the tenant.
    Changed:
        1. Should be provided with origin tenant name --> set as tenant.name field.
        2. slug_name is calculated inside.
        3. domain is calculated inside.
        4. Optional: provide an image --> set as tenant.image field.
        4. Optional: provide a country --> set as tenant.country field.
    """
    extra_data = {
        "description": description,
        "email": email,
        "phone_number": phone_number,
        "website": website,
        "street": street,
        "city": city,
        "postal_code": postal_code,
        "country": country
    }
    tenant = None

    UserModel = get_user_model()
    TenantModel = get_tenant_model()

    user = UserModel.objects.get(email=user_email)
    if not user.is_active:
        raise InactiveError("Inactive user passed to provision tenant")
    tenant_domain = None
    for _ in range(11):
        domain = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(6))
        domain_serializer = DomainSerializer(data={'domain': domain}, context={'host': host})
        if domain_serializer.is_valid():
            tenant_domain = domain_serializer.validated_data['domain']
            break
    if not tenant_domain:
        raise serializers.ValidationError({'details': "Could not find available domain name for this restaurant name"})

    tenant_slug = name.replace(' ', '').replace('-', '').lower()

    if TENANT_SCHEMAS:
        if TenantModel.objects.filter(domain_url=tenant_domain).first():
            raise ExistsError("Tenant URL already exists")
    else:
        if get_tenant_domain_model().objects.filter(domain=tenant_domain).first():
            raise ExistsError("Tenant URL already exists.")

    time_string = str(int(time.time()))
    # Must be valid postgres schema characters see:
    # https://www.postgresql.org/docs/9.2/static/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS
    # We generate unique schema names each time so we can keep tenants around without
    # taking up url/schema namespace.
    schema_name = '{}_{}'.format(domain, time_string)
    domain = None

    # Get Country by name or None
    # try:
    #     country = Country.objects.get(name=country) if country else None
    # except Country.DoesNotExist:
    #     raise serializers.ValidationError({'country': 'Country matching query does not exist'})
    # noinspection PyBroadException
    try:
        # Wrap it in public schema context so schema consistency is maintained
        # if any error occurs
        with schema_context(get_public_schema_name()):
            if TENANT_SCHEMAS:
                # Create a TenantModel object and tenant schema
                tenant = TenantModel.objects.create(
                    name=name,
                    slug=tenant_slug,
                    domain_url=tenant_domain,
                    schema_name=schema_name,
                    owner=user,
                    **extra_data)#, country=country)

            else:  # django-tenants
                tenant = TenantModel.objects.create(name=name,
                                                    slug=tenant_slug,
                                                    schema_name=schema_name,
                                                    owner=user,
                                                    **extra_data)#, country=country)

                # Add one or more domains for the tenant
                domain = get_tenant_domain_model().objects.create(domain=tenant_domain,
                                                                  tenant=tenant,
                                                                  is_primary=True)
            # Add user as a superuser inside the tenant
            tenant.add_user(user, is_superuser=True, is_staff=is_staff)
            if isinstance(image, InMemoryUploadedFile):
                with schema_context(schema_name):
                    image_serializer = BinaryImageSerializer(data={'image': image})
                    if image_serializer.is_valid():
                        image = image_serializer.validated_data['image']
                        tenant.image = image
                        tenant.save()

    except:
        if domain is not None:
            domain.delete()
        if tenant is not None:
            # Flag is set to auto-drop the schema for the tenant
            tenant.delete(True)
        raise

    return tenant_domain, tenant
