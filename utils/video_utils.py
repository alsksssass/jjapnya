# video_utils.py
import yt_dlp
import requests

YOUTUBE_API_KEY ='AIzaSyDfcoQyQq2lcevMuF0_6sngn-8ww5d1M68'
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'logtostderr': True,
    'extract_flat': True,
    'skip_download': True,
    'force-ipv4': True,
    'cachedir': False,
    
}

# def get_video_info(url: str):
#     while True:
#         try:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 video_info = ydl.extract_info(url, download=False)
#             new_url=video_info['url']
#             if not check_audio_url_validity(new_url):
#                 print(f"URL '{url}' is not playable. Retrying...")
#                 continue
#             break
#         except yt_dlp.utils.DownloadError as e:
#             print('여기서 에러남7')
#             print(f"다운로드 오류: {e}")
#             return None
#         except yt_dlp.utils.ExtractorError as e:
#             print('여기서 에러남8')
#             print(f"URL에서 정보 추출 오류: {e}")
#             return None
#         except requests.exceptions.HTTPError as errh:
#             print('여기서 에러남1')
#     return video_info

def get_video_info(url: str):
    try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(url, download=False)
    # except yt_dlp.utils.DownloadError as e:
    #         print(f"다운로드 오류: {e}")
    #         return None
    except yt_dlp.utils.ExtractorError as e:
            print(f"URL에서 정보 추출 오류: {e}")
            return None
    return video_info

def check_audio_url_validity(url):
    try:
        response = requests.head(url)
        # response = requests.get(url, stream=True)
        if response.status_code == 200:
            return True
        else:
            response = requests.head(url)
            # response = requests.get(url, stream=True)
            if response.status_code == 200:
                return True
            else:
                return False
    except requests.exceptions.RequestException as e:
        return False

def choose_best_audio(formats: list):
    audio_format = None
    for f in formats:
        if f['acodec'] != 'none' and (audio_format is None or f['abr'] > audio_format['abr']):
            audio_format = f
    return audio_format