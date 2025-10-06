from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.deletion import ProtectedError

from .models import Book, Author, Publisher
from .serializers import BookSerializer, AuthorSerializer, PublisherSerializer

class BookListCreateAPIView(APIView):
    def get(self, request):
        qs = Book.objects.all().order_by('-created_at')
        q = request.GET.get('q')
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(authors__name__icontains=q)).distinct()
        author_id = request.GET.get('author_id')
        if author_id:
            qs = qs.filter(authors__id=author_id)
        publisher_id = request.GET.get('publisher_id')
        if publisher_id:
            qs = qs.filter(publisher__id=publisher_id)
        ordering = request.GET.get('ordering')
        if ordering in ['price', '-price', 'created_at', '-created_at', 'title', '-title']:
            qs = qs.order_by(ordering)
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page_size', 10)
        paginator = Paginator(qs, page_size)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        serializer = BookSerializer(items, many=True)
        return Response({
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'results': serializer.data
        })

    def post(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Only admin can create books.'}, status=status.HTTP_403_FORBIDDEN)
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
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Only admin can edit books.'}, status=status.HTTP_403_FORBIDDEN)
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            book = serializer.save()
            return Response(BookSerializer(book).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Only admin can delete books.'}, status=status.HTTP_403_FORBIDDEN)
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AuthorListCreateAPIView(APIView):
    def get(self, request):
        qs = Author.objects.all().order_by('name')
        q = request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        serializer = AuthorSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Only admin can create authors.'}, status=status.HTTP_403_FORBIDDEN)
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
        data['books'] = [{'id': b.id, 'title': b.title, 'price': str(b.price)} for b in books]
        return Response(data)

    def patch(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Only admin can update authors.'}, status=status.HTTP_403_FORBIDDEN)
        author = get_object_or_404(Author, pk=pk)
        serializer = AuthorSerializer(author, data=request.data, partial=True)
        if serializer.is_valid():
            author = serializer.save()
            return Response(AuthorSerializer(author).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Only admin can delete authors.'}, status=status.HTTP_403_FORBIDDEN)
        author = get_object_or_404(Author, pk=pk)
        if author.books.exists():
            return Response({'detail': 'Cannot delete author with existing books.'}, status=status.HTTP_400_BAD_REQUEST)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PublisherListCreateAPIView(APIView):
    def get(self, request):
        qs = Publisher.objects.all().order_by('name')
        serializer = PublisherSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Only admin can create publishers.'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PublisherSerializer(data=request.data)
        if serializer.is_valid():
            pub = serializer.save()
            return Response(PublisherSerializer(pub).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PublisherDetailAPIView(APIView):
    def get(self, request, pk):
        pub = get_object_or_404(Publisher, pk=pk)
        data = PublisherSerializer(pub).data
        data['books'] = [{'id': b.id, 'title': b.title, 'price': str(b.price)} for b in pub.books.all()]
        return Response(data)

    def patch(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Only admin can update publishers.'}, status=status.HTTP_403_FORBIDDEN)
        pub = get_object_or_404(Publisher, pk=pk)
        serializer = PublisherSerializer(pub, data=request.data, partial=True)
        if serializer.is_valid():
            pub = serializer.save()
            return Response(PublisherSerializer(pub).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        if not request.user.is_authenticated or not request.user.is_staff:
            return Response({'detail': 'Only admin can delete publishers.'}, status=status.HTTP_403_FORBIDDEN)
        pub = get_object_or_404(Publisher, pk=pk)
        if pub.books.exists():
            return Response({'detail': 'Cannot delete publisher with existing books.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pub.delete()
        except ProtectedError:
            return Response({'detail': 'Cannot delete publisher due to related protected objects.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
