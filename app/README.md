#  Real World App

Implementation of real world application: https://github.com/gothinkster/realworld/ using Django and Unpoly.

## Installation:

To install and run locally:

- Clone the project:

  ```bash
  git clone https://github.com/alnuaimi94/realworld
  ```

- Change directory & Create virtualenv called **env**:
  ```bash
  cd realworld
  ```
  ```bash
  python3 -m venv env
  ```

- Activate virtualenv:
  - for Windows System:
    ```bash
      env/Scripts/activate
    ```
  - for Linux System:
    ```bash
      source ./env/bin/activate
    ```

- Install dependencies:
  ```bash
  pip install -r requirements/local.txt
  ```

- Change DJANGO_SETTINGS_MODULE from *production* to *local* in [manage.py](./manage.py), [asgi.py](./realworld/config/asgi.py) and [wsgi.py](./realworld/config/wsgi.py) files.
  ```python
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realworld.config.settings.local')
  ```

- Migrate & Runserver:
  ```bash
  python manage.py migrate
  ```
  ```bash
  python manage.py runserver
  ```

- Finally open the localhost in the browser:
  ```bash
    http://127.0.0.1:8000/
  ```
