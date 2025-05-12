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





class TicketMessageCreateSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer(read_only=True)

    class Meta:
        model = TicketMessage
        fields = ["sender", "message", "ticket", "title", "attachment", "created_at", "slug"]






class TicketMessageSerializer(ModelSerializer):
    ticket = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    admin = serializers.StringRelatedField(read_only=True)
    sender = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TicketMessage
        fields = "__all__"
        read_only_fields = ["sender", "slug", "admin_response", "admin", "message_status"]






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





class AdminEditableTicketMessageSerializer(serializers.ModelSerializer):
    admin = serializers.StringRelatedField(read_only=True)
    sender = serializers.StringRelatedField(read_only=True)
    ticket = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = TicketMessage
        fields = [
            'id',
            'ticket',
            'sender',
            'message',
            'attachment',
            'created_at',
            'title',
            'slug',
            'admin',
            'admin_response',
            'message_status'
        ]
        read_only_fields = [
            'id',
            'ticket',
            'sender',
            'message',
            'attachment',
            'created_at',
            'title',
            'slug',
            'admin',  # فقط نمایش داده می‌شه، ولی ست میشه از request.user
        ]



    def update(self, instance, validated_data):
        validated_data['admin'] = self.context['request'].user
        return super().update(instance, validated_data)