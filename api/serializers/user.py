from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.models.user import FriendRequest, User


class TokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        attrs["email"] = attrs["email"].lower()
        attrs["password"] = attrs["password"]

        user = authenticate(username=attrs["email"], password=attrs["password"])
        if user is None or not user.is_active:
            raise serializers.ValidationError("Invalid email or password.")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super(TokenObtainPairSerializer, cls).get_token(user)

        token["name"] = user.get_username()
        token["is_admin"] = user.is_superuser
        # ...

        return token


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "gender",
            "avatar",
            "avatar_url",
        )

    def get_avatar_url(self, obj):
        try:
            return obj.avatar.url
        except Exception:
            return None


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        extra_kwargs = {
            "username": {"required": True},
            "password": {
                "write_only": True,
                "required": True,
                "min_length": 8,
            },
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }
        fields = ("username", "password", "email", "first_name", "last_name", "gender")

    def validate(self, data):
        username = data["username"].lower()
        email = data["email"].lower()

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": "This username is already taken."}
            )

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": "This email is already registered."}
            )

        return data

    def create(self, validated_data):
        if "username" in validated_data.keys():
            validated_data["username"] = validated_data["username"].lower()
        if "email" in validated_data.keys():
            validated_data["email"] = validated_data["email"].lower()
        user = User.objects.create_user(**validated_data)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "avatar",
        )

    def update(self, instance, validated_data):
        if "first_name" in validated_data:
            instance.first_name = validated_data.pop("first_name")
            instance.save()
        if "last_name" in validated_data:
            instance.first_name = validated_data.pop("last_name")
            instance.save()
        if "avatar" in validated_data:
            instance.first_name = validated_data.pop("avatar")
            instance.save()
        return instance


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ["id", "from_user", "to_user", "timestamp", "status"]
        read_only_fields = ["from_user", "timestamp", "status"]

    def create(self, validated_data):
        from_user = self.context["request"].user
        to_user = validated_data["to_user"]
        friend_request, error = FriendRequest.send_friend_request(from_user, to_user)
        if error:
            raise serializers.ValidationError(error)
        return friend_request
