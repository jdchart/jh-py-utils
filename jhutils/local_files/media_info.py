from PIL import Image
# from moviepy import VideoFileClip
from pydub import AudioSegment
from pymediainfo import MediaInfo

def get_image_info(file_path):
    with Image.open(file_path) as img:
        width, height = img.size
        exif_data = img._getexif()
        return {
            "width": width,
            "height": height,
            "exif_data": exif_data,
            "color_mode" : img.mode,
            "bit_depth" : img.bits
        }
    
    with Image.open(file_object.path) as img:
        width, height = img.size
        props["width"] = width
        props["height"] = height
        props["color_mode"] = img.mode
        props["bit_depth"] = img.bits

    
def get_audio_info(file_path):
    audio = AudioSegment.from_file(file_path)
    return {
        "duration_ms" : len(audio),
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
                "video_duration_ms": track.duration,
                "width": track.width,
                "height": track.height,
                "video_frame_rate": track.frame_rate,
            }