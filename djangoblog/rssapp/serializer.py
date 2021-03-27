from rest_framework import serializers

from .models import User_feed, log_errors
from .utiles import get_rss_link


class Id_feed_serializer(serializers.Serializer):
    id = serializers.IntegerField()


class log_serializer(serializers.Serializer):
    id_feed = serializers.IntegerField()
    url = serializers.CharField(max_length=200)

    class Meta:
        model = log_errors
        fields = ['id_feed', 'url']

    def create(self, validate_data):
        return log_errors.objects.create(**validate_data)


class Add_feed_user(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    body = serializers.CharField(max_length=200)
    url = serializers.URLField(max_length=200)

    class Meta:
        model = User_feed
        fields = ['title', 'body', 'url']

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super().__init__(*args, **kwargs)

    def validate(self, attrs):
        author = self.author
        url = attrs["url"]
        url, found_rss = get_rss_link(url)
        attrs["url"] = url

        attrs["author"] = author
        # User_feed.objects.filter(title=title, author=author).exists() or

        if not found_rss:
            raise serializers.ValidationError(
                {'title': 'No sources found on this url.'})
        elif User_feed.objects.filter(url=url, author=author).exists():
            raise serializers.ValidationError(
                {'title': 'the url already exist'})
        return super().validate(attrs)

    def create(self, validate_data):
        return User_feed.objects.create(**validate_data)
