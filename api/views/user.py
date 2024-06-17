from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.models.user import Friend, FriendRequest, User
from api.serializers.user import (FriendRequestSerializer,
                                  TokenObtainPairSerializer, UserSerializer,
                                  UserSignUpSerializer)

User = get_user_model()


class TokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super(TokenObtainPairView, self).post(request, *args, **kwargs)
        response.set_cookie("jwt", response.data["access"])
        response.set_cookie("test", "obtain")
        response["Access-Control-Allow-Credentials"] = True
        return response


class TokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        response = super(TokenRefreshView, self).post(request, *args, **kwargs)
        response.set_cookie("jwt", response.data["access"])
        response.set_cookie("test", "refresh")
        response["Access-Control-Allow-Credentials"] = True
        return response


class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny]


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        query = self.request.query_params.get("q")
        if query:
            if "@" in query:
                return User.objects.filter(email__iexact=query)
            return User.objects.filter(username__icontains=query)


class FriendRequestView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer


class FriendsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        friend_ids = Friend.objects.filter(from_user=self.request.user).values_list(
            "to_user_id", flat=True
        )
        friends = User.objects.filter(id__in=friend_ids)
        return friends


class AcceptFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = self.kwargs["id"]
        friend_user = User.objects.get(id=request_id)
        try:
            friend_request = FriendRequest.objects.get(
                to_user=request.user, from_user=friend_user
            )
        except FriendRequest.DoesNotExist:
            return Response(
                {"msg": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if friend_request.status == "accepted":
            return Response(
                {"status": "Friend request is already accepted."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend_request.accept()
        return Response(
            {"status": "Friend request accepted."}, status=status.HTTP_200_OK
        )


class RejectFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = self.kwargs["id"]
        friend_user = User.objects.get(id=request_id)
        try:
            friend_request = FriendRequest.objects.get(
                to_user=request.user, from_user=friend_user
            )
        except FriendRequest.DoesNotExist:
            return Response(
                {"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND
            )

        friend_request.reject()
        return Response(
            {"status": "Friend request rejected."}, status=status.HTTP_200_OK
        )


class FriendRequestsListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(
            to_user=self.request.user, status=FriendRequest.RequestStatus.PENDING
        )
