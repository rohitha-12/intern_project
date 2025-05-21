from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone_number', 'company_name', 'company_website', 'country', 'linkedin_url', 'username']