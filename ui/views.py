#  ui/views.py: UI views for the web site
#
#  Copyright 2014 Sudaraka Wijesinghe <sudaraka.org/contact>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

""" UI views """

from django.shortcuts import render
from django.http import HttpResponse

from app.settings import SITE_TITLE, VERSION

from ui.forms import ItemForm

from data.models.inventory import Item


def homepage_view(request):
    """ Process homepage url '/' and render the template 'home.html' """

    return render(request, 'home.html', {'site_title': SITE_TITLE,
                                         'site_version': ('v%d.%d %s' %
                                                          VERSION).strip()})


def item_maintenance_view(request):
    """
    Process items maintenance url '/item-maintenance' and render the template
    'items.html'

    """

    item_list = Item.objects.all()

    return render(request, 'items/list.html',
                  {
                      'item_list': item_list,
                      'site_title': SITE_TITLE + ' - Item Maintenance',
                      'site_version': ('v%d.%d %s' % VERSION).strip()
                  })


def item_maintenance_form(request):
    """
    Render item maintenance (add/edit) form, and handle the submitted data.

    """

    form = ItemForm()

    return render(request, 'items/form.html', {'form': form})
