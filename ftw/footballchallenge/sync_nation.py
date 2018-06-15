from datetime import date
from ftw.footballchallenge.config import COUNTRY_CODE_MAPPING
from ftw.footballchallenge.config import MULTIPLIER_MAPPING
from ftw.footballchallenge.config import POSITION_MAPPING
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.player import Player
from PIL import Image
from pyquery import PyQuery
from requests.exceptions import RequestException
from z3c.saconfig import named_scoped_session
import logging
import requests
import requests_cache
import StringIO
import time


logger = logging.getLogger('ftw.footballchallenge')

requests_cache.install_cache('transfermarkt_cache')


def sync_nation(url, event):
    """Imports multiple Players a time from a external Site.
       Currently only working with Transfermarkt.ch

    """
    session = named_scoped_session('footballchallenge')
    headers = {'User-agent': 'Mozilla/5.0'}

    try:
        f = requests.get(url, headers=headers)
    except RequestException as exc:
        logger.warning('Could not fetch url %s. %r', url, exc)
        return

    nationpage = f.content
    nationpage = PyQuery(nationpage.decode('utf8'))
    content = nationpage("#main")
    nation_name = content('.dataMain h1').text()
    country_code = COUNTRY_CODE_MAPPING[nation_name]

    # Lookup nation
    nation = session.query(Nation).filter(
        Nation.country == country_code).first()

    if nation is None:
        return

    player_ids = set()
    playertable = content("table.items")
    playerlist = playertable("tbody")
    for item in playerlist("tbody > tr"):
        name = PyQuery(item)(".hide-for-small a.spielprofil_tooltip").text()
        link = PyQuery(item)(".hide-for-small a.spielprofil_tooltip").attr("href")
        link = "https://www.transfermarkt.ch" + link
        f = requests.get(link, headers=headers)
        playerpage = PyQuery(f.content.decode('utf8'))
        clubname = playerpage(".dataZusatzDaten .hauptpunkt .vereinprofil_tooltip").text()
        league = playerpage(".dataZusatzDaten .mediumpunkt a").text()

        data_items = playerpage(".dataContent p")
        player_props = dict([
            (k.text(), v.text()) for k, v
            in zip(data_items('.dataItem').items(), data_items('.dataValue').items())])

        img_src = playerpage('.dataBild img').attr('src')
        try:
            img = requests.get(img_src, headers=headers).content
        except RequestException as exc:
            logger.warning('Could not fetch image with from %s. %r', img_src, exc)
            img = None
        if img is not None:
            try:
                im = Image.open(StringIO.StringIO(img))
                im.verify()
            except Exception:
                img = None

        # Conversions
        position = POSITION_MAPPING.get(player_props.get('Position:'))

        # Marktwert
        value_data = playerpage('.dataMarktwert').text()
        if value_data:
            value = value_data.split()[0]
            multiplier = MULTIPLIER_MAPPING.get(value_data.split()[1], 1)
            if ',' in value:
                value = int(value.split(',')[0]) * multiplier + int(value.split(',')[1]) * multiplier * 0.01
            else:
                value = int(value) * multiplier
        else:
            value = 0

        size = player_props.get(u'Gr\xf6\xdfe:', '0.00').replace(',', '.')
        if size.endswith(' m'):
            size = size[:-2]
        date_of_birth = date.fromtimestamp(time.mktime(time.strptime(
            player_props.get('Geb./Alter:').split()[0], '%d.%m.%Y')))

        # Lookup player
        player = session.query(Player).filter(
            Player.name == name and Player.nation_id == nation.id_).first()

        # Create a new player if we didn't find one.
        if player is None:
            player = Player(name, position, nation.id_, event)
            session.add(player)
            logger.info('Adding player %s' % name)
            session.flush()

        player_ids.add(player.id_)

        # Set/update player properties
        player.original_name = player_props.get('Name im Heimatland:')
        player.date_of_birth = date_of_birth
        player.age = int(player_props.get('Geb./Alter:').split()[1].strip('()'))
        #player.foot = player_props.get(u'Fu\xdf:')
        player.value = value
        player.size = size
        player.club = clubname
        player.league = league
        player.image = img

    player_ids_in_db = session.query(Player.id_).filter(Player.nation_id == nation.id_).all()
    player_ids_in_db = set([pid[0] for pid in player_ids_in_db])
    delete_ids = player_ids_in_db - player_ids
    for player_id in delete_ids:
        player = session.query(Player).filter(Player.id_ == player_id).one()
        logger.info('Removing player %s, id=%s' % (player.name, player_id))
        session.delete(player)