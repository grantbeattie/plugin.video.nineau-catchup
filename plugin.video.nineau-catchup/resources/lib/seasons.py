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

import json, sys
import utils, classes
try:
	import xbmcgui, xbmcplugin
except ImportError:
	pass

def scrape(slug):
	season_list = []

	response = utils.http_get(slug + '?fields=true')
	json_data = json.load(response)

	for season in json_data['seasons']:
		new_season = classes.Season()

		new_season.slug = season['slug']
		new_season.title = season['title']
		new_season.description = season['description']
		new_season.episodeCount = season['numberEpisodes']
		new_season.showImage = json_data['image']['showImage']

		season_list.append(new_season)

	return season_list


def build_season_list(slug):
	addon_handle = int(sys.argv[1])
	
	for season in scrape(slug):
		url = utils.build_url({ 'slug': season.slug, 'season': season.get_title() })

		listitem = xbmcgui.ListItem(label=season.get_list_title())

		listitem.setInfo('video', season.get_xbmc_videoInfo())
		listitem.setArt({ 'fanart': season.get_fanart() })
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=listitem, isFolder=True, totalItems=season.get_episodeCount())

	xbmcplugin.endOfDirectory(addon_handle)
	xbmcplugin.setContent(addon_handle, content='tvshows')
