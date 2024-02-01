# import email
from pickle import TRUE
from django.db import models

from django.db import models

class Blogs(models.Model):
    blog_id=models.AutoField(auto_created=True,primary_key=True)
    blog_name=models.CharField(max_length=200)
    blog_details=models.CharField(max_length=200)
    blog_image=models.FileField(upload_to='blog_image')

    class Meta:
        db_table="blog"
