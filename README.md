#Python project

cd YOUR_PROJECT_DIRECTORY_PATH/

virtualenv --no-site-packages env

source env/bin/activate

pip install -r requirements.txt

export FLASK_APP=app

export FLASK_ENV=development # enables debug mode

python3 app.py

