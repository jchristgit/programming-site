import requests
from django.shortcuts import render


def index(request):
    widget_data = requests.get("https://canary.discordapp.com/api/guilds/181866934353133570/widget.json").json()
    online_members = len(widget_data['members'])
    context = {
        'online_members': online_members
    }
    return render(request, 'home/index.html', context)
