from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from core.models import Reader

class ReaderAuthentication(BaseAuthentication):

    def authenticate(self, request):
       
        api_key = request.headers.get('X-READER')

        if not api_key:
            return None
        
        try:
            reader = Reader.objects.get(api_key=api_key)
        
        except Reader.DoesNotExist:
            raise AuthenticationFailed("Invalid reader")
        
        request.reader = reader
        return (None, api_key)