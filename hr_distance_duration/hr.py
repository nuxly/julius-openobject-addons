# -*- coding: utf-8 -*-
#################################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Julius Network Solutions SARL <contact@julius.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################

from openerp.addons.google_maps_distance_duration.google_maps import GoogleMaps
import datetime
import time
from openerp import models, fields, api

class hr_job(models.Model):
    _inherit = 'hr.job'

    @api.one
    def get_duration(self):
        departure_time = self._context.get('departure_time')
        if not departure_time:
            n = datetime.datetime.now()
            departure_time = int(time.mktime(n.timetuple()))
        origin = 'Paris'
        destination = self.address_id and \
            self.address_id._get_url_parameters_partner_vals(self.address_id) or origin
        maps = GoogleMaps()
        for applicant in self.application_ids:
            origin = applicant.partner_id._get_url_parameters_partner_vals(applicant.partner_id)
            duration = maps.duration(origin, destination, mode='transit',
                                     departure_time=departure_time) / 60.0
            distance = maps.distance(origin, destination, mode='transit',
                                     departure_time=departure_time) / 1000.0
        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: