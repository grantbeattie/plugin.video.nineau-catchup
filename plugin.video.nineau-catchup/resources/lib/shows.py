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
import utils, config, classes
try:
	import xbmcgui, xbmcplugin
except ImportError:
	pass

def scrape():
	show_list = []

	response = utils.http_get('shows?take=-1')
	json_data = json.load(response)

	for show in json_data['payload']:
		new_show = classes.Show()
		new_show.slug = show['slug']
		new_show.title = show['title']
		new_show.drm = show['drm']
		new_show.episodeCount = show['episodeCount']
		new_show.description = show['description']
		new_show.showImage = show['image']['showImage']

		if new_show.drm is True:
			continue

		if new_show.episodeCount > 0:
			show_list.append(new_show)

	return sorted(show_list, key=lambda k: k.get_title())


def build_show_list():
	addon_handle = int(sys.argv[1])

	for show in scrape():
		url = utils.build_url({ 'slug': show.slug })

		thumbnail_url = show.get_thumbnail()
		listitem = xbmcgui.ListItem(label=show.get_list_title(), iconImage=thumbnail_url, thumbnailImage=thumbnail_url)

		listitem.setInfo('video', show.get_xbmc_videoInfo())
		listitem.setArt({ 'fanart': show.get_fanart() })
		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=listitem, isFolder=True)

	xbmcplugin.endOfDirectory(addon_handle)
	xbmcplugin.setContent(addon_handle, content='tvshows')

