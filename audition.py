import lxml.etree as ET


def get_markers(filename):
    with open(filename, 'rb') as f:
        o = ET.parse(f)
        xmp_as_xml_string = o.find('.//xmpMetadata').text
        namespaces = {'xmpDM': 'http://ns.adobe.com/xmp/1.0/DynamicMedia/'}
        xmp = ET.fromstring(xmp_as_xml_string)
        frame_rate = int(xmp.find('.//xmpDM:Tracks//xmpDM:frameRate', namespaces).text[1:])  # e.g. f44100
        markers_xpath = xmp.xpath('.//xmpDM:Tracks//xmpDM:trackName[.=\'CuePoint Markers\']/../xmpDM:markers//xmpDM:name/../xmpDM:startTime/..', namespaces=namespaces)
        markers = []
        for marker in markers_xpath:
            time = int(marker.find('xmpDM:startTime', namespaces).text)
            time_sec = time / frame_rate
            name = marker.find('xmpDM:name', namespaces).text
            markers.append([time_sec, name])
        return markers


def get_clips(filename, track_name):
    clips = {}
    with open(filename, 'rb') as f:
        o = ET.parse(f)
        sample_rate = int(o.xpath('/sesx/session/@sampleRate')[0])
        els = o.xpath('.//audioTrack/trackParameters/name[.=\'' + track_name + '\']/../../audioClip')
        for el in els:
            start_point = int(el.attrib['startPoint'])/sample_rate
            end_point = int(el.attrib['endPoint'])/sample_rate
            source_in_point = int(el.attrib['sourceInPoint'])/sample_rate
            source_out_point = int(el.attrib['sourceOutPoint'])/sample_rate
            name = el.attrib['name']
            clips[name] = [start_point, end_point, source_in_point, source_out_point]
    return clips


def find_time_in_clip(clip_name, rel_time, clips_translation):
    for name, clip in clips_translation.items():
        if name == clip_name:
            return rel_time+clip[0]-clip[2]


def adjust_marker(time, clips_recorded, clips_translation):
    for name, clip in clips_recorded.items():
        if clip[0] <= time <= clip[1]:
            rel_time = time - clip[0]
            adj_time = find_time_in_clip(name, rel_time, clips_translation)
            return adj_time


def seconds_to_time_stamp(seconds):
    sec_round = round(seconds)
    hours = int(sec_round / 3600)
    min = int(sec_round / 60) % 60
    sec = sec_round % 60
    res = ''
    if hours:
        res += str(hours)+':'
    res += '%02d:%02d' % (min, sec)
    return res


def adjust_markers(markers, clips_recorded, clips_translation):
    for marker in markers:
        marker_time = marker[0]
        marker_name = marker[1]
        adjusted_time = adjust_marker(marker_time, clips_recorded, clips_translation)
        time_str = seconds_to_time_stamp(adjusted_time)
        print(time_str, marker_name)

if __name__ == '__main__':
    filename = 'D:\\video\\GoswamiMj-videos\\2016-12-28 goswamimj ru.sesx'
    markers = get_markers(filename)
    clips_recorded = get_clips(filename, 'Track 1')
    clips_translation = get_clips(filename, 'Translation')
    markers_adjusted = adjust_markers(markers, clips_recorded, clips_translation)
