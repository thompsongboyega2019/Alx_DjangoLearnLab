from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
class FollowUserView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, user_id):
		user_to_follow = get_object_or_404(CustomUser, id=user_id)
		if user_to_follow == request.user:
			return Response({'detail': 'You cannot follow yourself.'}, status=400)
		request.user.following.add(user_to_follow)
		user_to_follow.followers.add(request.user)
		return Response({'detail': f'You are now following {user_to_follow.username}.'})

class UnfollowUserView(APIView):
	permission_classes = [permissions.IsAuthenticated]

	def post(self, request, user_id):
		user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
		request.user.following.remove(user_to_unfollow)
		user_to_unfollow.followers.remove(request.user)
		return Response({'detail': f'You have unfollowed {user_to_unfollow.username}.'})


from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(generics.GenericAPIView):
	queryset = CustomUser.objects.all()
	serializer_class = RegisterSerializer

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			'user': UserSerializer(user, context=self.get_serializer_context()).data,
			'token': token.key
		})

class CustomAuthToken(ObtainAuthToken):
	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		return Response({'token': token.key, 'user_id': user.pk, 'username': user.username})

class ProfileView(generics.RetrieveUpdateAPIView):
	queryset = CustomUser.objects.all()
	serializer_class = UserSerializer
	permission_classes = [permissions.IsAuthenticated]

	def get_object(self):
		return self.request.user
