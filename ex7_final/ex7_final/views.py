from colander import Schema, SchemaNode, SequenceSchema, String
from deform.widget import RichTextWidget, TextAreaWidget
from pyramid.httpexceptions import HTTPFound
from pyramid.security import Allow
from pyramid.view import view_config
from pyramid_deform import FormView

from .models import Folder, Page, User


@view_config(context=Folder, renderer='templates/folder.pt')
def folder_view(context, request):
    return {}


@view_config(context=Page, renderer='templates/page.pt')
def page_view(context, request):
    return {}


@view_config(context=User, renderer='templates/user.pt')
def user_view(context, request):
    return {}


class FolderSchema(Schema):
    title = SchemaNode(String())
    description = SchemaNode(
        String(),
        widget=TextAreaWidget(rows=5),
        missing=u"",
        )


class PageSchema(Schema):
    title = SchemaNode(String())
    description = SchemaNode(
        String(),
        widget=TextAreaWidget(rows=5),
        missing=u"",
        )
    body = SchemaNode(
        String(),
        widget=RichTextWidget(),
        missing=u"",
        )


@view_config(
    context=Folder,
    name='add-folder',
    permission='add',  # this permission argument was added
    renderer='templates/form.pt',
    )
class FolderAdd(FormView):
    schema = FolderSchema()
    buttons = ('save',)
    title = u"Add folder"

    def save_success(self, appstruct):
        context = self.request.context
        new_folder = Folder(**appstruct)
        name = appstruct['title'].lower()
        context[name] = new_folder
        self.request.session.flash(u"Your folder was added.", "success")
        return HTTPFound(location=self.request.resource_url(new_folder))


@view_config(
    context=Folder,
    name='edit',
    permission='edit',
    renderer='templates/form.pt',
    )
class FolderEdit(FormView):
    schema = FolderSchema()
    buttons = ('save',)
    title = u"Edit folder"

    def appstruct(self):
        context = self.request.context
        return {
            'title': context.title,
            'description': context.description,
            }

    def save_success(self, appstruct):
        context = self.request.context
        context.title = appstruct['title']
        context.description = appstruct['description']
        self.request.session.flash(u"Your changes have been saved.", "success")
        return HTTPFound(location=self.request.resource_url(context))


@view_config(
    context=Folder,
    name='add-page',
    permission='add',
    renderer='templates/form.pt',
    )
class PageAdd(FormView):
    schema = PageSchema()
    buttons = ('save',)
    title = u"Add page"

    def save_success(self, appstruct):
        context = self.request.context
        new_page = Page(**appstruct)
        name = appstruct['title'].lower()
        context[name] = new_page
        self.request.session.flash(u"Your page was added.", "success")
        return HTTPFound(location=self.request.resource_url(new_page))


@view_config(
    context=Page,
    name='edit',
    permission='edit',
    renderer='templates/form.pt',
    )
class PageEdit(FormView):
    schema = PageSchema()
    buttons = ('save',)
    title = u"Edit page"

    def appstruct(self):
        context = self.request.context
        return {
            'title': context.title,
            'description': context.description,
            'body': context.body,
            }

    def save_success(self, appstruct):
        context = self.request.context
        context.title = appstruct['title']
        context.description = appstruct['description']
        context.body = appstruct['body']
        self.request.session.flash(u"Your changes have been saved.", "success")
        return HTTPFound(location=self.request.resource_url(context))


class UsernamesSchema(SequenceSchema):
    username = SchemaNode(
        String(),
        title=u"Username",
        missing=None,
        )


class ShareSchema(Schema):
    usernames = UsernamesSchema(missing=[])


@view_config(
    name='share',
    permission='share',
    renderer='templates/form.pt',
    )
class Share(FormView):
    schema = ShareSchema()
    buttons = ('save',)
    title = u"Share item"

    def save_success(self, appstruct):
        context = self.request.context
        new_acl = set()
        existing_acl = getattr(context, '__acl__', [])

        for ace in existing_acl:
            allow_or_deny, username, permission = ace
            if username == self.request.user.__name__:
                new_acl.add(ace)
            elif username in appstruct['usernames']:
                new_acl.add(ace)

        for username in appstruct['usernames']:
            if username:
                new_acl.add((Allow, username, 'edit'))
                new_acl.add((Allow, username, 'add'))

        context.__acl__ = list(sorted(new_acl))
        self.request.session.flash(u"Your changes have been saved.", "success")
        return HTTPFound(location=self.request.path_url)

    def appstruct(self):
        usernames = []
        existing_acl = getattr(self.request.context, '__acl__', [])
        for allow_or_deny, username, permission in existing_acl:
            if permission == 'edit' and username != self.request.user.__name__:
                usernames.append(username)
        return {'usernames': usernames}


@view_config(name='follow')
def follow(context, request):
    logged_in_user = request.user
    if logged_in_user not in context.followers:
        context.followers.append(logged_in_user)
        request.session.flash(
            u"You are now following {0}.".format(context.__name__), "success")
    return HTTPFound(location=request.resource_url(context))


@view_config(name='unfollow')
def unfollow(context, request):
    logged_in_user = request.user
    if logged_in_user in context.followers:
        context.followers.remove(logged_in_user)
        request.session.flash(
            u"You no longer follow {0}.".format(context.__name__), "success")
    return HTTPFound(location=request.resource_url(context))
