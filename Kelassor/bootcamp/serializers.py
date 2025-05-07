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
        fields = ["instructor", "title", "instructor", "price", "capacity", "category", 
                "description", "start_date", "end_date", "created_at", "hours", "days", "slug"]
        read_only_fields = ['slug', 'status']





class CategoryBootcampSerializer(ModelSerializer):
    class Meta:
        model = BootcampCategory
        fields = "__all__"
        read_only_fields = ['slug']





class BootcampCountSerializer(serializers.ModelSerializer):
    request_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Bootcamp
        fields = ['title', 'is_online', 'request_count'] 





class BootCampRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    bootcamp = serializers.HyperlinkedRelatedField(
        view_name = 'bootcamp-detail',
        queryset = Bootcamp.objects.filter(status='registering')
    )
    class Meta:
        model = BootcampRegistration
        fields = [
            'url',
            'id',
            'bootcamp',
            'payment_type',
            'installment_count',
            'registered_at',
            'status',
            'comment',
            'phone_number',]
        
       
        
class BootCampRegitrationSerializer(ModelSerializer):
    class Meta:
        model = BootcampRegistration
        fields = "__all__"
        read_only_fields = ["reviewed_by", "volunteer"] 