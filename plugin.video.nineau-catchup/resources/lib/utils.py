#
# vim:ts=4
#

# XBMC addon for Nine (Australia) catch-up TV
# Copyright (c) 2014 Grant Beattie <xbmc#grantbeattie.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import httplib, urllib, sys
import config

conn = None

def http_get(path):
	global conn
	if conn is None:
		conn = httplib.HTTPConnection(config.web_host, 80)

	conn.request('GET', '/' + path, None, config.http_headers)
	response = conn.getresponse()
	return response

def build_url(query):
	base_url = sys.argv[0]
	return base_url + '?' + urllib.urlencode(query)
