import os, shutil
from django.db import models
from django.conf import settings
from django.dispatch import dispatcher
import datetime as dt


def get_file_path(instance, filename):
    return instance.get_rel_path() + "/" + instance.upload.name

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
    
    def get_abs_path(self):
        return settings.MEDIA_ROOT + self.get_rel_path()
    
    def real_create(self):
        directory = self.get_abs_path() + self.name + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def real_delete(self):
        directory = self.get_abs_path() + self.name + "/"
        shutil.rmtree(directory)


class File(models.Model):
    parrent = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    upload = models.FileField(upload_to=get_file_path)
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
