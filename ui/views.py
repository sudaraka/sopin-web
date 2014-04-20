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

import json

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from app.settings import SITE_TITLE, VERSION

from ui.forms import ItemForm, PurchaseForm

from data.models.inventory import Item


def homepage_view(request):
    """ Process homepage url '/' and render the template 'home.html' """

    running_out = []

    for i in Item.objects.running_out():
        if 0 == i.stock_age_percent:
            pass
        else:
            running_out.append(i)

    if 1 > len(running_out):
        running_out = None

    return render(request, 'home.html', {'site_title': SITE_TITLE,
                                         'site_version': ('v%d.%d %s' %
                                                          VERSION).strip(),
                                         'running_out_list': running_out})


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


def item_maintenance_form(request, itemid=''):
    """
    Render item maintenance (add/edit) form, and handle the submitted data.

    """

    item = None

    try:
        if itemid is not None:
            item = Item.objects.get(id=int(itemid))
    except Item.DoesNotExist:
        pass

    if 'POST' == request.method:
        form = ItemForm(data=request.POST, instance=item)

        if form.is_valid():  # pragma: no branch
            form.save()

            result = {
                'code': 0,
                'message': 'success',
            }

            return HttpResponse(json.dumps(result),
                                content_type='application/json')
    else:
        form = ItemForm(instance=item)

    return render(request, 'items/form.html', {'form': form})


def item_maintenance_delete(request, itemid=''):
    """
    Remove selected item from the database and redirect to item maintenance
    page.

    """

    try:
        if itemid is not None:
            Item.objects.get(id=int(itemid)).delete()

            messages.success(request, 'Item was successfully removed')
        else:  # pragma: no cover
            messages.warning(request, 'Item ID to remove was not provided')
    except Item.DoesNotExist:
        messages.warning(request, 'Item with give ID does not exists')
    except Exception as e:  # pragma: no cover
        messages.error(request, e)

    return redirect('item_maintenance')


def item_purchase_form(request):
    """ Render item purchase form, and handle the submitted data. """

    form = None
    item = Item()

    if 'POST' == request.method:
        form = PurchaseForm(data=request.POST)

        if form.is_valid():  # pragma: no branch
            form.save()

            result = {
                'code': 0,
                'message': 'success',
            }

            return HttpResponse(json.dumps(result),
                                content_type='application/json')
    else:
        try:
            itemid = int(request.GET['item'])
            if 0 < itemid:
                item = Item.objects.get(pk=itemid)
                form = PurchaseForm(data={'item': item})
        except Item.DoesNotExist:
            pass
        except MultiValueDictKeyError:
            pass

    return render(request, 'items/purchase.html', {'form': form,
                                                   'item': item})
