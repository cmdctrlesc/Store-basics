from django.core.management.base import BaseCommand, CommandError
from mainapp.models import Record, Song
from urllib.request import urlopen
import json


class Command(BaseCommand):

    help = 'add tracklists to db'

    def add_arguments(self, parser):
        parser.add_argument("start_of_chunk", type=int)

        parser.add_argument("len_of_chunk", type=int)

    def handle(self, *args, **options):
        start_of_chunk = options["start_of_chunk"]
        len_of_chunk = options["len_of_chunk"]

        def addtodb(start_of_chunk, len_of_chunk):

            allrecords = Record.objects.all()
            chunkofrecords = allrecords[start_of_chunk:len_of_chunk]
            for record in chunkofrecords:
                recordid = record.recordid
                pk = record.id
                num = recordid.replace(" ", "%20")
                url = f"https://api.discogs.com/database/search?q={num}&token=RyFRgAKgOTEcuEcnBbdksysexuKFoGIbyYHVlvFs"
                response = urlopen(url)
                data = json.loads(response.read())
                results = data['results']
                if not results:
                    pass
                else:
                    results1 = (results[0])
                    if not results1:
                        pass
                    else:
                        # print(results1)
                        masterurl = results1['master_url']
                        if not masterurl:
                            pass
                        else:
                            response = urlopen(masterurl)
                            data = json.loads(response.read())
                            tracklist = data['tracklist']
                            for track in tracklist:
                                song = Song.objects.create(record_id=pk, position=(
                                    track['position']), name=(track['title']), duration=(track['duration']))

        addtodb(start_of_chunk, len_of_chunk)
