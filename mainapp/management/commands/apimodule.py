from urllib.request import urlopen
import json
import string


def createlistofwords(mystring):

    listofwords = (mystring.translate(str.maketrans(
        string.punctuation, ' '*len(string.punctuation)))).split()

    return listofwords


def wikiartistsearch(artist_lst):
    artistdescriptions = []
    artistlinks = []

    list_of_words = ["band", "musician", "singer",
                     "singer-songwriter", "producer", "group", "duo"]

    for artist in artist_lst:

        if artist == "VARIOUS ARTISTS" or artist == "VA" or artist == "OST" or artist == "V.A.":
            artistdescriptions.append("not found")
            artistlinks.append("not found")

        else:

            try:
                newartistlist = createlistofwords(artist)
                if "," in artist:
                    artistlist = (artist.replace(",", " ")).split()
                    artistlist2 = artistlist.reverse()
                    artisttosearch = " ".join(artistlist)
                else:
                    artisttosearch = artist

                artistquery = artisttosearch.replace(" ", "%20")
                url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={artistquery}&namespace=0&format=json"
                response = urlopen(url)
                results = json.loads(response.read())
                descriptionlist = results[2]
                if not descriptionlist:
                    artistdescriptions.append("not found")
                    artistlinks.append("not found")

                else:

                    if [description for description in descriptionlist if any(x in description for x in list_of_words) and all(y in description.upper() for y in newartistlist)]:

                        for description in descriptionlist:
                            if any(x in description for x in list_of_words) and all(y in description.upper() for y in newartistlist):
                                artistdescriptions.append(
                                    description)
                                descriptionindex = descriptionlist.index(
                                    description)
                                link = (results[3])[
                                    descriptionindex]
                                artistlinks.append(link)
                                break

                            else:
                                pass

                    else:
                        artistdescriptions.append("not found")
                        artistlinks.append("not found")

            except:
                artistdescriptions.append("not found")
                artistlinks.append("not found")

    return artistdescriptions, artistlinks


def wikititlesearch(title_lst, artist_lst):

    titledescriptions = []
    titlelinks = []

    list_of_words = ["album"]

    for title, artist in zip(title_lst, artist_lst):

        newartistlist = createlistofwords(artist)

        newtitlelist = createlistofwords(title)

        try:

            titlequery = title.replace(" ", "%20")
            url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={titlequery}&namespace=0&format=json"
            response = urlopen(url)
            results = json.loads(response.read())
            descriptionlist = results[2]
            if not descriptionlist:
                titledescriptions.append("not found")
                titlelinks.append("not found")

            else:

                if [description for description in descriptionlist if any(x in description for x in list_of_words) and all(y in description.upper() for y in newartistlist) and all(z in description.upper() for z in newtitlelist)]:
                    for description in descriptionlist:
                        if any(x in description for x in list_of_words) and all(y in description.upper() for y in newartistlist) and all((z in description.upper() for z in newtitlelist)):

                            titledescriptions.append(description)
                            descriptionindex = descriptionlist.index(
                                description)
                            link = (results[3])[descriptionindex]
                            titlelinks.append(link)

                            break

                else:
                    titledescriptions.append("not found")
                    titlelinks.append("not found")

        except:
            titledescriptions.append("not found")
            titlelinks.append("not found")

    return titledescriptions, titlelinks


def wikilabelsearch(label_lst):
    labeldescriptions = []
    labellinks = []

    list_of_words = ["label", "records"]

    for label in label_lst:

        try:

            labelquery = label.replace(" ", "%20")
            url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={labelquery}&namespace=0&format=json"
            response = urlopen(url)
            results = json.loads(response.read())
            descriptionlist = results[2]

            if not descriptionlist:
                labeldescriptions.append("not found")
                labellinks.append("not found")

            else:

                if [description for description in descriptionlist if any(x in description for x in list_of_words)]:

                    for description in descriptionlist:
                        if any(x in description for x in list_of_words):
                            labeldescriptions.append(description)
                            descriptionindex = descriptionlist.index(
                                description)
                            link = (results[3])[descriptionindex]
                            labellinks.append(link)
                            break
                else:
                    labeldescriptions.append("not found")
                    labellinks.append("not found")

        except:
            labeldescriptions.append("not found")
            labellinks.append("not found")

    return labeldescriptions, labellinks


def discogspicsearch(artist_lst, title_lst, id_lst, ean_lst):

    imageurls = []
    for artist, title, idnum, ean in zip(artist_lst, title_lst, id_lst, ean_lst):

        try:
            num = idnum.replace(" ", "%20")
            url = f"https://api.discogs.com/database/search?q={num}&token=RyFRgAKgOTEcuEcnBbdksysexuKFoGIbyYHVlvFs"
            response = urlopen(url)
            data = json.loads(response.read())
            results = data['results']

            if not results:
                url = f"https://api.discogs.com/database/search?q={ean}&token=RyFRgAKgOTEcuEcnBbdksysexuKFoGIbyYHVlvFs"
                response = urlopen(url)
                data = json.loads(response.read())
                results = data['results']
                results1 = (results[0])
                imageurl = results1['cover_image']
                imageurls.append(imageurl)

                if not results:

                    name = artist_name + album_name
                    album = name.replace(" ", "%20")
                    url = f"https://api.discogs.com/database/search?q={album}&token=RyFRgAKgOTEcuEcnBbdksysexuKFoGIbyYHVlvFs"
                    response = urlopen(url)
                    data = json.loads(response.read())
                    results = data['results']
                    results1 = (results[0])
                    imageurl = results1['cover_image']
                    imageurls.append(imageurl)

                    if not results:
                        imageurls.append("image not found")
            else:
                results1 = (results[0])
                imageurl = results1['cover_image']
                imageurls.append(imageurl)
        except:
            imageurls.append("image not found")

    return imageurls


def youtubesearch(artist_lst, title_lst):
    apikey = "AIzaSyDatqiYfpBUVOiB1s_bLzuGrCtOBjwu7Jo"
    youtube_string = "www.youtube.com/watch?v="
    fullurls = []
    for artist, title in zip(artist_lst, title_lst):
        try:
            query = artist + " " + title
            ytquery = query.replace(" ", "%20")
            url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={ytquery}&type=video&key={apikey}"
            response = urlopen(url)
            results = json.loads(response.read())
            firstresult = ((results.get('items'))[0])
            videotitle = ((firstresult.get('snippet')).get('title'))

            newartistlist = createlistofwords(artist)

            if any(y in videotitle.upper() for y in newartistlist):
                videoid = ((firstresult.get('id')).get('videoId'))
                fullurls.append(youtube_string+videoid)

            else:
                fullurls.append("not found")

        except:
            fullurls.append("not found")

    return fullurls


if __name__ == "__main__":
    test = discogspicresearch(["SNAIL MAIL"], ["LUSH"], [
                              "OLE11791"], ["744861117919"])
    print(test)
