from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Book, Author, Publisher
from .serializers import BookSerializer, AuthorSerializer, PublisherSerializer


class BookListCreateAPIView(APIView):
    def get(self, request):
        qs = Book.objects.all().order_by('-created_at')
        q = request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q)
        author_id = request.GET.get('author_id')
        if author_id:
            qs = qs.filter(authors__id=author_id)
        publisher_id = request.GET.get('publisher_id')
        if publisher_id:
            qs = qs.filter(publisher__id=publisher_id)
        serializer = BookSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()
            return Response(BookSerializer(book).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailAPIView(APIView):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        return Response(BookSerializer(book).data)

    def patch(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            book = serializer.save()
            return Response(BookSerializer(book).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorListCreateAPIView(APIView):
    def get(self, request):
        qs = Author.objects.all().order_by('name')
        serializer = AuthorSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            author = serializer.save()
            return Response(AuthorSerializer(author).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorDetailAPIView(APIView):
    def get(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        data = AuthorSerializer(author).data
        books = author.books.all()
        data['books'] = [{'id': b.id, 'title': b.title} for b in books]
        return Response(data)

    def patch(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            author = serializer.save()
            return Response(AuthorSerializer(author).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        if author.books.exists():
            return Response({'error': 'Cannot delete author with existing books.'}, status=status.HTTP_400_BAD_REQUEST)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublisherListCreateAPIView(APIView):
    def get(self, request):
        qs = Publisher.objects.all().order_by('name')
        serializer = PublisherSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            publisher = serializer.save()
            return Response(PublisherSerializer(publisher).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublisherDetailAPIView(APIView):
    def get(self, request, pk):
        publisher = get_object_or_404(Publisher, pk=pk)
        data = PublisherSerializer(publisher).data
        data['books'] = [{'id': b.id, 'title': b.title} for b in publisher.books.all()]
        return Response(data)

    def patch(self, request, pk):
        publisher = get_object_or_404(Publisher, pk=pk)
        serializer = PublisherSerializer(publisher, data=request.data, partial=True)
        if serializer.is_valid():
            publisher = serializer.save()
            return Response(PublisherSerializer(publisher).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        publisher = get_object_or_404(Publisher, pk=pk)
        if publisher.books.exists():
            return Response({'error': 'Cannot delete publisher with existing books.'}, status=status.HTTP_400_BAD_REQUEST)
        publisher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
