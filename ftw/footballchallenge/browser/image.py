from zope.publisher.browser import BrowserView


class PlayerImage(BrowserView):
    
    def __call__(self):
        self.request.response.setHeader('Content-Type', 'image/jpeg')
        self.request.response.write(self.context.image)