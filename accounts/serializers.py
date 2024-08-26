from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    # user_type = serializers.CharField(write_only=True)

    # group =serializers.CharField()

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('password not match')
        return super().validate(data)
    
    
    def create(self, validated_data):        
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']

        user = self.Meta.model.objects.create_user(**data)

        user.save()

        return user
    
    class Meta:
        model = get_user_model()

        fields= (
            'id', 'email', 'password1', 'password2', 'first_name',
            'last_name',
        )
        read_only_fields = ('id', 'password1', 'password2',)


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        user_data = UserSerializer(user).data
        for key, value in user_data.items():
            if key != 'id':
                token[key] = value
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add your extra responses here
        # data['email'] = self.user.email
        # data['name'] = '{self.user.first_name} {self.user.last_name}'
        # data['id'] = self.user.id

        # data['groups'] = self.user.groups.values_list('name', flat=True)
        return data

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        read_only_fields = ('id', 'email',)

    def update(self, instance, validated_data):
        # Exclude password fields from validated data
        validated_data.pop('password1', None)
        validated_data.pop('password2', None)
        
        # Perform the usual update logic
        instance = super().update(instance, validated_data)
        return instance