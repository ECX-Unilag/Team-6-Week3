from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics, filters
from rest_framework.reverse import reverse
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet
from .serializers import (RegisterSerializer, UserSerializer, ProfileSerializer, LanguageSerializer,
                          StageSerializer, StudyMaterialSerializer, QuestionSerializer, AnswerSerializer,
                          ResultSerializer)
from rest_framework.authentication import TokenAuthentication
from user.models import Profile
from language.models import Language, Stage, StudyMaterial, Question, AnswerOptions, Result


@api_view(['GET'])
@permission_classes(())
def api_root(request, format=None):
    return Response({
        'users': reverse('api-users', request=request, format=format),
        'login': reverse('api-login', request=request, format=format),
        'register': reverse('api-register', request=request, format=format),
        'languages': reverse('api-languages', request=request, format=format),
    })


@api_view(['POST', ])
@permission_classes(())
def registration_view(request):
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully register a new user'
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.create(user=account)
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data)


class ObtainAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        context = {}

        # username = request.POST.get('username')
        # password = request.POST.get('password')
        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        if user:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            context['response'] = 'Successfully authenticated.'
            context['pk'] = user.pk
            context['username'] = username
            context['token'] = token.key
        else:
            context['response'] = 'Error'
            context['error_message'] = 'Invalid credentials'
        return Response(context)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = []


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class LanguageList(generics.ListAPIView):
    search_fields = ['name']
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = []


class LanguageDetail(generics.RetrieveAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = []


class StageView(generics.RetrieveAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = []


class StudyMaterialView(generics.RetrieveAPIView):
    queryset = StudyMaterial.objects.all()
    serializer_class = StudyMaterialSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = []


class QuestionView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = []


class AnswerView(generics.RetrieveAPIView):
    queryset = AnswerOptions.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = []


class ResultView(generics.RetrieveUpdateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

