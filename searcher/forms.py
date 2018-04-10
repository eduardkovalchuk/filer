from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Користувач", max_length=300)
    pswd = forms.CharField(label="Пароль", widget=forms.PasswordInput())


class AddFolderForm(forms.Form):
    name = forms.CharField(label="Назва", max_length=300)
    tags = forms.CharField(label="Теги", widget=forms.Textarea, required=False)


class AddFileForm(forms.Form):
    """
    Add file form
    """
    file = forms.FileField()
    tags = forms.CharField(label="Теги", widget=forms.Textarea, required=False)


class DeleteForm(forms.Form):
    """
    Delete form
    """
    def __init__(self, *args, **kwargs):
        folders = kwargs.pop('folders')
        files = kwargs.pop('files')
        super(DeleteForm, self).__init__(*args, **kwargs)
        for folder, folder_field in folders:
            self.fields[folder_field] = forms.BooleanField(required=False)
        for file_, file_field in files:
            self.fields[file_field] = forms.BooleanField(required=False)


class SearchForm(forms.Form):
    search = forms.CharField(
        max_length=300, 
        widget=forms.TextInput(attrs={'id':'search-text', 'placeholder': 'Пошук...', 'required': False,})
        )


class ChangeFolderForm(forms.Form):

    def __init__(self, *args, **kwargs):
        folder = kwargs.pop("folder")
        super(ChangeFolderForm, self).__init__(*args, **kwargs)
        self.fields["name"] = forms.CharField(label="Назва", initial=folder.name)
        self.fields["tags"] = forms.CharField(label="Теги", widget=forms.Textarea, required=False, initial=folder.tags)

class ChangeFileForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        file = kwargs.pop("file")
        super(ChangeFileForm, self).__init__(*args, **kwargs)
        self.fields["tags"] = forms.CharField(label="Теги", widget=forms.Textarea, required=False, initial=file.tags)