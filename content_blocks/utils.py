from django.core.urlresolvers import reverse
from test_helper.utils import TestHelper


def get_admin_list_page(model):
    """
    Returns the admin list page path for the given model.
    """
    return TestHelper().getAdminListPage(model)


def get_admin_edit_page(instance):
    """
    Returns the admin edit page path for the given instance.
    """
    return TestHelper().getAdminEditPage(instance)
