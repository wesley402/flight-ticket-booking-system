from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

def create_users(number_of_users, prefix='bulk_user'):
  allUsernames = [user.username for user in User.objects.all()]
  for n in list(range(number_of_users)):
    username = f'{prefix}{n}'
    if not username in allUsernames:
      password = make_password('user123')
      User.objects.create(username=username,password=password)

