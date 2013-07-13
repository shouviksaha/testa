from django.db import models
from django.contrib.auth.models import User
from reg.models import userInfo
import testa.settings


class client(models.Model):
	userinfo = models.ForeignKey(userInfo)
	details = models.TextField()
	
	
class student(models.Model):
	userinfo = models.ForeignKey(userInfo)
	college = models.CharField(max_length = 250)
	department_choices = (
                ('IT', 'IT'),
                ('CSE', 'CSE'),
                ('MCA', 'MCA'),
                ('BT', 'BT'),
                ('CE', 'CE'),
                ('CHE', 'CHE'),
                ('ECE', 'ECE'),
                ('EE', 'EE'),
                ('ME', 'ME'),
                ('MME', 'MME'),
                ('Other', 'Other'),
            )
	department = models.CharField(max_length=250,choices=department_choices)
	year_choices = (
					 ('2014', '2014'),
                ('2015', '2015'),                
                ('2016', '2016'),
        )
	year = models.CharField(max_length=10,choices=year_choices)
	phone = models.CharField(max_length = 11)