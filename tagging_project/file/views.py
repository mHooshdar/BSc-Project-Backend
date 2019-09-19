from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from object_detection.object_detection import detect_object
import copy, sys

from .serializers import FileSerializer
from tagging_project.file.models import File
from django.core.files.uploadedfile import InMemoryUploadedFile


@api_view(['PUT'])
def create_file(request):
    a = copy.deepcopy(request.data)
    result_image, categories = detect_object(request.FILES["file"])
    result_image.seek(0)

    a["result"] = InMemoryUploadedFile(result_image, 'ImageField', request.FILES["file"].name, 'image/jpeg', sys.getsizeof(result_image), None)

    file_serializer = FileSerializer(data=a, context={'request': request})

    if file_serializer.is_valid():
        file_serializer.save()
        return Response(file_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_files(request, user_id):
    files = File.objects.filter(user=user_id)
    file_serializer = FileSerializer(files, many=True)

    return Response(file_serializer.data, status=status.HTTP_200_OK)
