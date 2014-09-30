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

import os, sys
import urlparse

try:
        cur_dir = os.path.dirname(os.path.abspath(__file__))
except:
        cur_dir = os.getcwd()

sys.path.append(os.path.join(cur_dir, 'resources', 'lib'))
import shows, seasons, episodes, play

args = urlparse.parse_qs(sys.argv[2][1:])

slug_arg = args.get('slug', None)
season_arg = args.get('season', None)
play_arg = args.get('play', None)

if play_arg is not None:
	play.play_ep(play_arg[0])
elif slug_arg is None:
	shows.build_show_list()
elif season_arg is None:
	seasons.build_season_list(slug_arg[0])
else:
	episodes.build_episode_list(slug_arg[0])
