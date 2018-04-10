import os, shutil
from django.db import models
from django.conf import settings
from django.dispatch import dispatcher


# Create your models here.
class Folder(models.Model):
    name = models.CharField(max_length=300)
    parrent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    tags = models.TextField(null=True)

    class Meta:
        verbose_name = 'Папка'
        verbose_name_plural = 'Папки'

    def __str__(self):
        return self.name

    def get_rel_path(self):
        path = ""
        current_folder = self.parrent
        while current_folder != None:
            path = current_folder.name + "/" + path
            current_folder = current_folder.parrent
        return "root" + "/" + path


class File(models.Model):
    parrent = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    upload = models.FileField(upload_to="files")
    tags = models.TextField(null=True)

    def get_rel_path(self):
        if self.parrent == None:
            return "root/"
        else:
            return self.parrent.get_rel_path() + self.parrent.name + "/"

    def get_proper_name(self):
        return self.upload.name.split("/")[-1]

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файли'
    
    def __str__(self):
        return self.upload.name
