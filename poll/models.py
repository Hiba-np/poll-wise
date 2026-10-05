from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class  CustomeUser(AbstractUser):
    phone=models.IntegerField(null=True)

class poll(models.Model):
    question=models.CharField(max_length=250)
    owner=models.ForeignKey(CustomeUser,on_delete=models.CASCADE,related_name="poll")
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.question

class choice(models.Model):
    options=models.CharField(max_length=250)
    poll_object=models.ForeignKey(poll,on_delete=models.CASCADE,related_name="choice")

    def __str__(self):
        return self.options

class voting(models.Model):
    owner_object=models.ForeignKey(CustomeUser,on_delete=models.CASCADE,related_name="votes")
    poll_object=models.ForeignKey(poll,on_delete=models.CASCADE,related_name="votes")
    choice_object=models.ForeignKey(choice,on_delete=models.CASCADE,related_name="votes")
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('poll_object','owner_object')