from PIL import Image
from datetime import date
from ftw.footballchallenge.config import COUNTRY_CODE_MAPPING
from ftw.footballchallenge.config import POSITION_MAPPING
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.player import Player
from pyquery import PyQuery
import StringIO
import re
import requests
import requests_cache
import time


def import_team(rootpage, session, event):
    """Imports multiple Players a time from a external Site.
       Currently only working with Transfermarkt.ch

    """
    headers = {'User-agent': 'Mozilla/5.0'}
    requests_cache.install_cache('transfermarkt_cache',
                                 backend='sqlite',
                                 expire_after=None)
    club_league_mapping = {}
    for page in rootpage:
        resp = requests.get(page, headers=headers)
        nationpage = PyQuery(resp.content.decode('utf8'))
        nation_name = nationpage(".spielername-profil").text()
        country_code = COUNTRY_CODE_MAPPING[nation_name]
        fifa_rank = nationpage(".profilheader a[title=Weltrangliste]").text()
        coach = nationpage(
            ".mitarbeiterVereinSlider .container-hauptinfo a").eq(0).text()

        # Lookup nation
        nation = session.query(Nation).filter(
            Nation.country == country_code).first()
        # Create a new nation if we didn't find one
        if nation is None:
            nation = Nation(nation_name, event, country_code)
            nation.country = country_code
            nation.fifa_rank = int(re.sub("\D", "", fifa_rank))
            nation.coach = coach
            session.add(nation)

        playertable = nationpage("table.items")
        for item in playertable("tbody > tr"):
            name = PyQuery(item)(".spielprofil_tooltip").text()
            link = PyQuery(item)(".spielprofil_tooltip").attr("href")
            link = "http://www.transfermarkt.ch" + link
            resp = requests.get(link, headers=headers)
            playerpage = PyQuery(resp.content.decode('utf8'))

            player_data_trs = playerpage(
                ".box-personeninfos table.profilheader tr, "
                ".spielerdaten table.auflistung tr")
            player_data = {}
            for tr in player_data_trs:
                key = ' '.join(PyQuery(tr)("th").text().split())
                value = ' '.join(PyQuery(tr)("td").text().split())
                player_data[key] = value

            img_src = playerpage(".headerfoto > img").attr("src")
            if img_src:
                img = requests.get(img_src, headers=headers).content
                try:
                    im = Image.open(StringIO.StringIO(img))
                    im.verify()
                except Exception:
                    img = None
            else:
                img = None

            # Club and league lookup if necessary
            club = player_data.get('Aktueller Verein:')
            if club not in club_league_mapping:
                club_url = playerpage(
                    ".box-personeninfos th:contains('Aktueller Verein')"
                ).nextAll()("a").attr("href")
                club_url = "http://www.transfermarkt.ch" + club_url
                resp = requests.get(club_url, headers=headers)
                club_page = PyQuery(resp.content)
                club_data_trs = club_page(
                    ".box-personeninfos table.profilheader tr")
                club_data = {}
                for tr in club_data_trs:
                    key = ' '.join(PyQuery(tr)("th").text().split())
                    value = ' '.join(PyQuery(tr)("td").text().split())
                    club_data[key] = value
                club_league_mapping[club] = ['Wettbewerb:']

            # Conversions
            position = POSITION_MAPPING.get(player_data.get('Position:'))

            market_value = player_data.get('Marktwert:')
            if 'Mio.' in market_value:
                market_value = int(re.sub("\D", "", market_value)) * 10000

            size = player_data.get(u'Gr\xf6\xdfe:', '0.00').replace(
                ',', '.').split()[0]

            date_of_birth = date.fromtimestamp(time.mktime(time.strptime(
                player_data.get('Geburtsdatum:'), '%d.%m.%Y')))

            # Lookup player
            player = session.query(Player).filter(
                Player.name == name and Player.nation_id == nation.id_).first()
            # Create a new player if we didn't find one.
            if player is None:
                player = Player(name, position, nation.id_, event)
                session.add(player)
            # Set/update player properties
            player.original_name = player_data.get('Name im Heimatland:')
            player.date_of_birth = date_of_birth
            player.age = int(player_data.get('Alter:'))
            player.foot = player_data.get(u'Fu\xdf:')
            player.value = value
            player.size = size
            player.club = player_data.get('Aktueller Verein:')
            player.league = club_league_mapping[club]
            player.image = img

    requests_cache.uninstall_cache()
