from rest_framework.serializers import ModelSerializer
from .models import Bootcamp, BootcampCategory, BootcampRegistration
from rest_framework import serializers
from account.models import CustomUser




class BootcampSerializer(serializers.HyperlinkedModelSerializer):
    instructor = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(),
        slug_field='last_name',
        many=True)
    category = serializers.HyperlinkedRelatedField(
        queryset=BootcampCategory.objects.all(),
        view_name='bootcampcategory-detail',
        lookup_field='slug' 
    )
    class Meta:
        model = Bootcamp
        fields = ["instructor", "title", "price", "capacity", "category", 
                "description", "start_date", "end_date", "created_at", "hours", "days", "slug", "url"]
        read_only_fields = ['slug', 'status']
        extra_kwargs = { 'url': {'view_name': 'bootcamp-detail', 'lookup_field': 'slug'}}





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



class BootcampCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BootcampCategory
        fields = ['slug', 'name', 'date_created', 'url']
        extra_kwargs = {
            'url': {'view_name': 'bootcampcategory-detail', 'lookup_field': 'slug'}
        }





class BootcampRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BootcampRegistration
        fields = '__all__'
        read_only_fields = ['volunteer', 'status', 'registered_at', 'reviewed_at', 'reviewed_by', 'admin_status_comment', 'slug']
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

                    
        previous = BootcampRegistration.objects.filter(
            volunteer=user,
            status='approved'
        ).order_by('-registered_at').first()

        if previous:
        # انتقال همه‌ی اطلاعات قابل کپی
            validated_data['phone_number'] = previous.phone_number
            validated_data['payment_type'] = previous.payment_type
            validated_data['installment_count'] = previous.installment_count
            validated_data['slug'] = f"{validated_data['bootcamp'].slug}-{user.id}"

        validated_data['volunteer'] = user
        return super().create(validated_data)

  



class BootCampRegistraionSerializer(ModelSerializer):
    class Meta:
        model = BootcampRegistration
        fields = "__all__"
        read_only_fields = ["volunteer", "reviewed_by", "reviewed_at", "phone_number", "comment", "bootcamp", "payment_type", "slug"]

    def update(self, instance, validated_data):
        status = validated_data.get('status', instance.status)
        if status:
            instance.status = status

        comment = validated_data.get('admin_status_comment', instance.admin_status_comment)    
        if comment:
            instance.admin_status_comment = comment

        instance.save()
        return instance    