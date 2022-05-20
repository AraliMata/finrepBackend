from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


#user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

#Registro del usuario
def register(request):
    if request.method == 'POST':
        print("saludos")
        user = User.objects.create_user('isaac', 'raulchencho@hotmail.com', 'sisi')

#Login del usuario
def my_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        print("login exitoso")
        print(user.id)
        # Redirect to a success page.
        #Return exito
        ...
    else:
        print('terrible')
        # Return an 'invalid login' error message.

#Logout


def logout_view(request):
    logout(request)
    # Redirect to a success page.