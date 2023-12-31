from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
import random
from collection.models import Artwork, Collection
from django.contrib.postgres import search
from django.core.paginator import Paginator
from .forms import CollectionForm
from django.template.loader import render_to_string


def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            username = f.cleaned_data.get('username')
            raw_password = f.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect('/')

    else:
        f = UserCreationForm()

    return render(request, 'registration/registration_form.html', {'form': f})


def artwork(request, artwork_id):
    artwork = Artwork.objects.get(pk=artwork_id)
    return render(request, 'collection/artwork.html', {'artwork': artwork})


def collections(request):
    collections = Collection.objects.filter(owner=request.user)
    return render(request, 'collection/collections.html',
                  {'collections': collections})


def collection_list(request):
    collections = Collection.objects.filter(owner=request.user)
    print("a)")
    return render(request, 'collection/collection_list.html',
                  {'collections': collections})


def collection_add(request):
    form = None
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            collection = Collection(
                name=name,
                description=description,
                owner=request.user
            )
            collection.save()

            # Devolver el HTML actualizado de la lista de colecciones
            collections = Collection.objects.filter(owner=request.user)
            html = render_to_string('collection/collection_list.html', {'collections': collections})
            return HttpResponse(html, status=200)

    return render(request, 'collection/collection_form.html', {'form': form})


def index(request):
    artworks = list(Artwork.objects.all())
    random_works = []
    if artworks:
        random_works = random.sample(artworks, 4)
    print(random_works)
    return render(request, 'collection/index.html', {'artworks': random_works})


def random_artworks(request):
    artworks = list(Artwork.objects.all())
    random_works = []
    if artworks:
        random_works = random.sample(artworks, 4)
    return render(request, 'collection/artworks_random.html',
                  {'artworks': random_works})


def search_artworks(request):
    if request.method == 'GET':
        value = request.GET['search']
        artworks = ft_artworks(value)

        paginator = Paginator(artworks, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, 'collection/artwork_search.html',
                      {'artworks': artworks, 'search_value': value,
                       "page_obj": page_obj})
    else:
        return render(request, 'collection/index.html',
                      {'artworks': [], 'search_value': None})


def ft_artworks(value):
    vector = (
        search.SearchVector("title", weight="A")
        + search.SearchVector("author__name", weight="B")
        + search.SearchVector("style__name", weight="C")
        + search.SearchVector("genre__name", weight="C")
    )
    query = search.SearchQuery(value, search_type="websearch")
    return (
        Artwork.objects.annotate(
            search=vector,
            rank=search.SearchRank(vector, query),
        )
        .filter(search=query)
        .order_by("-rank")
    )


def artwork_add(value, artwork_id):
    collections = Collection.objects.filter(owner=value.user)    
    return render(value, 'collection/artwork_add.html', {'collections': collections, "artwork": artwork_id})

def artwork_add_collection(value, collection, artwork_id):
    collections = Collection.objects.filter(owner=value.user)
    for c in collections:
        if c.name == collection:
            c.artworks.add(artwork_id)
    return HttpResponse(status=204)

def show_collection(value, name):
    collection = Collection.objects.filter(owner=value.user)
    for c in collection:
        if c.name == name:
            artworks = list(c.artworks.all())
            print(artwork)
    return render(value, 'collection/collection_show.html', {'name':name, "artworks": artworks})

def collection_delete(value,name):
    collection = Collection.objects.filter(owner=value.user)
    for c in collection:
        if c.name == name:
            c.delete()
    return HttpResponse(status=204, headers={'HX-Trigger': 'listChanged'})