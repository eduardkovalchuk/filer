from django.shortcuts import render, redirect
from django.conf import settings
from .models import Folder, File
from .forms import AddFolderForm, AddFileForm, DeleteForm, SearchForm, ChangeFolderForm, ChangeFileForm, LoginForm
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy


def tupalize(seq, name):
    return list(map(lambda x: (x, name + str(x.id)), seq))


def get_breadcrumbs(folder_id):
    breadcrumbs = []
    if folder_id:
        current_folder = Folder.objects.get(id=folder_id)
    else:
        return breadcrumbs
    while current_folder != None:
        breadcrumbs.append((current_folder.id, current_folder.name))
        current_folder = current_folder.parrent
    return breadcrumbs


def add_folder(request, context):
    if context["add_folder_form"].is_valid():
        new_context = context
        data = context["add_folder_form"].cleaned_data
        current_folder_id = context["current_folder_id"]
        name = data["name"]
        tags = data["tags"]
        if not Folder.objects.filter(name=name).filter(parrent__id=current_folder_id) and "\\" not in name and "/" not in name:
            if current_folder_id:
                current_folder = Folder.objects.get(id=current_folder_id)
                new_folder = Folder(name=name, tags=tags, parrent=current_folder)
            else:
                new_folder = Folder(name=name, tags=tags, parrent=None)
            new_folder.save()
            files = tupalize(File.objects.filter(parrent__id=current_folder_id), "file_")
            folders = tupalize(Folder.objects.filter(parrent__id=current_folder_id), "folder_")
            delete_form = DeleteForm(request.POST or None, folders=folders, files=files)
            new_context.update({"folders":folders,"delete_form":delete_form})
            return render(request, "searcher/view_folder.html", new_context)


def add_file(request, context):
    if context["add_file_form"].is_valid():
        new_context = context
        current_folder_id = context["current_folder_id"]
        tags = context["add_file_form"].cleaned_data["tags"]
        if current_folder_id:
            current_folder = Folder.objects.get(id=current_folder_id)
            file = File(upload=request.FILES['file'], parrent=current_folder, tags=tags)
        else:
            file = File(upload=request.FILES['file'], parrent=None, tags=tags)
        file.save()
        files = tupalize(File.objects.filter(parrent__id=current_folder_id), "file_")
        folders = tupalize(Folder.objects.filter(parrent__id=current_folder_id), "folder_")
        delete_form = DeleteForm(request.POST or None, folders=folders, files=files)
        new_context.update({"files":files,"delete_form":delete_form})
        return render(request, "searcher/view_folder.html", new_context)


def delete(request, context):
    new_context = context
    current_folder_id = context["current_folder_id"]
    if context["delete_form"].is_valid():
        cleaned_data = context["delete_form"].cleaned_data
        for folder, folder_field in context["folders"]:
            if folder_field in request.POST:
                folder.delete()
        for file_, file_field in context["files"]:
            if file_field in request.POST:
                file_.delete()
        files = tupalize(File.objects.filter(parrent__id=current_folder_id), "file_")
        folders = tupalize(Folder.objects.filter(parrent__id=current_folder_id), "folder_")
        delete_form = DeleteForm(request.POST or None, folders=folders, files=files)
        new_context.update({"files":files, "folders":folders, "delete_form":delete_form})
        return render(request, "searcher/view_folder.html", new_context)


#--------------------------------------------------------------------------------------------------
# Admin views


