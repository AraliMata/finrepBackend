from tokenize import String
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
# import json
import json

from rest_framework.response import Response


#user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

#Registro del usuario
def register(request):
    if request.method == 'POST':
        datos = json.loads(request.body)
        print("saludos")
        username = datos["username"]
        email = datos["email"]
        password = datos["password"]
        user = User.objects.create_user(username, email, password)
        return HttpResponse(user,status=201)

#Login del usuario
def my_view(request):
    datos = json.loads(request.body)
    username = datos["username"]
    password = datos["password"]
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        print("login exitoso")
        print(user.id)
        userId = user.id
        #print(password)
        # return HttpResponse(userId,status=200)
        return HttpResponse(json.dumps({"id":userId,"respuesta": "usuario y contraseña correctos","codigo": 510}),status=200)
        # return idddd
        # return user.id
        
        # Redirect to a success page.
        #Return exito
        ...
    else:
        print('terrible')
        return HttpResponse(json.dumps({"error": "Algún dato incorrecto","codigo": 52}),status = 204)
        # Return an 'invalid login' error message.

#Logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.