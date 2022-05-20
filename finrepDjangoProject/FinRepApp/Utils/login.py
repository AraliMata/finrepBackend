from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse


#user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

#Registro del usuario
def register(request):
    if request.method == 'POST':
        print("saludos")
        username = request.POST.get('username')
        email = request.POST.get('username')
        password = request.POST.get('username')
        user = User.objects.create_user(username, email, password)
        return HttpResponse()

#Login del usuario
def my_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        print("login exitoso")
        return HttpResponse()
        #print(user.id)
        # Redirect to a success page.
        #Return exito
        ...
    else:
        print('terrible')
        return HttpResponse()
        # Return an 'invalid login' error message.

#Logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.