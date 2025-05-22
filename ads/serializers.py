from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Ad, Category, ExchangeProposal

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class AdSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )

    class Meta:
        model = Ad
        fields = ['id', 'title', 'description', 'category', 'category_id',
                 'condition', 'image', 'user', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class ExchangeProposalSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_ad = AdSerializer(read_only=True)

    class Meta:
        model = ExchangeProposal
        fields = ['id', 'from_user', 'to_ad', 'message', 'status',
                 'created_at', 'updated_at']
        read_only_fields = ['from_user', 'to_ad', 'status', 'created_at', 'updated_at'] 