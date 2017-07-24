from rest_framework import serializers
from authsystem.models import MyUser

__author__ = 'hamid'


class MyUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = MyUser.objects.create_user(**validated_data)
        return user

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'password')
