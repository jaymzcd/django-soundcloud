from radio.filebrowser_handler import FilebrowserImage


class ImageHandlerFactory(object):

    def __init__(self, url, code):
        self.url = url
        self.code = code

    def get(self):
        return FilebrowserImage(self.url, self.code)
