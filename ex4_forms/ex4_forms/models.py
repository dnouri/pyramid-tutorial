from persistent import Persistent
from persistent.mapping import PersistentMapping
import transaction


class Folder(PersistentMapping):
    __parent__ = __name__ = None

    def __init__(self, title, description=u""):
        super(Folder, self).__init__()
        self.title = title
        self.description = description

    def __setitem__(self, name, item):
        super(Folder, self).__setitem__(name, item)
        item.__name__ = name
        item.__parent__ = self


# This is our new Page model.  We inherit from Persistent instead of
# PersistentMapping, because we don't need the dict interface for
# pages.  (Pages cannot contain other pages or folders.)
class Page(Persistent):
    def __init__(self, title, description=u"", body=u""):
        super(Page, self).__init__()
        self.title = title
        self.description = description
        self.body = body


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        # Note how we, this time, prepopulate our database not only
        # with a root object, but also with a default 'about' object:
        app_root = Folder(
            title=u"FabCollab",
            description=u"Welcome to FabCollab!",
            )
        app_root['about'] = Page(
            title=u"About",
            body=u"<i>There's nothing to say</i>",
            )
        zodb_root['app_root'] = app_root
        transaction.commit()
    return zodb_root['app_root']
