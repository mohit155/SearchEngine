from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(label='search_query', max_length=200)
