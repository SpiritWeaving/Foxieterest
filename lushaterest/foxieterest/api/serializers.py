from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from foxieterest.models import *
from django.core.validators import FileExtensionValidator

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):
    user_avatar = serializers.SerializerMethodField()
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'user_name', 'user_avatar',
                  'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_user_avatar(self, obj):
        if obj.user.avatar:
            return obj.user.avatar.url
        return None


class BoardSerializer(serializers.ModelSerializer):
    pins = serializers.SerializerMethodField(read_only=True)
    pin_count = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Board
        fields = ('id', 'title', 'description', 'is_private', 'pin_count', 'pins')
        read_only_fields = ('id', 'pin_count', 'pins')

    def get_pin_count(self, obj):
        return obj.pins.count()

    def get_pins(self, obj):
        return list(obj.pins.values('id', 'title', 'content', 'is_private'))

#======Учетная запись========
class UserSerializer(serializers.ModelSerializer):
    boards = BoardSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'created_at', 'boards')
        read_only_fields = ('id', 'created_at')


class PinSerializer(serializers.ModelSerializer):
    liked_by = UserSerializer(many=True, read_only=True)
    boards = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    user_avatar = serializers.SerializerMethodField()
    is_image = serializers.SerializerMethodField(read_only=True)
    is_video = serializers.SerializerMethodField(read_only=True)
    content = serializers.FileField(use_url=True,
                                    validators=[FileExtensionValidator(
                                        allowed_extensions=['mp4', 'webm', 'ogg',
                                                            'mov', 'avi', 'jpg',
                                                            'jpeg', 'png', 'gif',
                                                            'webp']
                                    )])

    class Meta:
        model = Pin
        fields = ('id', 'title', 'description', 'content', 'user', 'user_name', 'liked_by', 'is_image', 'is_video',
                  'user_avatar', 'created_at', 'updated_at', 'is_private', 'boards', 'comments')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_is_image(self, obj):
        return obj.is_image()

    def get_is_video(self, obj):
        return obj.is_video()

    def get_user_avatar(self, obj):
        if obj.user.avatar:
            return obj.user.avatar.url
        return None

    def get_boards(self, obj):
        boards_list = obj.boards.all()
        result = []
        for board in boards_list:
            result.append(board.title)
        return result


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,
                                     validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True,
                                     validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise ValidationError({'password': 'Введенные пароли не совпадают!'})
        return attrs

    # validated_data – это словарь с проверенными данными, полученными в
    # результате POST - запроса после выполнения метода serializer.is_valid()
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return {'user': user}
        raise serializers.ValidationError("Неверный логин или пароль")




