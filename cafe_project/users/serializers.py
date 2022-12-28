from rest_framework import serializers
from.models import User
from django.utils.timezone import datetime


class UserSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'username', 'description', 'avatar')
        extra_kwargs = {'password1': {'write_only': True}}


class RegistrationSerializer(serializers.ModelSerializer):

    date_joined = serializers.ReadOnlyField()
    password1 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta(object):
        model = User
        fields = ('email', 'date_joined', 'password1', 'password2', 'username', 'avatar')
        extra_kwargs = {'password1': {'write_only': True}}

    def save(self):
        user = User(
            email=self.validated_data['email'].lower(),
            username=self.validated_data['username'],
            date_joined=datetime.today(),
        )
        password1 = self.validated_data['password1']
        password2 = self.validated_data['password2']
        if password1 != password2:
            raise serializers.ValidationError({'password': 'Пароли должны совпадать.'})
        user.set_password(password1)
        user.save()
        return user


class UploadAvatarSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(source="avatar", required=True)

    class Meta(object):
        model = User
        fields = ['image']
