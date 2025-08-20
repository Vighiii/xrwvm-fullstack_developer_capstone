from django.db import models
from django.utils.timezone import now

# Define your models from here:

# class User(models.Model):
#     first_name = models.CharField(null=False,max_length=30, default='jitendra')
#     last_name = models.CharField(null=False,max_length=30, default='kumar')
#     dob = models.DateField(null=True)
    
#     def __str__(self):
#         return self.first_name + " " + \
#                self.last_name
# class Instructor(models.Model):
#     full_time = models.BooleanField(default=True)
#     total_learners = models.IntegerField()
#     def __str__(self):
#         return "First name :" +self.first_name + " ," + \
#                "Last name :" +self.last_name+ " ," + \
#                "Is full time :"+ str(self.full)
