#  data/models/inventory.py: Data models that make up the shopping inventory
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

""" Data models that make up the shopping inventory """

from django.db import models


class Item(models.Model):
    """ Item data model definition """

    name = models.CharField(max_length=32, unique=True, blank=False,
                            null=False)
    unit_symbol = models.CharField(max_length=8, blank=True)
    unit_weight = models.DecimalField(max_digits=6, decimal_places=2,
                                      default=1)
    purchase_threshold = models.IntegerField(default=21)
    extended_threshold = models.IntegerField(null=True, blank=True)
    heavy = models.BooleanField(default=False)

    class Meta:  # pylint: disable=I0011,C1001
        """ Meta class for Item model """

        ordering = ('name', )

        # Set following fields manually since our models are in sub-directories
        app_label = 'data'
        db_table = 'sopin_item'
