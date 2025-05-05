from rest_framework.serializers import ModelSerializer
from .models import Bootcamp, BootcampCategory, BootcampRegistration
from rest_framework import serializers
from account.models import CustomUser




class BootcampSerializer(ModelSerializer):
    instructor = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(),
        slug_field='last_name',
        many=True)
    class Meta:
        model = Bootcamp
        fields = "__all__"
        read_only_fields = ['slug']





class CategoryBootcampSerializer(ModelSerializer):
    class Meta:
        model = BootcampCategory
        fields = "__all__"
        read_only_fields = ['slug']


        