from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Member, Order

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Member
        fields = ('id', 'user', 'phone', 'points', 'level', 'created_at')

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone')
    
    def create(self, validated_data):
        phone = validated_data.pop('phone')
        user = User.objects.create_user(**validated_data)
        Member.objects.create(user=user, phone=phone)
        return user

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'