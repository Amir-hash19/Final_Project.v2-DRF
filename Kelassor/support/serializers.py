from rest_framework.serializers import ModelSerializer
from models import Ticket, TicketMessage
from rest_framework import serializers
from bootcamp.models import Bootcamp
from account.models import CustomUser


class TickectSerializer(ModelSerializer):
    model = Ticket
    fields = "__all__"
    read_only_fields = ["user", "slug"]




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
    



class TicketSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name='user-detail', queryset=CustomUser.objects.all())
    bootcamp = serializers.HyperlinkedRelatedField(view_name='bootcamp-detail', queryset=Bootcamp.objects.all(), required=False)

    class Meta:
        model = Ticket
        fields = ['url', 'title', 'description', 'user', 'bootcamp', 'created_at', 'status', 'slug']





class TicketMessageSerializer(ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = "__all__"
        read_only_fields = ["sender", "slug", "ticket"]






class TicketMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = "__all__"
        read_only_fields = ["sebder", "slug", "admin"]


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user


        if not (user and user.is_authenticated and user.groups.filter(name__in=["SupportPanel", "SuperUser"]).exists()):
            self.fields.pop('admin', None)
            self.fields.pop('admin_response', None)






class AdminTicketMessageResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketMessage
        fields = ["admin", "admin_response"]
        read_only_fields = []
        