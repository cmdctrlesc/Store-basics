from django.core.management.base import BaseCommand, CommandError
from mainapp.models import Record
from django.core.files.base import ContentFile
from django.core.files import File
from urllib.request import urlparse
import requests
from django.template.defaultfilters import slugify


class Command(BaseCommand):

    help = 'create objects in db using pandas'

    def add_arguments(self, parser):
        parser.add_argument("start_of_chunk", type=int)

        parser.add_argument("len_of_chunk", type=int)

    def handle(self, *args, **options):
        start_of_chunk = options["start_of_chunk"]
        len_of_chunk = options["len_of_chunk"]

        def uploadphotos(start_of_chunk, len_of_chunk):

            queryset = Record.objects.all()[start_of_chunk:len_of_chunk]
            for obj in queryset:
                if not obj.coverimage:
                    if obj.discogspicurl == "image not found":
                        pass
                    else:
                        img_url = obj.discogspicurl
                        name = urlparse(img_url).path.split('/')[-1]
                        response = requests.get(img_url)
                        if response.status_code == 200:
                            obj.coverimage.save(name, ContentFile(
                                response.content), save=True)
                else:
                    pass

                obj.slug = '-'.join((slugify(obj.artist.name),
                                     slugify(obj.title)))
                obj.save()

        uploadphotos(start_of_chunk, len_of_chunk)
