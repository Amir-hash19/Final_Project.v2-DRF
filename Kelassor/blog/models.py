from django.db import models
from account.models import CustomUser




class CategoryBlog(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    




class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    uploaded_by = models.ForeignKey(to=CustomUser, on_delete=models.SET_NULL, null=True)
    slug = models.SlugField(unique=True)


    STATUS_CHOICES = (    
        ("draft", "Draft"),
        ("published", "Published")
    )    

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    blogcategory = models.ForeignKey(to=CategoryBlog, on_delete=models.CASCADE, null=True, blank=True)
    file = models.FileField(upload_to='articles/', null=True, blank=True)


    def __str__(self):
        return self.title