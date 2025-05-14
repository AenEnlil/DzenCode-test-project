from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # try to decode token
        try:
            token = self.get_validated_token(self.get_raw_token(self.get_header(request)))
            guest_id = token.get('guest_id', None)

            if not guest_id:
                raise AuthenticationFailed('Token does not contain guest_id')

            # return no user and token
            return None, token

        except Exception as e:
            raise AuthenticationFailed('Invalid token or token missing required claims')
