from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import CustomUser

User = get_user_model()



class CreateAccountSerializer(serializers.ModelSerializer):
    group = serializers.CharField(write_only=True, required=False)
    
   
    class Meta:
        model = CustomUser
        fields = [
            "username", "first_name", "last_name", "phone", "email",
            "about_me", "national_id", "gender","group","password"
        ]
        read_only_fields = ['group']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["phone"] = str(instance.phone) 
        return data

    def create(self, validated_data):
        group_name = validated_data.pop('group', None)

        user = CustomUser.objects.create(**validated_data)

        if group_name:
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
            except Group.DoesNotExist:
                raise serializers.ValidationError(f"Group '{group_name}' does not exist.")

        user.save()
        return user




class EditAccountSerializer(ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(), many=True, required=False, write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "phone", "email",
                  "about_me", "national_id", "gender", "password", "groups"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        if not user.is_authenticated or not user.groups.filter(name__in=["superuser", "supportpanel"]).exists():
            self.fields.pop('groups', None)
