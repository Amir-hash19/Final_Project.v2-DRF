from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Blog, CategoryBlog





class BlogCategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryBlog
        fields = "__all__"




class UploadBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'slug', 'blogcategory', 'uploaded_by']
        read_only_fields = ['uploaded_by'] 

        