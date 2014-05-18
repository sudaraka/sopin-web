#  ui/views/homepage.py: UI views for the homepage
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

""" Homepage views """

from django.shortcuts import render

from app.settings import SITE_TITLE, VERSION

from data.models.inventory import Item


def default_view(request):
    """ Process homepage url '/' and render the template 'home.html' """

    running_out = []
    to_buy = []

    for i in Item.objects.running_out():
        if 0 == i.stock_age_percent:
            to_buy.append(i)
        else:
            running_out.append(i)

    if 1 > len(running_out):
        running_out = None

    if 1 > len(to_buy):
        to_buy = None

    return render(request, 'home.html',
                  {'site_title': SITE_TITLE,
                   'site_version': ('v%d.%d %s' % VERSION).strip(),
                   'running_out_list': running_out,
                   'to_buy_list': to_buy, })
