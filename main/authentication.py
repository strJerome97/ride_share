
from rest_framework import authentication, exceptions
from .models import User

class AuthenticateUser(authentication.BaseAuthentication):
    def authenticate(self, request):
        email = request.headers.get('X-User-Email')
        print(email)
        if not email:
            raise exceptions.AuthenticationFailed('No email header provided')
        try:
            user = User.objects.get(email=email)
            if user.role != 'admin':
                raise exceptions.AuthenticationFailed('User is not an admin')
            else:
                return (user, None)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
