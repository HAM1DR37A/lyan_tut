from django.utils.datetime_safe import strftime
from rest_framework import serializers
from authsystem.models import MyUser
from messaging.models import Message, Group

__author__ = 'hamid'

class MessageSerializer(serializers.ModelSerializer):

    # text = serializers.CharField(max_length=300)
    # author = serializers.CharField()
    # date = serializers.SerializerMethodField()
    # group = serializers.CharField()

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)
        return message

    class Meta:
        model = Message
        fields = ('text', 'group', 'date', 'author')

    # def get_text(self, obj):
    #     return obj.get_text()
    #
    # def get_date(self, obj):
    #     return obj.date.strftime("%H:%M")
    #
    # def get_author(self, obj):
    #     return obj.author.username
class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('name', 'image', )

