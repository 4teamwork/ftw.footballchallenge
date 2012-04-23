from pyquery import PyQuery
import urllib2
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.player import Player
import StringIO
from PIL import Image
from datetime import date
import time
from ftw.footballchallenge.config import POSITION_MAPPING
from ftw.footballchallenge.config import COUNTRY_CODE_MAPPING


def import_team(rootpage, session, event):
    """Imports multiple Players a time from a external Site.
       Currently only working with Transfermarkt.ch

    """
    for page in rootpage:
        f = urllib2.urlopen(page)
        nationpage = f.read()
        nationpage = PyQuery(nationpage.decode('utf8'))
        content = nationpage("#content")
        nation_name = content("table.tabelle_spieler a#vereinsinfo").text()
        country_code = COUNTRY_CODE_MAPPING[nation_name]

        # Lookup nation
        nation = session.query(Nation).filter(
            Nation.country==country_code).first()
        # Create a new nation if we didn't find one
        if nation is None:
            nation = Nation(nation_name)
            nation.country = country_code
            session.add(nation)

        playertable = content("table#spieler")
        playerlist = playertable("tbody:first")
        for item in playerlist("tbody > tr"):
            name = PyQuery(item)("a.fb:first").text()
            link = PyQuery(item)("a.fb:first").attr("href")
            link = "http://www.transfermarkt.ch" + link
            f = urllib2.urlopen(link)
            playerpage = f.read()
            playerpage = PyQuery(playerpage.decode('utf8'))
            clubname = playerpage(
                "table.tabelle_spieler img:first").attr('title')
            league = playerpage(
                "table.tabelle_spieler tr").eq(1)("a").eq(1).text()

            tds = [PyQuery(td) for td in playerpage(
                   "table.tabelle_spieler.s10 td")]
            player_props = dict([(k.text(), v.text()) for k,v in zip(
                                 tds[::2], tds[1::2])])

            img_src = playerpage("img.minifoto").attr("src")
            img = urllib2.urlopen(img_src).read()
            try:
                im = Image.open(StringIO.StringIO(img))
                im.verify()
            except Exception:
                img = None

            # Conversions
            position = POSITION_MAPPING.get(player_props.get('Position:'))
            value = int(player_props.get('Marktwert:').split()[0].replace(
                '.', ''))
            size = player_props.get(u'Gr\xf6\xdfe:').replace(',', '.')
            date_of_birth = date.fromtimestamp(time.mktime(time.strptime(
                player_props.get('Geburtsdatum:'), '%d.%m.%Y')))

            # Lookup player
            player = session.query(Player).filter(
                Player.name==name and Player.nation_id==nation.id_).first()
            # Create a new player if we didn't find one.
            if player is None:
                player = Player(name, position, nation.id_, event)
                session.add(player)
            # Set/update player properties
            player.original_name = player_props.get('Name im Heimatland:')
            player.date_of_birth = date_of_birth
            player.age = player_props.get('Alter:')
            player.foot = player_props.get(u'Fu\xdf:')
            player.value = value
            player.size = size
            player.club = clubname
            player.league = league
            player.image = img
