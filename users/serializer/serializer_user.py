import logging
from users.models import User
from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        # Authenticate user based on phone number and password
        user = authenticate(phone_number=phone_number, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid phone number or password.")
        
        # If authentication is successful, return the user object
        data['user'] = user
        return data

    def create(self, validated_data):
        # Generate JWT tokens for the user
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'username', 'password', 'membership_type']
        extra_kwargs = {
            'phone_number': {'required': True, 'error_messages': {'required': 'Phone number is required.'}},
            'password': {'required': True, 'error_messages': {'required': 'Password is required.'}},
            'membership_type': {'required': True, 'error_messages': {'required': 'Member Type is required.'}},
            'username': {'allow_blank': True, 'allow_null': True},
        }
    
    def validate_membership_type(self, value):
        logger.debug(f"Received membership_type: {value}")
        
        # Check for membership type choice is valid
        if value not in ['Silver', 'Gold', 'Diamond']:
            raise serializers.ValidationError(f"{value} is not a valid choice.")
        return value
        
    def validate_phone_number(self, value):
        # Check if phone number length is greater than 10
        if len(value) > 10:
            raise serializers.ValidationError('Phone number must not greater than 10 characters.')
        
        # Check if phone number is already Registration
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('This Phone number is already Registration.')
        
        return value
