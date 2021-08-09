from stockupapi.views.auth import login_user
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from django.contrib.auth.models import User
import json
import pytz

class AuthTokenMiddleware(object):
    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """

        utc = pytz.UTC

        now = datetime.now()

        token_life = timedelta(seconds=24)

        recycle_date = utc.localize(now - token_life)

        login = None

        try:
            _, user_token = request.META["HTTP_AUTHORIZATION"].split(" ")
                
            token = Token.objects.get(key=user_token)

        except Token.DoesNotExist:
            # If sone passes a token that doesn't exist after being logged in, the reset property will cause the user to be 
            # redirected to login on the client side regardless of the token
            token = Token.objects.get(user_id=1)

            request.META["HTTP_AUTHORIZATION"]= f"Token {token.key}"

            request.reset = True

            response = self.get_response(request)

            return response

        except:
            login = login_user(request)

            token_dict = json.loads(login.content.decode("utf-8"))

            token = Token.objects.get(key=token_dict["token"])

        if token.created < recycle_date or login:

            user_id = token.user_id

            token.delete()

            new_token = Token.objects.create(user_id=user_id)

            request.META["HTTP_AUTHORIZATION"]= f"Token {new_token}"

            request.reset = True

        else:
            token.reset = False
            
        response = self.get_response(request)
        return response