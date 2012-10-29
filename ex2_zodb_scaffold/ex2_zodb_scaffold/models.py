from persistent.mapping import PersistentMapping


# This is the class that we use as our root object.
# 'PersistentMapping' inherits from 'dict' and thus we inherit
# '__getitem__' and '__setitem__' from it.
class MyModel(PersistentMapping):
    # These two attributes are part of the ILocation interface.  We'll
    # discuss what this means in the next exercise.
    __parent__ = __name__ = None


# The 'appmaker' is where, given a ZODB root, we return our
# application's 'app_root'.  If there is no 'app_root' in the database
# yet, we create one using our 'MyModel' class.
def appmaker(zodb_root):
    if not 'app_root' in zodb_root:
        app_root = MyModel()
        zodb_root['app_root'] = app_root
        import transaction
        transaction.commit()
    return zodb_root['app_root']
