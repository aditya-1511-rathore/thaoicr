# THAI ID CARD OCR RECOGNIZATION AND HANDLING


## How to Install
1. Install Tesseract from [Tesseract](https://github.com/tesseract-ocr/tesseract#installing-tesseract)
2. Update the Tesseract to the path variable
3. Install required libraries by ```pip install -r requirements.txt```
4. On bash, write following commands (must be in the same directory)
```console
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

the server will be started on http://127.0.0.1:8000