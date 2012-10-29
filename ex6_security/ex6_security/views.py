from colander import Schema, SchemaNode, String
from deform.widget import RichTextWidget, TextAreaWidget
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid_deform import FormView

from .models import Folder, Page


@view_config(context=Folder, renderer='templates/folder.pt')
def folder_view(context, request):
    return {}


@view_config(context=Page, renderer='templates/page.pt')
def page_view(context, request):
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
