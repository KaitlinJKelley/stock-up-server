from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from django.contrib.auth.models import User

class AuthTokenMiddleware(object):
    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        now = datetime.utcnow()

        token_life = timedelta(hours=24)

        tokens = Token.objects.filter(created__lte=now - token_life)

        request.reset = False

        for token in tokens:

            Token.objects.get(user_id=token.user_id).delete()

            new_token = Token.objects.create(user_id=token.user_id)

            if request.META["HTTP_AUTHORIZATION"] == f"Token {token}":
                request.reset = True

                request.META["HTTP_AUTHORIZATION"]= f"Token {new_token}"

            
        response = self.get_response(request)
        return response