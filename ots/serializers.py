from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from ots.models import Session, Participation, Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     required=True,
                                     style={'input_type': 'password', 'placeholder': 'Password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'id']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    # Serializer authentication object
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        # Validate and authenticate the user

        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('context'),
            username=username,
            password=password
        )
        if not user:
            message = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(message, code='authentication')
        attrs['user'] = user
        return attrs


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['name', 'start_date', 'host', 'id', 'url']

    def create(self, validated_data):
        start_date = validated_data['start_date']
        name = validated_data['name']
        host = validated_data['host']
        url = validated_data['url']
        session = Session.objects.create(start_date=start_date, name=name, host=host, url=url)
        session.save()
        return session


class ParticipationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participation
        fields = ['user', 'fullname', 'session', 'start_date', 'end_date', 'role']

    def create(self, validated_data):
        user = validated_data['user']
        session_id = validated_data['session']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']
        role = validated_data['role']
        fullname = validated_data['fullname']
        participation = Participation.objects.create(user=user, session=session_id, start_date=start_date,
                                                     end_date=end_date,
                                                     role=role,
                                                     fullname=fullname)
        participation.save()
        return participation


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'fullname', 'session', 'content']

    def create(self, validated_data):
        message = Message.objects.create(sender=validated_data['sender'], session=validated_data['session'],
                                         content=validated_data['content'], fullname=validated_data['fullname'])
        message.save()
        return message
