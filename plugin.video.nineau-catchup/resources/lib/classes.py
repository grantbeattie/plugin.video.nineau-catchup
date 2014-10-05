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

import utils
import time

class Show(object):
	def __init__(self):
		self.slug = None
		self.title = None
		self.description = None
		self.episodeCount = None
		self.showImage = None
		self.genre = None

	def get_title(self):
		return self.title

	def get_list_title(self):
		return "%s (%d)" % (self.get_title(), self.get_episodeCount())

	def get_description(self):
		return self.description

	def get_episodeCount(self):
		return self.episodeCount

	def get_thumbnail(self):
		return self.showImage

	def get_fanart(self):
		return self.showImage

	def get_genre(self):
		return self.genre

	def get_xbmc_videoInfo(self):
		info = {}
		if self.get_title():			info['title'] = self.get_title()
		if self.get_description():		info['plot'] = self.get_description()
		if self.get_description():		info['plotoutline'] = self.get_description()
		if self.get_genre():			info['genre'] = self.get_genre()

		return info


class Season(object):
	def __init__(self):
		self.slug = None
		self.title = None
		self.description = None
		self.episodeCount = None
		self.showImage = None

	def get_title(self):
		return self.title

	def get_list_title(self):
		return "%s (%d)" % (self.get_title(), self.get_episodeCount())

	def get_episodeCount(self):
		return self.episodeCount

	def get_description(self):
		return self.description

	def get_fanart(self):
		return self.showImage

	def get_xbmc_videoInfo(self):
		info = {}
		if self.get_description():		info['plot'] = self.get_description()
		if self.get_description():		info['plotoutline'] = self.get_description()

		return info


class Episode(object):
	def __init__(self):
		self.slug = None
		self.videoId = None
		self.title = None
		self.showTitle = None
		self.description = None
		self.seasonTitle = None
		self.episodeNumber = None
		self.thumbnail = None
		self.showImage = None
		self.rating = None
		self.durationSeconds = None
		self.date = None
		self.genre = None

	def get_title(self):
		return self.title

	def get_showTitle(self):
		return self.showTitle

	def get_list_title(self):
		return "Episode %d: %s" % (self.get_episodeNumber(), self.get_title())

	def get_description(self):
		return self.description

	def get_season(self):
		return self.seasonTitle.replace('Season ', '')

	def get_episodeNumber(self):
		if self.episodeNumber: return int(self.episodeNumber)

	def get_thumbnail(self):
		return self.thumbnail

	def get_fanart(self):
		return self.showImage

	def get_rating(self):
		return self.rating

	def get_duration(self):
		if self.durationSeconds: return self.durationSeconds

	def get_durationMinutes(self):
		if self.durationSeconds: return int(self.durationSeconds/60)

	def get_year(self):
		if self.date: return time.strftime('%Y', self.date)

	def get_date(self):
		if self.date: return time.strftime('%Y-%m-%d', self.date)

	def get_genre(self):
		return self.genre

	def get_xbmc_videoInfo(self):
		info = {}
		if self.get_title():			info['title'] = self.get_title()
		if self.get_showTitle():		info['tvshowtitle'] = self.get_showTitle()
		if self.get_description():		info['plot'] = self.get_description()
		if self.get_description():		info['plotoutline'] = self.get_description()
		if self.get_season():			info['season'] = self.get_season()
		if self.get_episodeNumber():	info['episode'] = self.get_episodeNumber()
		if self.get_date():				info['aired'] = self.get_date()
		if self.get_year():				info['year'] = self.get_year()
		if self.get_durationMinutes():	info['duration'] = self.get_durationMinutes()
		if self.get_rating():			info['mpaa'] = self.get_rating()
		if self.get_genre():			info['genre'] = self.get_genre()

		return info

	def get_xbmc_audioStreamInfo(self):
		return {
			'codec':    'aac',
			'language': 'en',
			'channels': 2
		}

	def get_xbmc_videoStreamInfo(self):
		info = {}
		if self.get_duration():			info['duration'] = self.get_duration()

		info['codec'] = 'h264'
		return info

	def get_hls_url(self):
		return utils.get_stream_url(self.videoId)
		