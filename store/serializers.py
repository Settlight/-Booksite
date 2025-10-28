from rest_framework import serializers
from .models import Book, Author, Publisher


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    author_names = serializers.SerializerMethodField(read_only=True)
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'description',
            'authors',
            'publisher',
            'author_names',
            'publisher_name',
            'price',
            'stock'
        ]

    def get_author_names(self, obj):
        return ", ".join(a.name for a in obj.authors.all())
