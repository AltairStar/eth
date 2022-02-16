from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from . models import Eth


def index(request):
    URL = 'https://etherscan.io/accounts/1?ps=100'
    HEADERS = {
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36",
        "accept": "*/*"}

    r = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(r.text, 'html.parser')
    addresses = soup.find_all('a')
    ad = []
    balance = []

    for i in range(58, len(addresses) - 26):
        ad.append(addresses[i].text)

    for i in range(len(ad)):
        URLs = 'https://etherscan.io/address/%s' % ad[i]
        HEADERS = {
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36",
            "accept": "*/*"}
        s = requests.get(URLs, headers=HEADERS)
        ssoup = BeautifulSoup(s.text, 'html.parser')
        str = ""
        for j in range(len(ssoup.find('div', {"class": "col-md-8"}).text)):
            if ssoup.find('div', {"class": "col-md-8"}).text[j] == '.' or ssoup.find('div', {"class": "col-md-8"}).text[j] == 'E':
                balance.append(str)
                break
            str = str + ssoup.find('div', {"class": "col-md-8"}).text[j]
    for i in range(len(balance)):
        balance[i] = balance[i].replace(',', '')
        balance[i] = int(balance[i])

    return render(request, 'base/base.html', ads=ad, balances=balance)
