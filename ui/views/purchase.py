#  ui/views/purchase.py: UI views for item purchase
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

""" Item purchase views """

import json

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

from ui.forms import PurchaseForm

from data.models.inventory import Item


def form_view(request):
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
