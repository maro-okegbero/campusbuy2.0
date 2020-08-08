from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.models import Category, SubCategory
from campusbuy_api.serializers import LoginSerializer, UserSerializer, CategorySerializer, SubCategorySerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Log a user using the username and password as the authentication credentials
    """
    data = request.data
    print(data, "User===========")
    serializer = LoginSerializer(data=data)
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a user
    """
    # data = JSONParser().parse(request.data)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            print(dir(user), "dir user========")
            token = user.token
            json = serializer.data
            json['token'] = token
            return Response(json, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def category_handler(request, pk=None):
    """
    View to handle all requests regarding categories
    """
    if pk:
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category)
            data = serializer.data
            subcategories = category.subcategory_set.all()
            sc = SubCategorySerializer(subcategories, many=True)
            data["subcategories"] = sc.data
            return Response(data, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            response = {'message': "No category with that id exists",
                        "status": "fail"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
@permission_classes([AllowAny])
def subcategory_handler(request, pk=None):
    """
    view to handle all subcategory related requests
    """
    if pk:
        try:
            subcategory = SubCategory.objects.get(pk=pk)
            serializer = SubCategorySerializer(subcategory)
            data = serializer.data
            subcategories = subcategory.product_set.all()
            products = SubCategorySerializer(subcategories, many=True)
            data["products"] = products.data
            return Response(data, status=status.HTTP_200_OK)

        except Category.DoesNotExist:
            response = {'message': "No category with that id exists",
                        "status": "fail"}
            return Response(response, status=status.HTTP_404_NOT_FOUND)

