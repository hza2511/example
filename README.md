# Chowtime
***

## Init the project
### 1. Migrations
```shell
python manage.py makemigrations
python manage.py migrate
```
### 2. Basic schema
```shell
python manage.py shell
```
```python
from restaurants.models import Restaurant, Domain
# create your public tenant
tenant = Restaurant(schema_name='public', name='Basic Schema.')
tenant.save()
# Add one or more domains for the tenant
domain = Domain()
domain.domain = 'localhost' # don't add your port or www here! on a local server you'll want to use localhost here
domain.tenant = tenant
domain.is_primary = True
domain.save()
```