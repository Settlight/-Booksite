from rest_framework import serializers
from .models import Book, Author, Publisher

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'born_at', 'created_at']

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'name', 'description', 'created_at']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    author_names = serializers.SerializerMethodField()
    publisher = PublisherSerializer(read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Author.objects.all(), source='authors')
    publisher_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Publisher.objects.all(), source='publisher')

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'authors', 'author_names',
            'author_ids', 'publisher', 'publisher_id', 'price', 'stock',
            'published_at', 'created_at'
        ]

    def get_author_names(self, obj):
        return ", ".join([a.name for a in obj.authors.all()])

    def create(self, validated_data):
        authors = validated_data.pop('authors', [])
        publisher = validated_data.pop('publisher', None)
        book = Book.objects.create(publisher=publisher, **validated_data)
        if authors:
            book.authors.set(authors)
        return book

    def update(self, instance, validated_data):
        authors = validated_data.pop('authors', None)
        publisher = validated_data.pop('publisher', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if publisher is not None:
            instance.publisher = publisher
        instance.save()
        if authors is not None:
            instance.authors.set(authors)
        return instance
