from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from projects.models import Project, Review, Tag

from .serializers import ProjectSerializer


@api_view(["GET"])
def getRoutes(request):
    routes = [
        {"GET": "/api/projects"},
        {"GET": "/api/projects/id"},
        {"POST": "/api/projects/id/vote"},
        {"POST": "/api/users/token"},
        {"POST": "/api/users/token/refresh"},
    ]

    # return JsonResponse(routes, safe=False)
    return Response(routes)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getProjects(request):
    # print("USER : ", request.user)
    projects = Project.objects.all()
    # convert projects to json data
    serializer = ProjectSerializer(projects, many=True)
    # return serialized projects
    return Response(serializer.data)


@api_view(["GET"])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    # convert projects to json data
    serializer = ProjectSerializer(project, many=False)
    # return serialized projects
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    print("DATA : ", data)

    review, created = Review.objects.get_or_create(owner=user, project=project)
    review.value = data["value"]
    review.save()
    project.getVoteCount

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)
