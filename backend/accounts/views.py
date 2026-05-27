
# RIGHT: Use DRF's Response for dictionaries/JSON
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view
from accounts.serializer import RegisterSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    email = request.data.get('email')
    email=serializer.validate_email(email)  #validate email before saving to database
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    return Response({'message': 'User registered successfully'})
    
