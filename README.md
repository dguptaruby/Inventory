## Setup
Create environment

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Setup DB

```
DATABASES  = {
	'default': {
	'ENGINE': 'django.db.backends.postgresql_psycopg2',
	'NAME': 'DBNAME',
	'USER': 'USERNAME',
	'PASSWORD': 'PASSWORD',
	'HOST': 'localhost',
	'PORT': '5432'
	}
}
```
Migrations
```
python manage.py migrate
```
Create user
```
python manage.py createsuperuser
```
Create token
```
python manage.py drf_create_token admin
```
## Run
```
python manage.py runserver
```
Create Entries

http://127.0.0.1:8000/admin/

## Fetch Data

Stores:
```
curl --location --request GET 'http://127.0.0.1:8000/stores/' -header 'Authorization: token a0095e38f280a9141b6841cb11ac18efee90e0d2'
```
```
{"status":"success","data":[{"id":1,"title":"XYZ","address":"dfgdfg","company_id":1,"manager_id":1,"user_id":1,"username":"admin","products":"sdfsd"}]}
```

Products
```
curl --location --request GET 'http://127.0.0.1:8000/products/' --header 'Authorization: token a0095e38f280a9141b6841cb11ac18efee90e0d2'
```
```
{"status":"success","data":[{"id":1,"barcode":"1232sdfsd","title":"sdfsd","description":"sdfsdf","price":1231.33,"quantity":12323.0,"date_added":"2022-03-09T06:00:12.751378Z","last_updated":"2022-03-09T06:00:12.751402Z","company_id":1,"comapny_name":"XYZ","manager_id":1,"user_id":1}]}
```

Products Analytics
```
curl --location --request GET 'http://127.0.0.1:8000/analytics/products/' --header 'Authorization: token a0095e38f280a9141b6841cb11ac18efee90e0d2'
```
```
{"status":"success","data":[{"id":1,"barcode":"1232sdfsd","title":"sdfsd","description":"sdfsdf","price":1231.33,"quantity":12323.0,"date_added":"2022-03-09T06:00:12.751378Z","last_updated":"2022-03-09T06:00:12.751402Z","company_id":1,"comapny_name":"XYZ","manager_id":1,"user_id":1}]}
```
Stores Analytics
```
curl --location --request GET 'http://127.0.0.1:8000/analytics/stores/' --header 'Authorization: token a0095e38f280a9141b6841cb11ac18efee90e0d2'
```
```
{"status":"success","data":[{"id":1,"title":"XYZ","address":"dfgdfg","company_id":1,"manager_id":1,"user_id":1,"username":"admin","products":"sdfsd"}]}
```