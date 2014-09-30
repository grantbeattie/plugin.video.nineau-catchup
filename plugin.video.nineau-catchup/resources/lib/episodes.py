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

import json, time, sys
import utils, classes
import config

try:
	import xbmcgui, xbmcplugin
except ImportError:
	pass

def make_ep_obj(ep):
	new_ep = classes.Episode()

	new_ep.slug = ep['slug']
	new_ep.videoId = ep['videoId']
	new_ep.title = ep['title']
	new_ep.showTitle = ep['showTitle']
	new_ep.seasonTitle = ep['seasonTitle']
	if ep.has_key('airDate') and ep['airDate'] is not None: new_ep.date = time.gmtime(ep['airDate']/1000)
	new_ep.episodeNumber = ep['episodeNumber']
	new_ep.description = ep['description']
	new_ep.durationSeconds = ep['durationSeconds']
	if ep.has_key('classification'): new_ep.rating = ep['classification']
	new_ep.thumbnail = ep['images']['videoStill']

	return new_ep


def scrape_ep(slug):
	ep = json.load(utils.http_get(slug))

	new_ep = make_ep_obj(ep)
	return new_ep


def scrape(slug):
	episode_list = []

	response = utils.http_get(slug + '?fields=true')
	json_data = json.load(response)

	for ep in json_data['episodes']:
		new_ep = make_ep_obj(ep)
		new_ep.showImage = json_data['show']['image']['showImage']

		episode_list.append(new_ep)

	return sorted(episode_list, key=lambda k: k.get_episodeNumber())


def build_episode_list(slug):
	addon_handle = int(sys.argv[1])

	eps = scrape(slug)
	for ep in eps:
		url = utils.build_url({ 'play': ep.slug })

		thumbnail_url = ep.get_thumbnail()
		listitem = xbmcgui.ListItem(label=ep.get_list_title(), iconImage=thumbnail_url, thumbnailImage=thumbnail_url)

		listitem.setInfo('video', ep.get_xbmc_videoInfo())
		listitem.addStreamInfo('video', ep.get_xbmc_videoStreamInfo())
		listitem.addStreamInfo('audio', ep.get_xbmc_audioStreamInfo())
		listitem.setArt({ 'fanart': ep.get_fanart() })

		xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=listitem, isFolder=False, totalItems=len(eps))

	xbmcplugin.endOfDirectory(addon_handle)
	xbmcplugin.setContent(addon_handle, content='episodes')
