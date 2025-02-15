import logging
from users.models import User
from users.global_parameters import *
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializer import UserLoginSerializer, UserRegistrationSerializer


logger = logging.getLogger(__name__)

class UserLoginAPI(APIView):
    """
    Handles user login and token generation.

    This API endpoint accepts login data (e.g., username and password), 
    validates it, and generates JWT tokens if the data is valid. It also logs 
    the login attempts and provides error messages when the login is unsuccessful.
    """
    def post(self, request):
        """
        Handle POST request for user login.

        This method accepts incoming login credentials, validates them using the 
        `UserLoginSerializer`, and returns JWT tokens upon successful authentication. 
        In case of invalid data or errors, it returns the relevant validation 
        error messages or a generic error response.

        Arguments:
        - request: The HTTP request containing the login data.

        Returns:
        - Response: A response containing either JWT tokens, validation errors, 
          or a generic error message.
        """
        # Initialize the serializer with incoming data
        serializer = UserLoginSerializer(data=request.data)
        
        try:
            # Validate the data and create tokens if valid
            if serializer.is_valid():
                # Get the JWT tokens
                tokens = serializer.create(serializer.validated_data)
                return Response(tokens, status=HTTP_200_success)
            
            logger.warning(f"Invalid login attempt: {serializer.errors}")
            # Return validation errors if invalid
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"An error occurred during login: {str(e)}")
            return Response({"detail": "An error occurred during login."}, status=HTTP_500_INTERNAL_SERVER_ERROR)



class UserRegistrationAPI(APIView):
    """
    Handles the user registration process.

    This API endpoint accepts user registration data, validates the data,
    creates a new user registration, hashes the user's password, and
    saves the user to the database. It also logs the registration attempt,
    including both successful and failed attempts.
    """
    def post(self, request):
        """
        Handle the POST request for user registration.

        This method takes incoming registration data, validates it using
        the UserRegistrationSerializer, and creates a new user if the data
        is valid. It hashes the password before saving the user to the database.
        
        If the data is invalid, it returns a detailed error message. If
        there is an unexpected error during user creation, it returns a generic
        error message.

        Arguments:
        - request: The HTTP request containing the registration data.

        Returns:
        - Response: A response with either a success message or validation errors.
        """
        # Initialize the serializer with incoming data
        serializer = UserRegistrationSerializer(data=request.data)
        
        try:
            # Check if the data is valid
            if serializer.is_valid():
                # If the data is valid, create the user
                user_data = serializer.validated_data
                user = User.objects.create(
                    phone_number=user_data['phone_number'],
                    username=user_data.get('username', ''),  # Use default '' if no username is provided
                    password=user_data['password'],
                    membership_type=user_data['membership_type'],
                )
                user.set_password(user_data['password'])
                user.save()

                logger.info(f"User registered successfully: {user.username}, Phone: {user.phone_number}")
                # Return a success response
                return Response({'message': 'User registered successfully'}, status=HTTP_201_CREATED)
            
            logger.warning(f"Invalid registration data: {serializer.errors}")
            # If the data is invalid, return error messages
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"An error occurred during registration: {str(e)}")
            return Response({"detail": "An error occurred during registration."}, status=HTTP_500_INTERNAL_SERVER_ERROR)