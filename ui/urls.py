#  ui/urls.py: URL definition for the web site UI module
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

""" UI URL definitions """

from django.conf.urls import patterns, url

urlpatterns = patterns(
    'ui',

    # Home page
    url(r'^$', 'views.homepage.default_view', name='homepage'),
    url(r'^download-to-buy/$', 'views.homepage.download_to_buy_view',
        name='download_to_buy'),

    # Item maintenance
    url(r'^item-maintenance/$', 'views.item.list_view',
        name='item_maintenance'),
    url(r'^item-maintenance/form(?:/(?P<itemid>\d+))?/$',
        'views.item.form_view', name='item_maintenance_form'),
    url(r'^item-maintenance/remove/(?P<itemid>\d+)/$',
        'views.item.remove', name='item_maintenance_delete'),

    # Purchase
    url(r'^item-maintenance/purchase/$',
        'views.purchase.form_view', name='item_purchase_form'),
)
