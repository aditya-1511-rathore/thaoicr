from django.db import models

class OCRResult(models.Model):
    image = models.ImageField(upload_to='ocr_images/')
    text = models.TextField()
    id_number = models.CharField(max_length = 100, blank = True, null = True)
    name = models.CharField(max_length = 100, blank = True, null = True)
    last_name = models.CharField(max_length = 100, blank = True, null = True)
    date_of_birth = models.CharField(max_length = 100, blank = True, null = True)
    date_of_issue = models.CharField(max_length = 100, blank = True, null = True)
    date_of_expiry = models.CharField(max_length = 100, blank = True, null = True)
    success = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'OCR Result for {self.image} ({self.created_at})'