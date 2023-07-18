# Dependencies Installation
pip3 install -r deps.txt

python3 manage.py collectstatic --no-input
# Run Migration 
python3 manage.py migrate
