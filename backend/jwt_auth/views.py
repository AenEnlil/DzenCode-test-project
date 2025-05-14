import uuid
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


class JWTViewSet(ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='create')
    def create_token(self, request):
        # create guest id
        guest_id = str(uuid.uuid4())

        refresh = RefreshToken()
        refresh['guest_id'] = guest_id
        refresh['guest'] = True

        return Response({'access': str(refresh.access_token),
                         'refresh': str(refresh)})

    @action(detail=False, methods=['post'], url_path='refresh')
    def refresh_token(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Missing refresh token'}, status=401)
        try:
            refresh = RefreshToken(refresh_token)
            access = refresh.access_token
            return Response({'access': str(access)})
        except TokenError:
            return Response({'detail': 'Invalid or expired refresh token'}, status=401)
