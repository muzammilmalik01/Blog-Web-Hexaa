from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=50, unique = True)
    
    def __str__(self) -> str:
        return self.title