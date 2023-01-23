from django.forms import ModelForm, ChoiceField, TextInput
from .models import Region, SummonerName

class RegionForm(ModelForm):

    query_choices = []
    region = ChoiceField(choices = query_choices)
    class Meta:
        model = Region
        fields = ['region']


class SummonerNameForm(ModelForm):

    summoner_name = TextInput()
    class Meta:
        model = SummonerName
        fields = ['name']
        
