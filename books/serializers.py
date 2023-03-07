from rest_framework import serializers

from books import models


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""
    class Meta:
        model = models.UserProfile
        fields = (
            'id',
            'email', 'name',
            'password', 'image')
        extra_kwargs = {'password': {
            'write_only': True, 'style': {
                'input_type': 'password', 'placeholder': 'Password'}
        }}

    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""

    class Meta:
        model = models.Category
        fields = ['id', 'category_name']


class EditorSerializer(serializers.ModelSerializer):
    """Serializer for Editor model"""

    class Meta:
        model = models.Editor
        fields = ['id', 'url', 'editor_name']
        extra_kwargs = {
            'url': {'view_name': 'books:editor-detail',
                    'lookup_field': 'editor_name'},
        }

class BooksSerializer(serializers.ModelSerializer):
    """Serializes books from model"""
    category = CategorySerializer(many=True, required=False)

    class Meta:
        model = models.Books
        fields = ['id', 'title', 'author', 'editor',
                  'price', 'description',
                  'release_date', 'language', 'category', 'image']
        # extra_kwargs = {
        #     'url': {'view_name': 'books:books-detail',
        #             'lookup_field': 'title'}
        # }
        read_only_fields = ['id']


class ReadBooksSerializer(serializers.ModelSerializer):
    """Serializer for user's read books"""
    book_title = serializers.ReadOnlyField()
    book_image = serializers.ImageField()
    class Meta:
        model = models.ReadBooks
        fields = ['id', 'book', 'book_title', 'book_image']


class ReadBooksAddSerializer(serializers.ModelSerializer):
    """Serializer for adding a new book to the read books model"""
    book_id = serializers.IntegerField()
    book_title = serializers.ReadOnlyField()
    book_image = serializers.ReadOnlyField()

    class Meta:
        model = models.ReadBooks
        fields = ['id', 'user', 'book', 'book_id', 'book_title', 'book_image']
        extra_kwargs = {'user': {'read_only':True},
                        }

    def create(self, validated_data):
        auth_user = self.context['request'].user
        book = models.Books.objects.get(id=validated_data['book_id'])

        new_read_book = models.ReadBooks.objects.create(
            book = book,
            user = auth_user
        )
        new_read_book.save()
        return new_read_book


class BasicUserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Books
        fields = ['id', 'title', 'author', 'editor',
                  'price', 'description',
                  'release_date', 'language', 'category', 'image']
        read_only_fields = ['id', 'title', 'author', 'editor',
                  'price', 'description',
                  'release_date', 'language', 'category', 'image']

class BasicUserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'
        read_only_fields = ['id', 'user', 'category_name']