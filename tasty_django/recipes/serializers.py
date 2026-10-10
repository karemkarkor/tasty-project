from rest_framework import serializers
from .models import Recipe, Favorite, User


class RecipeSerializer(serializers.ModelSerializer):
    """
    Serializes Recipe model.
    IMPORTANT: cookTime field is exposed as 'cookTime' (camelCase) to stay
    compatible with the existing JavaScript frontend, even though the Django
    model field is cook_time (snake_case).
    """
    cookTime = serializers.CharField(source='cook_time')

    class Meta:
        model = Recipe
        fields = ['id', 'type', 'image', 'title', 'description', 'cookTime', 'ingredients', 'steps']

    def create(self, validated_data):
        # source='cook_time' means DRF puts the value under cook_time in validated_data
        return Recipe.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.image = validated_data.get('image', instance.image)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.cook_time = validated_data.get('cook_time', instance.cook_time)
        instance.ingredients = validated_data.get('ingredients', instance.ingredients)
        instance.steps = validated_data.get('steps', instance.steps)
        instance.save()
        return instance


class RecipeWriteSerializer(serializers.Serializer):
    """
    Used for POST /api/add-recipe and PUT /api/update-recipe/:id.
    Mirrors exactly the fields the frontend sends in req.body.
    """
    type = serializers.CharField(required=False, allow_blank=True, default='')
    image = serializers.CharField(required=False, allow_blank=True, default='')
    title = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True, default='')
    cookTime = serializers.CharField(required=False, allow_blank=True, default='')
    ingredients = serializers.ListField(child=serializers.CharField(), default=list)
    steps = serializers.ListField(child=serializers.CharField(), default=list)

    def create(self, validated_data):
        return Recipe.objects.create(
            type=validated_data.get('type', ''),
            image=validated_data.get('image', ''),
            title=validated_data['title'],
            description=validated_data.get('description', ''),
            cook_time=validated_data.get('cookTime', ''),
            ingredients=validated_data.get('ingredients', []),
            steps=validated_data.get('steps', []),
        )

    def update(self, instance, validated_data):
        instance.type = validated_data.get('type', instance.type)
        instance.image = validated_data.get('image', instance.image)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.cook_time = validated_data.get('cookTime', instance.cook_time)
        instance.ingredients = validated_data.get('ingredients', instance.ingredients)
        instance.steps = validated_data.get('steps', instance.steps)
        instance.save()
        return instance


class SignupSerializer(serializers.Serializer):
    """
    Handles /signup POST body: username, email, password, user_type.
    """
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(
        choices=['normal', 'admin'],
        default='normal',
        required=False
    )

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Username or email already exists.")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username or email already exists.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data.get('user_type', 'normal'),
        )
        # Mirror Express: admin users also get Django staff status
        if validated_data.get('user_type') == 'admin':
            user.is_staff = True
            user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """
    Handles /login POST body: username, email, password.
    The original Express code checks all three fields simultaneously.
    """
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
