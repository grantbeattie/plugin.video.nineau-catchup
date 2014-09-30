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

import classes, episodes, config, utils
try:
	import xbmcgui, xbmc
except ImportError:
	pass

def play_ep(slug):
    ep = episodes.scrape_ep(slug)

    hls_url = ep.get_hls_url()
    thumbnail_url = ep.get_thumbnail()
    listitem = xbmcgui.ListItem(label=ep.get_title(), iconImage=thumbnail_url, thumbnailImage=thumbnail_url)

    listitem.setInfo('video', ep.get_xbmc_videoInfo())
    listitem.addStreamInfo('audio', ep.get_xbmc_audioStreamInfo())
    listitem.addStreamInfo('video', ep.get_xbmc_videoStreamInfo())

	config.log_msg("Playing stream: %s" % hls_url)
    xbmc.Player().play(hls_url, listitem)
