from django.forms import ModelForm, ChoiceField, TextInput
from .models import Region, SummonerName

class RegionForm(ModelForm):

    query =  Region.objects.all().values_list('name', flat=True)
    query_choices = [('', 'None')] + [(name, name) for name in query]
    region = ChoiceField(choices = query_choices)
    class Meta:
        model = Region
        fields = ['region']


class SummonerNameForm(ModelForm):

    summoner_name = TextInput()
    class Meta:
        model = SummonerName
        fields = ['name']
        
