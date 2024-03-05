from django.db import models

class Subscribers(models.Model):
    email = models.EmailField(unique = True, blank = False)