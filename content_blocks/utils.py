from django.contrib import admin
from django.core.urlresolvers import reverse


def get_admin_list_page(model):
    """
    Returns the admin list page path for the given model.
    """
    app_label = model._meta.app_label
    model_name = model.__name__
    admin_base_url = reverse(admin.site.root, args=('',))
    return u"%s%s/%s/" % (admin_base_url, app_label, model_name.lower())


def get_admin_edit_page(instance):
    """
    Returns the admin edit page path for the given instance.
    """
    list_page = get_admin_list_page(instance.__class__)
    return u"%s%d/" % (list_page, instance.pk)
