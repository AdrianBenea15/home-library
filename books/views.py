from rest_framework import viewsets, mixins, generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import status


from books import models
from books import permissions
from books import serializers


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating user profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)

    def get_queryset(self):
        """Retrieve only logged in user profile"""
        return self.queryset.filter(email=self.request.user)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class EditorViewSet(viewsets.ModelViewSet,
                    mixins.ListModelMixin):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.EditorSerializer
    queryset = models.Editor.objects.all()
    lookup_field = 'editor_name'


class CategoryViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    permission_classes = (IsAuthenticated, permissions.StaffPermission)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return serializers.CategorySerializer
        elif self.request.user.is_staff == False:
            return serializers.BasicUserCategorySerializer
        return self.serializer_class


class BooksViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated, permissions.StaffPermission]
    serializer_class = serializers.BooksSerializer
    queryset = models.Books.objects.all()


    def get_serializer_class(self):
        if self.request.user.is_staff:
            return serializers.BooksSerializer
        elif self.request.user.is_staff == False:
            return serializers.BasicUserBookSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user=self.request.user)

    # def list(self, request):
    #     qs = self.get_queryset()
    #     data = qs.values_list('id', 'title', 'created_at', 'category', 'price')
    #     return Response({'data': data, 'status': status.HTTP_200_OK})
    #
    #
    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         title = serializer.data['title']
    #         author = serializer.data['author']
    #         price = serializer.data['price']
    #         description = serializer.data['description']
    #         models.Books.objects.create(
    #             user = request.user,
    #             title = title,
    #             author = author,
    #             price = price,
    #             description = description
    #         )
    #         return Response(status=status.HTTP_201_CREATED)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    # def partial_update(self, request, *args, **kwargs):
    #     book = self.get_object()
    #     data = request.data
    #
    #     book.price = data.get('price', book.price)
    #     book.save()
    #     serializer = serializers.BooksSerializer(book)
    #
    #     return Response(serializer.data)





    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         book_read = serializer.data['read']
    #         if book_read == True:
    #
    # def update(self, request, pk=None):
    #     qs = models.Books.objects.get(id=pk)


class ReadBooksView(generics.ListAPIView):
    serializer_class = serializers.ReadBooksSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        queryset = models.ReadBooks.objects.filter(user=self.request.user.id)
        return queryset


class ReadBooksAddView(generics.CreateAPIView):
    queryset = models.ReadBooks.objects.all()
    serializer_class = serializers.ReadBooksAddSerializer
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]


class ReadBooksDeleteView(generics.DestroyAPIView):
    queryset = models.ReadBooks.objects.all()
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, pk, format=None):
        all_read_books = models.ReadBooks.objects.filter(user=request.user)
        book_to_delete = all_read_books.get(pk=pk)
        book_to_delete.delete()
        return Response(status=status.HTTP_200_OK, data={'details': 'deleted'})

