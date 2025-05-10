from rest_framework.serializers import ModelSerializer
from .models import Bootcamp, BootcampCategory, BootcampRegistration, SMSLog, ClassNotifications
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
    volunteer_name = serializers.SerializerMethodField()
    bootcamp_name = serializers.SerializerMethodField()

    class Meta:
        model = BootcampRegistration
        fields = "__all__"
        read_only_fields = ["reviewed_by", "volunteer", "reviewed_at", "status", "slug"] 

    def get_volunteer_name(self, obj):
        return obj.volunteer.get_full_name()

    def get_bootcamp_name(self, obj):
        return obj.bootcamp.title

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['volunteer'] = instance.volunteer.get_full_name()
        representation['bootcamp'] = instance.bootcamp.title
        return representation






class BootcampCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BootcampCategory
        fields = ['slug', 'name', 'date_created', 'url']
        extra_kwargs = {
            'url': {'view_name': 'bootcampcategory-detail', 'lookup_field': 'slug'}
        }





class BootcampRegistrationCreateSerializer(serializers.ModelSerializer):
    volunteer = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = BootcampRegistration
        fields = [
            'volunteer', 'bootcamp', 'payment_type', 'installment_count',
            'comment', 'phone_number', 'slug'
        ]

    def create(self, validated_data):
        volunteer = validated_data['volunteer']
        bootcamp = validated_data['bootcamp']

        
        existing_registration = BootcampRegistration.objects.filter(
            volunteer=volunteer,
            status='approved'
        ).exclude(bootcamp=bootcamp).first()

        if existing_registration:
            
            for field, value in validated_data.items():
                setattr(existing_registration, field, value)
            existing_registration.save()
            return existing_registration
        return super().create(validated_data)
  





class AdminBootcampRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BootcampRegistration
        fields = ["status", "admin_status_comment"]

    def to_internal_value(self, data):
        allowed_keys = {'status', 'admin_status_comment'}
        extra_keys = set(data.keys()) - allowed_keys

        if extra_keys:
            raise serializers.ValidationError(
                f"You are only allowed to update: {', '.join(allowed_keys)}. Extra fields: {', '.join(extra_keys)}"
            )
        return super().to_internal_value(data)
            








class BootcampStudentSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = BootcampRegistration
        fields = ['full_name', 'phone_number', 'status', 'registered_at', 'payment_type']

    def get_full_name(self, obj):
        return obj.volunteer.get_full_name()
    







class MassNotificationSerializer(serializers.Serializer):
    bootcamp_title = serializers.CharField()
    title = serializers.CharField(max_length=100)
    admin_message = serializers.CharField()

    def validate(self, data):
        try:
            bootcamp = Bootcamp.objects.get(title=data['bootcamp_title'])
        except Bootcamp.DoesNotExist:
            raise serializers.ValidationError({'bootcamp_title': 'Bootcamp not found.'})
        data['bootcamp'] = bootcamp
        return data
    
    def create(self, validated_data):
        bootcamp = validated_data['bootcamp']
        title = validated_data['title']
        admin_message = validated_data['admin_message']

        registrations = BootcampRegistration.objects.filter(bootcamp=bootcamp)

        notifications = []
        from .tasks import send_sms_notification

        for reg in registrations:
            notif = ClassNotifications.objects.create(
                title=title,
                bootcampRegistration=reg,
                admin_message=admin_message,
                status='pending'
            )
            notifications.append(notif)
            send_sms_notification.delay(notif.id)

        return notifications    








class SMSLogSerializer(ModelSerializer):
    class Meta:
        model = SMSLog
        fields = "__all__"
