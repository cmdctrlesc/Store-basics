from django.shortcuts import render, get_object_or_404
from mainapp.models import Record, Artist, Label, Song
from cartapp.forms import CartAddProductForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from urllib.parse import urlencode
from django.shortcuts import redirect


def mainview(request):

    allrecords = Record.objects.all()[0:10]

    return render(request, "mainapp/searchpage.html", {"allrecords": allrecords})


def product_detail(request, slug):
    record = get_object_or_404(Record, slug=slug)
    cart_product_form = CartAddProductForm()
    artist = record.artist
    products_from_artist = Record.objects.filter(
        artist=artist).exclude(slug=slug)
    products_from_artist1 = products_from_artist[0:3]
    label = record.label
    products_from_label = Record.objects.filter(label=label).exclude(slug=slug)
    products_from_label1 = products_from_label[0:3]
    request.session['artist'] = artist.name
    request.session['label'] = label.name
    songs = Song.objects.filter(record=record)

    context = {'record': record,
               'cart_product_form': cart_product_form, 'products_from_artist': products_from_artist, 'products_from_artist1': products_from_artist1, 'products_from_label': products_from_label, 'products_from_label1': products_from_label1, 'songs': songs}
    return render(request, 'mainapp/detail.html', context)


def search(request):

    query = request.GET.get('q')
    if "everything" in request.GET:
        base_url = reverse('mainapp:everythingsearch')
        query_string = urlencode({'query': query})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)

    elif "albumtitles" in request.GET:
        base_url = reverse('mainapp:albumsearch')
        query_string = urlencode({'query': query})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)

    if "artistnames" in request.GET:
        base_url = reverse('mainapp:artistsearch')
        query_string = urlencode({'query': query})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)

    if "recordlabels" in request.GET:
        base_url = reverse('mainapp:recordlabelsearch')
        query_string = urlencode({'query': query})
        url = '{}?{}'.format(base_url, query_string)
        return redirect(url)


def everythingsearch(request):

    query = request.GET.get('query')
    qs = Record.objects.filter(Q(wikiinfo__icontains=query) | Q(
        label__wikiinfo__icontains=query) | Q(artist__wikiinfo__icontains=query))

    allresults = qs.order_by('pk')

    paginator = Paginator(allresults, 10)
    page = request.GET.get('page')

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    context = {'results': results, 'query': query}

    return render(request, 'mainapp/everythingsearch.html', context)


def albumsearch(request):

    query = request.GET.get('query')
    qs = Record.objects.filter(Q(title__icontains=query))

    allresults = qs.order_by('pk')

    paginator = Paginator(allresults, 10)
    page = request.GET.get('page')

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    context = {'results': results, 'query': query}

    return render(request, 'mainapp/albumsearch.html', context)


def artistsearch(request):

    query = request.GET.get('query')
    qs = Artist.objects.filter(Q(name__icontains=query))

    allresults = qs.order_by('pk')
    print(allresults)

    paginator = Paginator(allresults, 5)
    page = request.GET.get('page')

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    context = {'results': results, 'query': query}
    # print(context)

    return render(request, 'mainapp/artistsearch.html', context)


def recordlabelsearch(request):

    query = request.GET.get('query')
    qs = Label.objects.filter(Q(name__icontains=query))

    allresults = qs.order_by('pk')

    paginator = Paginator(allresults, 5)
    page = request.GET.get('page')

    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    context = {'results': results, 'query': query}

    return render(request, 'mainapp/labelsearch.html', context)


def seeallfromartist(request):

    artist = request.session['artist']
    allfromartist = Record.objects.filter(artist=artist)

    return render(request, 'mainapp/seeall.html', {'allfromartist': queryset, 'title': artist})


def seeallfromlabel(request):

    label = request.session['label']
    allfromlabel = Record.objects.filter(label__name=label)

    return render(request, 'mainapp/seeall.html', {'queryset': allfromlabel, 'title': label})
