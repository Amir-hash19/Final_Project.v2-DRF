from rest_framework.serializers import ModelSerializer
from models import Ticket, TicketMessage
from rest_framework import serializers



class TickectSerializer(ModelSerializer):
    model = Ticket
    fields = "__all__"
    read_only_fields = ["user", "slug"]
    