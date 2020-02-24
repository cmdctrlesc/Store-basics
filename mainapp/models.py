from django.db import models
from django.urls import reverse


class Record(models.Model):
    recordid = models.CharField(max_length=100, default="recordid")
    artist = models.ForeignKey(
        'Artist', on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(max_length=700, default="title")
    barcode = models.CharField(max_length=100, default="barcode")
    unit = models.CharField(max_length=100, default="unit")
    recordformat = models.CharField(max_length=100, default="recordformat")
    label = models.ForeignKey(
        'Label', on_delete=models.PROTECT, null=True, blank=True)
    price = models.CharField(max_length=100, default="price")
    precision = models.CharField(max_length=100, default="precision")
    delivery = models.CharField(max_length=100, default="delivery")
    stock = models.CharField(max_length=100, default="stock")
    date = models.CharField(max_length=100, default="date")

    wikiinfo = models.TextField(default="wikiinfo")
    wikilink = models.CharField(max_length=500, default="wikilink")
    discogspicurl = models.CharField(max_length=500, default="discogpicurl")
    ytlink = models.CharField(max_length=500, default="ytlink")
    coverimage = models.ImageField(
        blank=True, null=True, upload_to='coverimages/')
    slug = models.SlugField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('mainapp:product_detail', kwargs={'slug': self.slug})


class Label(models.Model):
    name = models.CharField(max_length=700, default="name")
    wikiinfo = models.TextField(default="wikiinfo")
    wikiinfolink = models.CharField(max_length=700, default="wikiinfolink")


class Artist(models.Model):
    name = models.CharField(max_length=700, default="name")
    wikiinfo = models.TextField(default="wikiinfo")
    wikiinfolink = models.CharField(max_length=700, default="wikiinfolink")


class Song(models.Model):
    record = models.ForeignKey(
        'Record', on_delete=models.CASCADE, null=True)
    position = models.CharField(
        max_length=100, default="position", null=True)
    name = models.CharField(
        max_length=800, default="songname", null=True)
    duration = models.CharField(
        max_length=100, default="position", null=True)
