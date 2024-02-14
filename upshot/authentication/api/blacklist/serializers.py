from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken


class JWTTokenBlacklistSerializer(TokenBlacklistSerializer):
    token_class = RefreshToken


class SlidingTokenBlacklistSerializer(TokenBlacklistSerializer):
    token_class = SlidingToken
