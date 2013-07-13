from django.db import models
from django.contrib.auth.models import User

class userInfo(models.Model):
	user = models.ForeignKey(User)
	activation_string = models.CharField(max_length=100,blank=True)
	forgot_password_string = models.CharField(max_length=100,blank=True)
	name = models.CharField(max_length=200)


	def __unicode__(self):
		return self.name
