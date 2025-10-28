python -m venv .venv

.venv\Scripts\activate   #Windows

source .venv/bin/activate  #Mac

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

![img_1.png](img_1.png)
