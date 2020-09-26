from django.db import models

# Create your models here.
class Heritage(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=255)
    # it comes 위치_도 + 위치_시
    location = models.CharField(max_length=255)
    dynasty = models.CharField(max_length=255)
    img_url = models.TextField()
    content = models.TextField()
    # 경도
    longitude = models.TextField()
    # 위도
    latitude = models.TextField()
