from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ProjectForm
from .models import Project

# projectsList = [
#     {
#         "id": "1",
#         "title": "Ecommerce Website",
#         "description": "Fully functional ecommerce website",
#     },
#     {
#         "id": "2",
#         "title": "Portfolio Website",
#         "description": "This was a project where I built out my portfolio",
#     },
#     {
#         "id": "3",
#         "title": "Social Network",
#         "description": "Awesome open source project I am still working on",
#     },
# ]

# Create your views here.


def projects(request):
    # page = "projects"
    # number = 10
    # context = {"page": page, "number": number, "projects": projectsList}
    # return HttpResponse("Here are our products.")
    # return render(request, "projects/projects.html", context)

    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, "projects/projects.html", context)


def project(request, pk):
    # projectObj = None
    # for i in projectsList:
    #     if i["id"] == pk:
    #         projectObj = i
    # return HttpResponse("Single Project." + " " + str(pk))
    # return render(request, "projects/single-project.html", {"project": projectObj})
    projectObj = Project.objects.get(id=pk)
    # tags = projectObj.tags.all()
    # print("projectObj:", projectObj)
    # return render(request, "projects/single-project.html", {"project": projectObj,'tags':tags})
    return render(request, "projects/single-project.html", {"project": projectObj})


def createProject(request):
    form = ProjectForm()
    if request.method == "POST":
        # print(request.POST)
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        # print(request.POST)
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects")
    context = {"object": project}
    return render(request, "projects/delete_template.html", context)
