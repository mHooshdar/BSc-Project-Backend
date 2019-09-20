from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
import copy, sys

from .serializers import FileSerializer, CategorySerializer
from tagging_project.file.models import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from tagging_project.file.models import Category


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_file(request):
    from object_detection.object_detection import detect_object
    from googletrans import Translator

    translator = Translator()
    a = copy.deepcopy(request.data)
    result_image, categories = detect_object(request.FILES["file"])
    result_image.seek(0)

    a["result"] = InMemoryUploadedFile(result_image, 'ImageField', request.FILES["file"].name, 'image/jpeg', sys.getsizeof(result_image), None)

    translated = {}
    description = []
    description_fa = []

    categories = sorted(categories, key=lambda x: x['area'] * x['score'], reverse=True)

    index = 0
    # translate from google
    for category in categories:
        class_name = category['class_name']
        if class_name not in translated:
            translated[class_name] = translator.translate(class_name, dest='fa').text
        category['class_name_fa'] = translated[class_name]

        if index < 5 and class_name not in description:
            description.append(category['class_name'])
            description_fa.append(category['class_name_fa'])
            index += 1

    description = "-".join(description)
    description_fa = "-".join(description_fa)

    a["description"] = description
    a["description_fa"] = description_fa

    file_serializer = FileSerializer(data=a, context={'request': request})

    if file_serializer.is_valid():
        file = file_serializer.save()

        for category in categories:
            category['file'] = file.id

        category_serializer = CategorySerializer(data=categories, many=True)

        if category_serializer.is_valid():
            category_serializer.save()
            return Response({
                **file_serializer.data,
                "categories": category_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_files(request, user_id):
    result = []
    files = File.objects.filter(user=user_id)
    file_serializer = FileSerializer(files, many=True)

    for file in file_serializer.data:
        categories = Category.objects.filter(file=file['id'])
        category_serializer = CategorySerializer(categories, many=True)
        result.append({
            **file,
            'categories': category_serializer.data
        })

    return Response(result, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_file(request, file_id):
    file = File.objects.filter(pk=file_id)
    if file:
        file.delete()
        return Response({
            'file_id': file_id,
            'message': 'File Deleted'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'file_id': file_id,
            'message': 'File Not Found',
            'error': True
        }, status=status.HTTP_404_NOT_FOUND)