from django.contrib import admin
from django.urls import path
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import mainapp.views

urlpatterns = [
    path("test/", mainapp.views.TestView.as_view()),
    path("signup/", mainapp.views.SignUp.as_view()),
    path("generate/", mainapp.views.GenerateResults.as_view()),
    path("cgpagenerate/", mainapp.views.GenerateResultsCgpa.as_view()),
    path("saveresult/", mainapp.views.SaveResult.as_view())
]