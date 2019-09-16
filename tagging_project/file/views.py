from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from .serializers import FileSerializer
from tagging_project.file.models import File


@api_view(['PUT'])
def create_file(request):
    file_serializer = FileSerializer(data=request.data)

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
