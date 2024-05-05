
from rest_framework import serializers

from main.models import *


class ModAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModAdmin
        fields =["id_user", "full_name", "describe", "role", "mssv", "class_school", "image"]

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = '__all__'

class PaperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paper
        fields = '__all__'