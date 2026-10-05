from django.shortcuts import render
from rest_framework.generics import CreateAPIView,ListAPIView,ListCreateAPIView,RetrieveAPIView,DestroyAPIView
from rest_framework.response import Response
from poll.models import CustomeUser,poll,choice,voting
from poll.serializers import UserSerializer,PollSerializer,ChoiceSerializer,VotingSerializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
# Create your views here.

class UserCreateView(CreateAPIView):
    serializer_class=UserSerializer

class pollView(CreateAPIView,ListAPIView):
    serializer_class=PollSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=poll.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

class PollListView(ListAPIView):
    serializer_class=PollSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=poll.objects.all()

class PollRetrieveView(RetrieveAPIView):
    serializer_class=PollSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=poll.objects.all()

class PollDestroyView(DestroyAPIView):
    serializer_class=PollSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=poll.objects.all()

class ChoiceView(CreateAPIView):
    serializer_class=ChoiceSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        poll_id=self.kwargs.get('pk')
        poll_obj=poll.objects.get(id=poll_id)
        return serializer.save(poll_object=poll_obj)

class VotingView(CreateAPIView):
    authentication_classes=[TokenAuthentication]
    serializer_class=VotingSerializer
    permission_classes=[IsAuthenticated]
    def perform_create(self, serializer):
        pid=self.kwargs.get('pk')
        poll_object=poll.objects.get(id=pid)
        valid_choice_objects=choice.objects.filter(poll_object=poll_object)
        choice_object=serializer.validated_data.get('choice_object')
        # choice_object=choice.objects.get(id=choice_id)
        if choice_object not in valid_choice_objects:
            raise serializers.ValidationError("invalid choice for poll!!")
        return serializer.save(poll_object=poll_object,owner_object=self.request.user)
    