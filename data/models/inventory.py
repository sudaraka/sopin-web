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


RUNOUT_DAYS = 7


class ItemManager(models.Manager):
    """ Model manager for Items """

    def running_out(self):
        """
        Return a list of Items that needs to be purchased with in RUNOUT_DAYS
        days.

        """

        cursor = connection.cursor()
        cursor.execute(
            """
            select
                i.id,
                i.name,
                i.unit_symbol,
                i.unit_weight,
                i.purchase_threshold,
                i.extended_threshold,
                i.heavy,
                ifnull(julianday('now') - julianday(max(p.date)), -1)
                    as stock_days,
                ifnull(p.quantity, 0)
            from
                sopin_item as i
            left join sopin_purchase as p
                on p.item_id = i.id
            group by
                i.id
            having
                stock_days = -1 or
                (
                    (i.purchase_threshold * p.quantity)
                    + i.extended_threshold
                    - stock_days
                ) < %d
            order by
                stock_days asc
            """ % RUNOUT_DAYS)

        result = []
        for i in cursor.fetchall():
            item = self.model(pk=i[0], name=i[1], unit_symbol=i[2],
                              unit_weight=i[3], purchase_threshold=i[4],
                              extended_threshold=i[5], heavy=i[6])
            item.stock_age = i[7]

            age = i[7]
            th = (i[4] * i[8]) + i[5]

            if 0 < age and age < th:
                item.stock_age_percent = age / th * 100

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

    stock_age = None
    stock_age_percent = 0

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
