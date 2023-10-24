from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import ProjectForm, ReviewForm
from .models import Project, Tag
from .utils import paginateProjects, searchProjects

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
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)
    context = {
        "projects": projects,
        "search_query": search_query,
        "custom_range": custom_range,
    }
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
    form = ReviewForm()
    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        # update the vote count
        projectObj.getVoteCount
        messages.success(request, "Your review was successfully submitted")
        return redirect("project", pk=projectObj.id)

    return render(
        request, "projects/single-project.html", {"project": projectObj, "form": form}
    )


@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":
        # print(request.POST)
        newtags = request.POST.get("newtags").replace(",", " ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect("account")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == "POST":
        # print(request.POST)
        newtags = request.POST.get("newtags").replace(",", " ").split()
        print("Data : ", request.POST)

        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect("account")

    context = {"form": form, "project": project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect("projects")
    context = {"object": project}
    return render(request, "delete_template.html", context)
