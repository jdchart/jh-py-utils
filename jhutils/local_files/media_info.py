from PIL import Image
# from moviepy import VideoFileClip
from pydub import AudioSegment
from pymediainfo import MediaInfo
import stat
import os
import time
import mimetypes
import hashlib

def get_file_info(file_path):
    info = {}
    info['absolute_path'] = os.path.abspath(file_path)
    info['size_bytes'] = os.path.getsize(file_path)
    info['created'] = time.ctime(os.path.getctime(file_path))
    info['modified'] = time.ctime(os.path.getmtime(file_path))
    info['accessed'] = time.ctime(os.path.getatime(file_path))
    
    st = os.stat(file_path)
    info['mode'] = oct(st.st_mode)
    info['is_readable'] = os.access(file_path, os.R_OK)
    info['is_writable'] = os.access(file_path, os.W_OK)
    info['is_executable'] = os.access(file_path, os.X_OK)

    # File type
    info['extension'] = os.path.splitext(file_path)[1]
    info['mimetype'], _ = mimetypes.guess_type(file_path)

    def get_hash(file_path, algorithm):
        hash_func = hashlib.new(algorithm)
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    for algo in ['md5', 'sha1', 'sha256', 'sha512']:
        info[f'{algo}_hash'] = get_hash(file_path, algo)

    return info

def get_image_info(file_path):
    with Image.open(file_path) as img:
        width, height = img.size
        exif_data = img._getexif()
        return {
            "width": width,
            "height": height
            #"exif_data": exif_data,
            #"color_mode" : img.mode,
            #"bit_depth" : img.bits
        }

    
def get_audio_info(file_path):
    audio = AudioSegment.from_file(file_path)
    return {
        "duration" : len(audio),
        "channels" : audio.channels,
        "frame_rate" : audio.frame_rate,
        "sample_width" :audio.sample_width,
        "frames" : audio.frame_count() 
    }

# def get_video_info(file_path):
#     video = VideoFileClip(file_path)
#     width, height = video.size

#     return {
#         "video_duration_ms" : video.duration / 1000,
#         "width" : width,
#         "height" : height,
#         # "video_frames" : video.reader.nframes,
#         "video_frame_rate" : video.fps,
#         # "video_codec" : video.reader.codec,
#         # "audio_duration_ms" : video.audio.duration / 1000,
#         # "audio_channels" : video.audio.nchannels,
#         # "audio_frame_rate" : video.audio.fps,
#         # "audio_sample_width" : video.audio.nbytes // video.audio.nchannels ,
#         # "audio_frames" : video.audio.reader.nframes,
#     }

def get_video_info(file_path):
    media_info = MediaInfo.parse(file_path)
    for track in media_info.tracks:
        if track.track_type == 'Video':
            return {
                "duration": track.duration,
                "width": track.width,
                "height": track.height,
                "video_frame_rate": track.frame_rate,
            }