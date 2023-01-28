import math
import os
from django.shortcuts import render
from .models import Champion, ChampionMastery
from .forms import RegionForm, SummonerNameForm
from django.shortcuts import redirect
import requests
from django.middleware.csrf import get_token
import json
from django.core.exceptions import ObjectDoesNotExist 


def home(request):

    if request.method == 'POST':

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
    csrf_token = get_token(request)
    cookies = {'csrftoken': csrf_token}
    headers = {"X-CSRFToken": csrf_token}
    response = requests.get(f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}?api_key={api_key}', headers=headers, cookies=cookies)
    data = json.loads(response.content.decode('utf-8'))
    summoner_id = data.get('id')
    mastery_response = requests.get(f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{summoner_id}?api_key={api_key}')
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
    colors = ['#3F1453','#1E3C6E','#702403', '#2D93B2','#3E4167', '#30A2A9', '#E2933C', '#46F8CF', '#8EAE32', '#0A90BA', '#D58A1B', '#BBBA39', '#AC0717',
              '#DDAA71', '#FF32EC', '#20B4BE', '#2026EB', '#591984', '#437CC8', '#2AE3F7', '#7D36D8', '#FE5D8D', '#7185AD', '#54C5B2', '#DDD917']
    color_index = 0
    words = {}
    rest = 0
    for champion_mastery in champion_masteries:
        champion_mastery.percentage = round((champion_mastery.points / total_points * 100), 2)
        if not champion_mastery.valid and champion_mastery.percentage > 0.8:
            unvalidated_percentage += champion_mastery.percentage
            unvalidated.append(champion_mastery)
            data =  words.get(champion_mastery.reason)
            if data:
                data['percentage'] += champion_mastery.percentage
                data['champions'].append(champion_mastery.name)
            else:
                words[champion_mastery.reason] = {'percentage' : champion_mastery.percentage, 'color': colors[color_index], 'champions': [champion_mastery.name]}
                color_index += 1
        elif not champion_mastery.valid:
            rest += champion_mastery.percentage
    rest = round(rest, 2)
    normal = round(100 - unvalidated_percentage, 2)
    words['normal'] = {'percentage': normal, 'color': 'grey', 'champions': ['Respectable champions']}
    words['others'] = {'percentage': rest, 'color': 'black', 'champions': ['Other non-respectable champions']}
    champion_masteries = sorted(champion_masteries, key=lambda x : x.percentage)

    validated_percentage = round(100 - unvalidated_percentage, 2)
    appreciations = ["public ennemy n°1", "literally the antechrist", "threat to society", "disgusting", "awful", "decent", "ok", "good", "very good", "angel", "god"]
    index = math.floor(validated_percentage / 10)
    appreciation = appreciations[index]

    if validated_percentage < 50:
        return render(request, 'failed.html', context={'champions': champion_masteries, 'unvalidated': unvalidated, 'validated_percentage': validated_percentage, 'appreciation': appreciation, 'words': words})
    
    return render(request, 'passed.html', context={'champions': champion_masteries, 'unvalidated': unvalidated, 'validated_percentage': validated_percentage, 'appreciation': appreciation, 'words': words})
