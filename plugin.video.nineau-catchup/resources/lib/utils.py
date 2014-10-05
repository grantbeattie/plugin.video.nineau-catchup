#
# vim:ts=4
#

# XBMC addon for Nine (Australia) catch-up TV
# Copyright (c) 2014 Grant Beattie <xbmc#grantbeattie.com>

# Portions Copyright (C) 2014 Andy Botting <andy#andybotting.com>

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

import sys, os
import re, httplib, threading, urllib
import xbmc, xbmcaddon

import config
import m3u8
from hashlib import md5

addon = xbmcaddon.Addon(config.ADDON_ID)

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


def log(msg):
	print "[%s] %s" % (config.NAME, msg)


def get_stream_url(video_id):
    if addon and addon.getSetting('ssl_compatibility_mode') == 'false':
        # Use Apple iOS HLS stream directly
        # This requires gnutls support in ffmpeg, which is only found in XBMC v13
        # but not available at all in iOS or Android builds
        log("Using native HTTPS HLS stream handling...")
        stream_url = config.stream_url % videoId

    else:
        # Use Adam M-W's implementation of handling the HTTPS business within
        # the m3u8 file directly. He's a legend.
        log("Using HTTPS HLS stream compatibility mode...")
        stream_url = get_m3u8(video_id)

    return stream_url


def get_m3u8(video_id):
    brightcove_url = config.stream_url % video_id
    index_m3u8 = m3u8.load(brightcove_url)

    # Get the highest bitrate video
    rendition_uri = sorted(index_m3u8.playlists, key=lambda playlist: playlist.stream_info.bandwidth)[0].uri

    # Download the rendition and modify the key uris
    (rendition_m3u8_path, keys) = download_rendition(rendition_uri, video_id)

    # Download the keys
    download_keys(keys)

    return rendition_m3u8_path


def get_temp_dir(video_id):
    topdir = os.path.join(xbmc.translatePath('special://temp/'), config.ADDON_ID)
    if not os.path.isdir(topdir):
        os.mkdir(topdir)

    dirname = 'brightcove_%s' % video_id
    path = os.path.join(topdir, dirname)
    if not os.path.isdir(path):
        os.mkdir(path)
    return path


def download_rendition(rendition_uri, video_id):
    temp_dir = get_temp_dir(video_id)
    log('Downloading rendition file from "%s" to "%s"...' % (rendition_uri, temp_dir))
    rendition_m3u8_path = os.path.join(temp_dir, 'rendition.m3u8')
    rendition_m3u8_file = open(rendition_m3u8_path, 'w')
    rendition_m3u8_response = urllib.urlopen(rendition_uri)
    keys = []
    for line in rendition_m3u8_response:
        match = re.match('#EXT-X-KEY:METHOD=AES-128,URI="(https://.+?)"', line)
        if match:
            key_url = match.group(1)
            key_path = os.path.join(temp_dir, "keyfile_%s.key" % md5(key_url).hexdigest())
            keys.append((key_path, key_url))
            rendition_m3u8_file.write('#EXT-X-KEY:METHOD=AES-128,URI="%s"\n' % key_path)
        else:
            rendition_m3u8_file.write(line)
    rendition_m3u8_file.close()
    return (rendition_m3u8_path, keys)

def download_key(key_path, key_url):
    urllib.urlretrieve(key_url, key_path)

def download_keys(keys):
    log('Downloading HLS key files...')

    threads = []
    for key in keys:
        thread = threading.Thread(target=download_key, args=key)
        thread.daemon = True
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
