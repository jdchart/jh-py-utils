import requests
from PIL import Image
from io import BytesIO
from pymediainfo import MediaInfo

media_urls = {
    "images" : [
        "https://tile.loc.gov/storage-services/service/pnp/fsac/1a34000/1a34600/1a34630v.jpg",
        "https://tile.loc.gov/storage-services/service/pnp/fsac/1a34000/1a34200/1a34209v.jpg"
    ],
    "audio" : [
        "https://tile.loc.gov/storage-services/master/afc/afc1940001/afc1940001_a3815a2/afc1940001_a3815a2.wav",
        "https://tile.loc.gov/storage-services/master/afc/afc1999008/afc1999008_crf_mha215007.wav"
    ],
    "video" : [
        "https://tile.loc.gov/storage-services/service/mbrs/ntscrm/01629085/01629085.mp4",
        "https://tile.loc.gov/storage-services/public/music/musihas-200003870/musihas-200003870.0001.mp4"
    ]
}

def _get_online_image_info_process(url, bytes = 50000):
    headers = {'Range': f'bytes=0-{bytes}'}
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 206 or response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        return {
            "width" : img.size[0],
            "height" : img.size[1]
        }
    return None

def _get_online_video_info_process(url, bytes = 50000):
    headers = {'Range': f'bytes=0-{bytes}'}
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code in [200, 206]:
        media_info = MediaInfo.parse(BytesIO(response.content))
        for track in media_info.tracks:
            if track.track_type == 'Video':
                return {
                    'duration': track.duration / 1000,
                    'width': track.width,
                    'height': track.height,
                    "frame_rate" : track.frame_rate,
                    "format" : track.format,
                    "bit_depth" : track.bit_depth,
                    "frames" : track.frame_count
                }
    return None

def _get_online_audio_info_process(url, bytes = 50000):
    headers = {'Range': f'bytes=0-{bytes}'}
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code in [200, 206]:
        media_info = MediaInfo.parse(BytesIO(response.content))
        for track in media_info.tracks:
            if track.track_type == 'Audio':
                return {
                    "duration" : track.duration / 1000,
                    "channels" : track.channel_s,
                    "sample_rate" : track.sampling_rate,
                    "bit_rate" : track.bit_rate
                }
    return None

# import requests
# from pydub.utils import mediainfo

# def get_audio_metadata(url):
#     headers = {'Range': 'bytes=0-1000000'}  # Fetch first MB for metadata
#     response = requests.get(url, headers=headers, stream=True)
#     if response.status_code in [200, 206]:
#         with open("temp.wav", "wb") as f:
#             f.write(response.content)
#         info = mediainfo("temp.wav")
#         return info['duration'], info['channels'], info['sample_rate']
#     return None

def _get_online_info(type, url, initial_bytes = 50000, byte_limit = 100000000, byte_step = 50000, debug = True):
    answer = None
    found_answer = False
    current_bytes = initial_bytes
    
    while found_answer == False:
        if debug:
            print(f"Trying {current_bytes} bytes")
        if type == "image":
            answer = _get_online_image_info_process(url, current_bytes)
        if type == "audio":
            answer = _get_online_audio_info_process(url, current_bytes)
        if type == "video":
            answer = _get_online_video_info_process(url, current_bytes)
        
        if answer != None:
            found_answer = True
        else:
            current_bytes = current_bytes + byte_step
            if current_bytes > byte_limit:
                found_answer = True
    
    return answer

def get_online_image_info(url):
    return _get_online_info("image", url, 50000, 100000000, 50000)

def get_online_audio_info(url):
    return _get_online_info("audio", url, 50000, 100000000, 100000)

def get_online_video_info(url):
    return _get_online_info("video", url, 50000000, 100000000, 1000000)




print(get_online_image_info(media_urls["images"][1]))
print(get_online_audio_info(media_urls["audio"][1]))
print(get_online_video_info(media_urls["video"][0]))
