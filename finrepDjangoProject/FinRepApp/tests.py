from django.test import TestCase
from django.contrib.auth.models import User

user = User.objects.create_user('juan', 'perez@hotmail.com', 'contra')
# Create your tests here.

#def flutter_redirect(request, resource):

#def xlsx_upload(request):

#def balanceGeneral(request):