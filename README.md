# Окружение

#### активировать окружение -
```source back-olimp-env/bin/activate```

#### отключить окружение - deactivate

# Django
```python manage.py runserver```

UPDATE "olimApp_customuser"
SET is_active = false, activation_code = 'a54e4823-b09d-4731-977d-7527c0134a32'
WHERE id = 38;