from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from django.contrib.postgres.fields.jsonb import JSONField

class Event(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.IntegerField(choices = [(i,i) for i in range(1,11)])
    name = models.CharField(max_length=30)
    event_type = models.CharField(max_length=50,default="actividad_fija") #Choices: actividad_fija, no fija y horario suenio.
    constraints = models.JSONField(default = dict)




class Position(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    day = models.IntegerField(MaxValueValidator(7))
    hour = models.IntegerField(MaxValueValidator(24))








