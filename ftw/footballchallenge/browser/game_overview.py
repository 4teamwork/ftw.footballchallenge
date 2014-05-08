from zope.publisher.browser import BrowserView
from z3c.saconfig import named_scoped_session
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class GameOverview(BrowserView):
    """Defines a view for the league which displays the ranking."""
    
    template = ViewPageTemplateFile("game_overview.pt")

    def __call__(self):
        self.request['disable_plone.leftcolumn'] = True
        self.request['disable_plone.rightcolumn'] = True
        return self.template()

    def get_gameinfos(self):
        context = self.context
        home = context.nation1.name
        visitor = context.nation2.name
        goals = []
        for goal in context.goals:
            goals.append(goal.player.name)
        cards = []
        for card in context.cards:
            cards.append(card.player.name)
        saves = []
        for save in context.saves:
            saves.append(save.player.name)
        
        infos = {'home': home,
                 'visitor':visitor,
                 'goals':goals,
                 'cards':cards,
                 'saves':saves}
        
        return infos