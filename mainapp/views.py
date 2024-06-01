from django.shortcuts import render
from django.contrib.auth.models import User
from mainapp.models import Userdata
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from mainapp.gpa_result_algorithm import generate_possible_results, get_total_units


# Create your views here.
class TestView(APIView):

    def get(self, request):
        data = {'user': request.user}
        print(request.user)
        return Response(str(data))


@permission_classes([AllowAny])
@authentication_classes([])
class SignUp(APIView):

    def post(self, request):
        data = request.POST
        print(data)
        username = data['username']
        password = data['password']

        user = User.objects.create_user(username=username, password=password)

        if user:
            userdata = Userdata(username=username, saved_results="")
            userdata.save()

            return Response('ok')

        return Response('fail')


class GenerateResults(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        gpa = request.data.get('gpa')
        courses = request.data.get('courses')

        print(gpa)
        print(courses)

        results = generate_possible_results(gpa, courses)

        return Response(results)


class GenerateResultsCgpa(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):

        cgpa = float(request.data.get('cgpa'))
        total_marks = int(request.data.get('total_marks'))
        total_units = int(request.data.get('total_units'))
        courses = request.data.get('courses')

        total_current_units = int(get_total_units(courses))
        required_marks = (cgpa * (total_units + total_current_units)) - int(total_marks)

        gpa = float(required_marks) / float(total_current_units)
        gpa = round(gpa, 2)

        if gpa > 5.0:
            return Response({'status': 'This result is IMPOSSIBLE. go home and take a nap'})

        print(f"DATA: {gpa}, {cgpa}, {total_current_units}, {required_marks}")

        results = generate_possible_results(gpa, courses)

        return Response(results)


class SaveResult(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Userdata.objects.get(username=str(request.user))
        return Response({'status': 'ok', 'data': user.saved_results})

    def post(self, request):
        print(str(request.user))
        save_result = request.data.get('result')

        user = Userdata.objects.get(username=str(request.user))
        print(user)
        text = user.saved_results
        text += f";{save_result}"
        user.saved_results = text

        user.save()

        return Response({'status': 'ok'})


    def put(self, request):
        save_result = request.data.get('result')
        print(save_result)

        user = Userdata.objects.get(username=str(request.user))
        user.saved_results = save_result

        user.save()

        return Response({'status': 'ok'})

