from django import template
from mainapp.models import Record

register = template.Library()


# @register.filter
# def by_artist(allrecords, artist):
#     return allrecords.filter(title=artist)


@register.simple_tag
def get_records_artist(artist):

    return (Record.objects.filter(artist__name=artist)[0:3])


@register.simple_tag
def get_records_label(label):

    return (Record.objects.filter(label__name=label)[0:3])


@register.simple_tag
def get_songs(record):

    return (Song.objects.filter(song_record=record))
