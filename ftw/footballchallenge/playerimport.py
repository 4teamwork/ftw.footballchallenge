from pyquery import PyQuery
import urllib2
from ftw.footballchallenge.nation import Nation
from ftw.footballchallenge.player import Player
import StringIO
from PIL import Image
from datetime import date
import time

def import_team(rootpage, session, event):
    """Imports multiple Players a time from a external Site.
       Currently only working with Transfermarkt.ch

    """
    for page in rootpage:
        query = PyQuery(url=page)
        content = query("#content")
        Nationname = content("table.tabelle_spieler a#vereinsinfo").text()
        existing_nation = session.query(Nation).filter(Nation.name==Nationname).first()
        if existing_nation:
            nation_id = existing_nation.id_
        else:
            nation = Nation(Nationname)
            session.add(nation)
            nation_id = session.query(Nation).filter(Nation.name==Nationname).first().id_
        playertable = content("table#spieler")
        playerlist = playertable("tbody:first")
        for item in playerlist("tbody > tr"):
            name = PyQuery(item)("a.fb:first").text()
            link = PyQuery(item)("a.fb:first").attr("href")
            link = "http://www.transfermarkt.ch" + link
            playerpage = PyQuery(url=link)
            clubname = playerpage("table.tabelle_spieler img:first").attr('title')
            original_name = playerpage("table.tabelle_spieler.s10 tr").eq(0)("td:last").text()
            date_of_birth = playerpage("table.tabelle_spieler.s10 tr").eq(1)("td:last").text()
            age = playerpage("table.tabelle_spieler.s10 tr").eq(3)("td:last").text()
            size = playerpage("table.tabelle_spieler.s10 tr").eq(4)("td:last").text()
            size = size.replace(',','.')
            position = PyQuery(playerpage("table.tabelle_spieler.s10 tr")[6])("td:last").text()
            foot = playerpage("table.tabelle_spieler.s10 tr").eq(7)("td:last").text()
            value = playerpage("table.tabelle_spieler.s10 tr").eq(8)("td:last").text()
            img_src = playerpage("img.minifoto").attr("src")
            img = urllib2.urlopen(img_src).read()
            date_of_birth = date.fromtimestamp(time.mktime(time.strptime(date_of_birth, '%d.%m.%Y')))
            try:
                im = Image.open(StringIO.StringIO(img))
                im.verify()
            
            except Exception:
                img = None
            if not session.query(Player).filter(Player.name==name and Player.event.id_==event).all():
                player = Player(name, position, nation_id, original_name=original_name, date_of_birth=date_of_birth, age=age, foot=foot, value=value, size=size, club=clubname, image=img)
                session.add(player)
    session.commit()