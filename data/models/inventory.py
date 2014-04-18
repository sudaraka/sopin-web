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

import datetime

from django.db import models, connection


class ItemManager(models.Manager):
    """ Model manager for Items """

    NEAR_THRESHOLD = 14

    def running_out(self):
        """
        Return a list of Items that near the threshold.

        Note: "Near Threshold" means the number of days since last purchase
        either passed the purchase_threshold or within NEAR_THRESHOLD days

        """

        cursor = connection.cursor()
        cursor.execute("""
                       select
                        i.id
                       from sopin_item as i
                       inner join sopin_purchase as p
                        on p.item_id = i.id
                       group by i.id
                       having (julianday('now') - julianday(max(p.date))) > %d
                       """ % self.NEAR_THRESHOLD)

        result = []
        for row in cursor.fetchall():
            item = self.model(pk=row[0])

            result.append(item)

        return result


class Item(models.Model):
    """ Item data model definition """

    objects = ItemManager()

    name = models.CharField(max_length=32, unique=True, blank=False,
                            null=False)
    unit_symbol = models.CharField(max_length=8, blank=True)
    unit_weight = models.DecimalField(max_digits=6, decimal_places=2,
                                      default=1)
    purchase_threshold = models.IntegerField(default=21)
    extended_threshold = models.IntegerField(null=False, blank=True, default=0)
    heavy = models.BooleanField(default=False)

    def last_purchase(self):
        """ Return the most recent Purchase for this item """

        try:
            return Purchase.objects.filter(item__id=self.id)[0]
        except IndexError:
            return None

    class Meta:  # pylint: disable=I0011,C1001
        """ Meta class for Item model """

        ordering = ['name']

        # Set following fields manually since our models are in sub-directories
        app_label = 'data'
        db_table = 'sopin_item'


class Purchase(models.Model):
    """ Purchase data model definition """

    item = models.ForeignKey(Item)
    date = models.DateField(default=datetime.date.today(), db_index=True)
    quantity = models.DecimalField(max_digits=6, decimal_places=2, default=1)

    def save(self, *args, **kwargs):  # pylint: disable=I0011,E1002
        """ Override parent "save" method to adjust Item parameters """

        super(Purchase, self).save(*args, **kwargs)

        if 0 != self.item.extended_threshold:
            self.item.extended_threshold = 0
            self.item.save()

    class Meta:  # pylint: disable=I0011,C1001
        """ Meta class for Purchase model """

        ordering = ['-date']

        # Set following fields manually since our models are in sub-directories
        app_label = 'data'
        db_table = 'sopin_purchase'
