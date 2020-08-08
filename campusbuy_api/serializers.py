from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from app.models import User, OnlineStore, Category, SubCategory
from django.db.models import ObjectDoesNotExist


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False)
    fullname = serializers.CharField(required=True)
    whatsapp_number = serializers.CharField(required=False)
    business_name = serializers.CharField(required=False, max_length=500)
    address = serializers.CharField(required=False, max_length=1000)
    description = serializers.CharField(required=False, max_length=1000)
    email = serializers.EmailField(required=True)
    is_merchant = serializers.BooleanField(required=False, default=False)

    username = serializers.CharField(required=True, max_length=32)
    password = serializers.CharField(required=True, min_length=8, write_only=True)

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    @staticmethod
    def validate_phone_number(value):
        """
        check that a correct phone_number was inputted
        """
        # print(self)
        try:
            _exists = User.objects.get(phone_number=value)
        except ObjectDoesNotExist:
            _exists = None

        if len(value) != 11:
            raise serializers.ValidationError('The length of the phone_number is incorrect')
        elif _exists:
            raise serializers.ValidationError('The phone_number provided is already in use!')

        return value

    @staticmethod
    def validate_username(value):
        """
        check that a correct never been use before username was provided
        """
        # print(self)
        try:
            _exists = User.objects.get(username=value)
        except ObjectDoesNotExist:
            _exists = None

        if _exists:
            raise serializers.ValidationError('The username provided is already in use!')

        return value

    @staticmethod
    def validate_email(value):
        """
        check that a correct never been use before username was provided
        """
        # print(self)
        try:
            _exists = User.objects.get(email=value)
        except ObjectDoesNotExist:
            _exists = None

        if _exists:
            raise serializers.ValidationError('The email provided is already in use!')

        return value

    @staticmethod
    def validate_whatsapp_number(value):
        """
        check that a correct whatsapp_number was inputted
        """

        try:
            _exists = User.objects.get(whatsapp_number=value)
        except ObjectDoesNotExist:
            _exists = None

        if len(value) != 11:
            raise serializers.ValidationError('The length of the phone_number is incorrect')
        elif _exists:
            raise serializers.ValidationError('The phone_number provided is already in use!')

        return value

    def validate(self, data):
        """

        """
        is_merchant = data.get("is_merchant", False)
        business_name = data.get("business_name", "")
        description = data.get("description", "")
        address = data.get("address", "")
        phone_number = data.get("phone_number", "")
        whatsapp_number = data.get("whatsapp_number", "")

        if is_merchant and (not business_name or not description or not address or not phone_number or not whatsapp_number):
            raise serializers.ValidationError(
                'If is_merchant==True the following fields are required:  business_name, description , address, whatsapp_number, phone_number')

        return data

    def create(self, validated_data):
        business_name = validated_data.pop("business_name") if validated_data.get("business_name") else None
        description = validated_data.pop("description") if validated_data.get("description") else None
        address = validated_data.pop("address") if validated_data.get("address") else None
        print(validated_data.get("phone_number"), "phonenumber====")
        user = User.objects.create_user(**validated_data)

        if validated_data.get("is_merchant"):

            store = OnlineStore(owner=user, business_name=business_name, description=description,
                                address=address).save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone_number',
                  'whatsapp_number', 'fullname', 'school',
                  'token', "is_merchant", "address", "description", "business_name")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, max_length=255)
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    #
    # def validate_email(self, value):
    #     """
    #     check that the email is correct
    #     """
    #     pass

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid" information. In the case of logging a
        # user in, this means validating that they've provided a username or email
        # and password and that this combination matches one of the users in
        # our database.

        user = None
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email and username is not provided.
        if not username and not email:
            raise serializers.ValidationError(
                'A username or an email is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this username/password combination.
        if username:
            user = authenticate(username=username, password=password)

            # if user is none raise a validation  error
            if user is None:
                raise serializers.ValidationError(
                    'A user with this username and password was not found.'
                )

        if email:
            # search the database for a user with the provided email
            # and extract the username and check for the username/password combination
            try:
                u = User.objects.get(email=email)

            except ObjectDoesNotExist:
                raise serializers.ValidationError(
                    'A user with this email and password was not found.'
                )

            username = u.username
            user = authenticate(username=username, password=password)

            # if user is none raise a validation  error
            if user is None:
                raise serializers.ValidationError(
                    'A user with this email and password was not found.'
                )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token}


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'details', 'date_created')


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'category', 'date_created')
