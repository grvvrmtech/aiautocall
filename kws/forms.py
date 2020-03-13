from django import forms

class SearchKeyWordForm(forms.Form):
    #keywords = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter keyword'}))
    keywords = forms.CharField(max_length=500) # widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter keyword'}))

class KeyWordForm(forms.Form):
    #keywords = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter keyword'}))
    keywords = forms.CharField(max_length=500)# widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter keyword'}))
    file_field = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': 'True'}))
