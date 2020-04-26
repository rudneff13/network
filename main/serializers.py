from rest_framework import serializers
from .models import User, Post


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class PostSerializer(serializers.ModelSerializer):
    def validate(self, data):
        data['user_id'] = self.context['request'].user.id
        return super().validate(data)

    class Meta:
        model = Post
        fields = ('id', 'header', 'text', 'user_id', 'total_likes')


class ActivitySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    activity = serializers.CharField(max_length=50)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
