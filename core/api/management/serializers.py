"""
Place here common serializers related to the management.
"""
import requests
from rest_framework import serializers


class GoogleTokenSerializer(serializers.Serializer):
    """
    Serializer to handle auth/signup with google.
    """

    def validate_google_access_token(self, token):
        r = requests.get('https://www.googleapis.com/oauth2/v2/userinfo', params={'access_token': token}).json()
        if er := r.get('error'):
            raise serializers.ValidationError(er.get('message'))
        if not r.get('verified_email'):
            raise serializers.ValidationError(f'The email {r.get("email")} is not verified.')
        if self.initial_data.get('email') != r.get('email'):
            raise serializers.ValidationError('The emails do not match.')
        return r
