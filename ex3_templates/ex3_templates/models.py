from persistent.mapping import PersistentMapping
import transaction


# We replace the 'MyModel' model from ex2 with a 'Folder' model.
class Folder(PersistentMapping):
    __parent__ = __name__ = None

    # Our model's '__init__' looks like any old Python '__init__'
    # method.  Make sure you make a 'super' call to the base class
    # when initializing:
    def __init__(self, title, description=u""):
        super(Folder, self).__init__()
        self.title = title
        self.description = description

    # This is the dict method that's called when you do
    # 'folder["child"] = child'.  Notice how, in addition, to adding
    # the object into the container, we also set the item's '__name__'
    # and '__parent__' attributes.  These help Pyramid find an item's
    # location in the object graph, and allow us to traverse up the
    # tree.  (By accessing 'item.__parent__'.)
    def __setitem__(self, name, item):
        super(Folder, self).__setitem__(name, item)
        item.__name__ = name
        item.__parent__ = self


def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        # Instead of adding a 'MyModel' class as our root object, we
        # now add a 'Folder'.  Folders have a 'title' and a 'description'.
        app_root = Folder(
            title=u"FabCollab",
            description=u"Welcome to FabCollab!",
            )
        zodb_root['app_root'] = app_root
        transaction.commit()
    return zodb_root['app_root']
