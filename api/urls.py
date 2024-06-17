from django.urls import path, re_path

from api.views.user import (AcceptFriendRequestView, FriendRequestsListView,
                            FriendRequestView, FriendsListView,
                            RejectFriendRequestView, TokenObtainPairView,
                            TokenRefreshView, UserSearchView, UserSignupView)

urlpatterns = [
    path("auth/signup/", UserSignupView.as_view(), name="signup"),
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    re_path(r"^auth/token/refresh/$", TokenRefreshView.as_view()),
    path("users/search/", UserSearchView.as_view(), name="user-search"),
    path("request/", FriendRequestView.as_view(), name="request"),
    path("friends/", FriendsListView.as_view(), name="friend-list"),
    path(
        "friend-requests/",
        FriendRequestsListView.as_view(),
        name="pending-friend-requests",
    ),
    path(
        "friend-requests/<int:id>/accept/",
        AcceptFriendRequestView.as_view(),
        name="accept-friend-request",
    ),
    path(
        "friend-requests/<int:id>/reject/",
        RejectFriendRequestView.as_view(),
        name="reject-friend-request",
    ),
]
