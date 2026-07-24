from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'role', 'store', 'store_name', 'phone', 'branch_id']
        read_only_fields = ['role', 'store']


class StaffCreateSerializer(serializers.ModelSerializer):
    """Owner/Manager uses this to create staff (cashier, inventory staff, etc.)
    within their OWN store — store is stamped by the view, never sent by the client."""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'phone', 'branch_id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user