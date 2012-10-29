import hashlib

from persistent import Persistent
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from pyramid.security import ALL_PERMISSIONS
from pyramid.security import Allow
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


class Page(Persistent):
    def __init__(self, title, description=u"", body=u""):
        super(Page, self).__init__()
        self.title = title
        self.description = description
        self.body = body


class User(Folder):
    def __init__(self, title, email, password,
                 description=u"", followers=None):
        super(User, self).__init__(title=title, description=description)
        self.email = email
        self.hashed_password = self.hash(password)

        if followers is None:
            self.followers = PersistentList()
        else:
            self.followers = PersistentList(followers)

    @staticmethod
    def hash(password):
        # Very weak hashing.  Do not use at home:
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    def validate_password(self, password):
        return self.hash(password) == self.hashed_password


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = Folder(
            title=u"FabCollab",
            description=u"Welcome to FabCollab!",
            )
        app_root['about'] = Page(
            title=u"About",
            body=u"<i>There's nothing to say</i>",
            )

        app_root['admin'] = User(
            title=u"admin",
            email=u"admin@fabcollab.it",
            password=u"admin",
            description=u"Site administrator",
            )

        # This grants all permissions every to the 'admin' user.
        app_root.__acl__ = [
            (Allow, 'admin', ALL_PERMISSIONS),
            ]

        zodb_root['app_root'] = app_root
        transaction.commit()
    return zodb_root['app_root']