def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        username = data['username']
        pswd = data['pswd']
        user = authenticate(request, username=username, password=pswd)
        if user is not None:
            login(request, user)
            return redirect('searcher:view_folder')
    context = {'form':form}
    return render(request, 'searcher/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('searcher:login')


@user_passes_test(lambda u: u.is_active and u.is_superuser, login_url=reverse_lazy('searcher:login'))
def view_folder(request, current_folder_id=None):
    current_folder_name = None
    if current_folder_id:
        current_folder_name = Folder.objects.get(id=current_folder_id).name
    folders = tupalize(Folder.objects.filter(parrent__id=current_folder_id), "folder_")
    files = tupalize(File.objects.filter(parrent__id=current_folder_id), "file_")
    add_folder_form = AddFolderForm(request.GET)
    add_file_form = AddFileForm(request.POST or None, request.FILES or None)
    delete_form = DeleteForm(request.POST or None, folders=folders, files=files)
    search_form = SearchForm(request.GET or None)
    breadcrumbs = list(reversed(get_breadcrumbs(current_folder_id)[1:]))
    context = {
        "folders":folders,
        "files":files,
        "add_folder_form":add_folder_form, 
        "add_file_form":add_file_form,
        "search_form":search_form,
        "delete_form":delete_form,
        "current_folder_id":current_folder_id,
        "current_folder_name":current_folder_name,
        "breadcrumbs":breadcrumbs,
        "MEDIA_URL":settings.MEDIA_URL,
    }
    add_folder(request, context)
    add_file(request, context)
    delete(request, context)
    return render(request, "searcher/view_folder.html", context)


@user_passes_test(lambda u: u.is_active and u.is_superuser, login_url=reverse_lazy('searcher:login'))
def change_folder(request, folder_id):
    folder = Folder.objects.get(id=folder_id)
    form = ChangeFolderForm(request.POST or None, folder=folder)
    if form.is_valid():
        new_name = form.cleaned_data["name"]
        new_tags = form.cleaned_data["tags"]
        folder.name = new_name
        folder.tags = new_tags
        folder.save()
        if folder.parrent:
            return redirect('searcher:view_folder', folder.parrent.id)
        else:
            return redirect('searcher:view_folder')
    context = {"form":form, "folder":folder}
    return render(request, "searcher/change_folder.html", context)


@user_passes_test(lambda u: u.is_active and u.is_superuser, login_url=reverse_lazy('searcher:login'))
def change_file(request, file_id):
    file = File.objects.get(id=file_id)
    form = ChangeFileForm(request.POST or None, file=file)
    if form.is_valid():
        new_tags = form.cleaned_data["tags"]
        file.tags = new_tags
        file.save()
        if file.parrent:
            return redirect('searcher:view_folder', file.parrent.id)
        else:
            return redirect('searcher:view_folder')
    context = {"form":form, "file":file}
    return render(request, "searcher/change_file.html", context)


@user_passes_test(lambda u: u.is_active and u.is_superuser, login_url=reverse_lazy('searcher:login'))
def search(request):
    search_form = SearchForm(request.GET or None)
    context = {"search_form":search_form, "MEDIA_URL":settings.MEDIA_URL}
    search = request.GET["search"]
    search_list = search.split()
    if search_list:
        folders = set(Folder.objects.filter(tags__icontains=search_list[0]))
        files = set(File.objects.filter(tags__icontains=search_list[0]))
        for word in search_list[1:]:
            folders.intersection_update(Folder.objects.filter(tags__icontains=word))
            files.intersection_update(File.objects.filter(tags__icontains=word))
        folders = tupalize(folders, "folder_")
        files = tupalize(files, "file_")
        context.update({"folders":folders, "files":files})
        return render(request, "searcher/search.html", context)
    else:
        folders = tupalize(Folder.objects.all(), "folder_")
        files = tupalize(File.objects.all(), "file_")
        context.update({"folders":folders, "files":files})
        return render(request, "searcher/search.html", context)



#--------------------------------------------------------------------------------------------------
# User views

def user_search(request):
    form = SearchForm(request.POST or None)
    context = {'form':form, "MEDIA_URL":settings.MEDIA_URL,}
    return render(request, 'searcher/user-search.html', context)


def search_ajax(request):
    if request.method == 'GET':
        search_text = request.GET.get('search_text')
        search_list = search_text.split()
        response_data = {}
        if search_list:
            folders = set(Folder.objects.filter(tags__icontains=search_list[0]))
            files = set(File.objects.filter(tags__icontains=search_list[0]))
            for word in search_list[1:]:
                folders.intersection_update(Folder.objects.filter(tags__icontains=word))
                files.intersection_update(File.objects.filter(tags__icontains=word))
            folders = [{'id':f.id, 'name':f.name} for f in folders]
            files = [{'id':f.id, 'name':f.get_proper_name()} for f in files]
            response_data.update({'folders':folders, 'files':files})
        return JsonResponse(response_data)
    else:
        return JsonResponse({})