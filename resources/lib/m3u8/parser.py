# coding: utf-8
# Copyright 2014 Globo.com Player authors. All rights reserved.
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.

import re
from m3u8 import protocol

'''
http://tools.ietf.org/html/draft-pantos-http-live-streaming-08#section-3.2
http://stackoverflow.com/questions/2785755/how-to-split-but-ignore-separators-in-quoted-strings-in-python
'''
ATTRIBUTELISTPATTERN = re.compile(r'''((?:[^,"']|"[^"]*"|'[^']*')+)''')

def parse(content):
    '''
    Given a M3U8 playlist content returns a dictionary with all data found
    '''
    data = {
        'is_variant': False,
        'is_endlist': False,
        'is_i_frames_only': False,
        'playlist_type': None,
        'playlists': [],
        'iframe_playlists': [],
        'segments': [],
        'media': [],
        }

    state = {
        'expect_segment': False,
        'expect_playlist': False,
        }

    for line in string_to_lines(content):
        line = line.strip()

        if line.startswith(protocol.ext_x_byterange):
            _parse_byterange(line, state)
            state['expect_segment'] = True

        elif state['expect_segment']:
            _parse_ts_chunk(line, data, state)
            state['expect_segment'] = False

        elif state['expect_playlist']:
            _parse_variant_playlist(line, data, state)
            state['expect_playlist'] = False

        elif line.startswith(protocol.ext_x_targetduration):
            _parse_simple_parameter(line, data, float)
        elif line.startswith(protocol.ext_x_media_sequence):
            _parse_simple_parameter(line, data, int)
        elif line.startswith(protocol.ext_x_program_date_time):
            _parse_simple_parameter_raw_value(line, data)
        elif line.startswith(protocol.ext_x_version):
            _parse_simple_parameter(line, data)
        elif line.startswith(protocol.ext_x_allow_cache):
            _parse_simple_parameter(line, data)

        elif line.startswith(protocol.ext_x_key):
            _parse_key(line, data)

        elif line.startswith(protocol.extinf):
            _parse_extinf(line, data, state)
            state['expect_segment'] = True

        elif line.startswith(protocol.ext_x_stream_inf):
            state['expect_playlist'] = True
            _parse_stream_inf(line, data, state)

        elif line.startswith(protocol.ext_x_i_frame_stream_inf):
            _parse_i_frame_stream_inf(line, data)

        elif line.startswith(protocol.ext_x_media):
            _parse_media(line, data, state)

        elif line.startswith(protocol.ext_x_playlist_type):
            _parse_simple_parameter(line, data)

        elif line.startswith(protocol.ext_i_frames_only):
            data['is_i_frames_only'] = True

        elif line.startswith(protocol.ext_x_endlist):
            data['is_endlist'] = True

    return data

def _parse_key(line, data):
    params = ATTRIBUTELISTPATTERN.split(line.replace(protocol.ext_x_key + ':', ''))[1::2]
    data['key'] = {}
    for param in params:
        name, value = param.split('=', 1)
        data['key'][normalize_attribute(name)] = remove_quotes(value)

def _parse_extinf(line, data, state):
    duration, title = line.replace(protocol.extinf + ':', '').split(',')
    state['segment'] = {'duration': float(duration), 'title': remove_quotes(title)}

def _parse_ts_chunk(line, data, state):
    segment = state.pop('segment')
    segment['uri'] = line
    data['segments'].append(segment)

def _parse_attribute_list(prefix, line, quoted):
    params = ATTRIBUTELISTPATTERN.split(line.replace(prefix + ':', ''))[1::2]

    attributes = {}
    for param in params:
        name, value = param.split('=', 1)
        name = normalize_attribute(name)

        if name in quoted:
            value = remove_quotes(value)

        attributes[name] = value

    return attributes

def _parse_stream_inf(line, data, state):
    data['is_variant'] = True
    quoted = ('codecs', 'audio', 'video', 'subtitles')
    state['stream_info'] = _parse_attribute_list(protocol.ext_x_stream_inf, line, quoted)

def _parse_i_frame_stream_inf(line, data):
    quoted = ('codecs', 'uri')
    iframe_stream_info = _parse_attribute_list(protocol.ext_x_i_frame_stream_inf, line, quoted)
    iframe_playlist = {'uri': iframe_stream_info.pop('uri'),
                       'iframe_stream_info': iframe_stream_info}

    data['iframe_playlists'].append(iframe_playlist)

def _parse_media(line, data, state):
    quoted = ('uri', 'group_id', 'language', 'name', 'characteristics')
    media = _parse_attribute_list(protocol.ext_x_media, line, quoted)
    data['media'].append(media)

def _parse_variant_playlist(line, data, state):
    playlist = {'uri': line,
                'stream_info': state.pop('stream_info')}

    data['playlists'].append(playlist)

def _parse_byterange(line, state):
    state['segment']['byterange'] = line.replace(protocol.ext_x_byterange + ':', '')

def _parse_simple_parameter_raw_value(line, data, cast_to=str, normalize=False):
    param, value = line.split(':', 1)
    param = normalize_attribute(param.replace('#EXT-X-', ''))
    if normalize:
        value = normalize_attribute(value)
    data[param] = cast_to(value)

def _parse_simple_parameter(line, data, cast_to=str):
    _parse_simple_parameter_raw_value(line, data, cast_to, True)

def string_to_lines(string):
    return string.strip().replace('\r\n', '\n').split('\n')

def remove_quotes(string):
    '''
    Remove quotes from string.

    Ex.:
      "foo" -> foo
      'foo' -> foo
      'foo  -> 'foo

    '''
    quotes = ('"', "'")
    if string and string[0] in quotes and string[-1] in quotes:
        return string[1:-1]
    return string

def normalize_attribute(attribute):
    return attribute.replace('-', '_').lower().strip()

def is_url(uri):
    return re.match(r'https?://', uri) is not None
