from django.contrib import admin
from django.core.urlresolvers import reverse


def get_admin_list_page(model):
    """
    Returns the admin list page path for the given model.
    """
    app_label = model._meta.app_label
    model_name = model.__name__
    return reverse('admin:%s_%s_changelist' % (app_label, model_name.lower()))


def get_admin_edit_page(instance):
    """
    Returns the admin edit page path for the given instance.
    """
    app_label = instance.__class__._meta.app_label
    model_name = instance.__class__.__name__
    return reverse(
        'admin:%s_%s_change' % (app_label, model_name.lower()),
        args=(instance.pk,)
    )
