from django.db import models

class StackAPI(models.Model):
	ip = models.CharField(max_length=100)
	count = models.IntegerField()
	date = models.DateTimeField()
