from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, mixins, authentication, permissions, status
from rest_framework.settings import api_settings
from ots.serializers import UserSerializer, SessionSerializer, ParticipationSerializer, MessageSerializer, \
    AuthTokenSerializer
from ots.models import User, Session, Participation, Message
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from rest_framework import authentication


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        _id = kwargs['pk']
        user = User.objects.get(id=_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class CreateTokenView(ObtainAuthToken):
    # Create a new auth token for user
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    # Manage the authenticated user
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication, authentication.BasicAuthentication)
    permission_classes = (permissions.IsAuthenticated,)

    # def get(self, request, *args, **kwargs):
    #     print()
    #

    def get_object(self):
        return self.request.user


class SessionView(ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        url = kwargs['pk']
        try:
            session = Session.objects.get(url=url)
            serializer = SessionSerializer(session)
            return Response(serializer.data)
        except Session.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ParticipationView(ModelViewSet):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer

    def retrieve(self, request, *args, **kwargs):
        user_id = kwargs['pk']
        try:
            participation = Participation.objects.filter(user=user_id)
            serializer = ParticipationSerializer(participation, many=True)
            return Response(serializer.data)
        except Participation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        user_id = kwargs['pk']

        try:
            participation = Participation.objects.filter(user=user_id)
            self.perform_destroy(participation)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Participation.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class MessageView(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def retrieve(self, request, *args, **kwargs):
        session_id = kwargs['pk']
        try:
            messages = Message.objects.filter(session=session_id)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        session_id = kwargs['pk']
        try:
            messages = Message.objects.filter(session=session_id)
            self.perform_destroy(messages)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Message.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
