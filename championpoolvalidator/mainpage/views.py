import os
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Champion, ChampionMastery
from .forms import RegionForm, SummonerNameForm
from django.shortcuts import redirect
import requests
import json

def home(request):

    if request.method == 'POST':

        template = loader.get_template('output.html')
        region_form = RegionForm(request.POST, prefix='region_form')
        summoner_name_form = SummonerNameForm(request.POST, prefix='summoner_name_form')
        region_form.is_valid()
        region_selected = region_form.cleaned_data.get('region')
        summoner_name_form.is_valid()
        summoner_name_typed = summoner_name_form.cleaned_data.get('name')
        return redirect(f'output/{region_selected}/{summoner_name_typed}')

    else:
        region_form = RegionForm(prefix='region_form')
        summoner_name_form = SummonerNameForm(prefix='summoner_name_form')

        context = {'region_form' : region_form, 'summoner_name_form': summoner_name_form }
    return render(request, 'home.html', context)



def output(request, region, summoner_name):

    path = os.path.join(os.path.dirname(__file__))
    with open(f'{path}/riot_api_key.txt') as file:
        api_key = file.read()
        
    response = requests.get(f'https://{region}1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}')
    data = json.loads(response.content.decode('utf-8'))
    summoner_id = data.get('id')
    mastery_response = requests.get(f'https://{region}1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}?api_key={api_key}')
    mastery_data = json.loads(mastery_response.content.decode('utf-8'))
    champion_masteries = []
    total_points = 0
    for data in mastery_data:
        points = data.get('championPoints')
        total_points += points
        champion = Champion.objects.get(pk=data.get('championId'))
        name = champion.name
        valid = champion.valid
        reason = champion.reason
        champion_mastery = ChampionMastery(name=name, valid=valid, reason=reason, points=points)
        champion_masteries.append(champion_mastery)
    
    unvalidated_percentage = 0
    unvalidated = []
    for champion_mastery in champion_masteries:
        champion_mastery.percentage = round((champion_mastery.points / total_points * 100), 2)
        print(f'Champion : {champion_mastery.name}, percentage : {champion_mastery.percentage}')
        if not champion_mastery.valid:
            unvalidated_percentage += champion_mastery.percentage
            unvalidated.append(champion_mastery)

    champion_masteries = sorted(champion_masteries, key=lambda x : x.percentage)
    validated_percentage = round(100 - unvalidated_percentage, 2)
    appreciations = ["public ennemy n°1", "literally the antechrist", "threat to society", "disgusting", "awful", "decent", "ok", "good", "very good", "angel"]
    index = round(validated_percentage / 10)
    appreciation = appreciations[index]
    if validated_percentage < 50:
        return render(request, 'failed.html', context={'champions': champion_masteries, 'unvalidated': unvalidated, 'validated_percentage': validated_percentage, 'appreciation': appreciation})
    
    return render(request, 'passed.html', context={'champions': champion_masteries, 'unvalidated': unvalidated, 'validated_percentage': validated_percentage, 'appreciation': appreciation})