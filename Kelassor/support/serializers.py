from rest_framework.serializers import ModelSerializer
from .models import Ticket, TicketMessage
from rest_framework import serializers
from bootcamp.models import Bootcamp
from account.models import CustomUser
from django.utils.text import slugify
from django.db import transaction
import uuid



class TicketSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'bootcamp', 'status', 'slug', 'user']
        read_only_fields = ['status', 'slug', 'user'] 

    def create(self, validated_data):
        with transaction.atomic():
            user = self.context['request'].user
            title = validated_data.get('title', '')
            slug = slugify(title) + "-" + str(uuid.uuid4())[:8]  # یکتا و خوانا
            validated_data['slug'] = slug
            ticket = Ticket.objects.create(user=user, **validated_data)
            return ticket





class TicketCreateSerializer(serializers.HyperlinkedModelSerializer):
    bootcamp = serializers.HyperlinkedRelatedField(
        queryset=Bootcamp.objects.all(),
        view_name='bootcamp-detail',  
        required=False,
        allow_null=True
    )

    class Meta:
        model = Ticket
        fields = ['url', 'title', 'description', 'bootcamp', 'slug']
        extra_kwargs = {
            'url': {'view_name': 'ticket-detail'},  
        }

    def create(self, validated_data):
        user = self.context['request'].user
        return Ticket.objects.create(user=user, **validated_data)
    







class TicketMessageSerializer(ModelSerializer):
    ticket = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = TicketMessage
        fields = "__all__"
        read_only_fields = ["sender", "slug", "admin_response", "admin"]

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['sender'] = user

        title = validated_data.get('title') or "message"
        slug = slugify(title) + "-" + str(uuid.uuid4())[:8]
        validated_data['slug'] = slug

        return super().create(validated_data)





# class TicketMessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TicketMessage
#         fields = "__all__"
#         read_only_fields = ["sebder", "slug", "admin"]


#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         user = self.context['request'].user


#         if not (user and user.is_authenticated and user.groups.filter(name__in=["SupportPanel", "SuperUser"]).exists()):
#             self.fields.pop('admin', None)
#             self.fields.pop('admin_response', None)






class AdminTicketMessageResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = ["admin", "admin_response"]
        read_only_fields = []
