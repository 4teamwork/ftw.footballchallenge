from zope.publisher.browser import BrowserView
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from PIL import Image
import StringIO


class PlayerView(BrowserView):
    """Defines a view for the league which displays the ranking."""

    template = ViewPageTemplateFile("player_view.pt")

    def __call__(self):
        self.request['disable_plone.leftcolumn'] = True
        self.request['disable_plone.rightcolumn'] = True
        self.context.Title = self.context.name
        return self.template()

        