# from pytube import YouTube
# import asyncio
# import json
# with open('config.json') as f:
#     dir_path = json.load(f)['videos_path']
#
# def get_available_qualities(youtube_link):
#     try:
#         yt = YouTube(youtube_link)
#         resolutions = yt.streams.filter(file_extension='mp4').all()  # Get the first available video stream
#         return resolutions
#         # res = []
#         # print(resolutions)
#         # for video in resolutions:
#         #     if video.resolution:
#         #         res.append((video.itag,video.resolution,video.filesize_mb))
#         # return res
#     except Exception as e:
#         print("Error:", e)
#
# async def download_video(youtube_link,filename):
#     yt = YouTube(youtube_link)
#     # path = yt.streams.get_by_itag(int(itag)).download()
#     # return path
#     path = yt.streams.get_highest_resolution().download(max_retries=3,filename=filename,output_path=dir_path)
#     return filename
# def get_time():
#     pass
#
# def send_resolution_list():
#     pass
#
# if __name__ == '__main__':
#
#     import time
#     start = time.time()
#     youtube_link = "https://www.youtube.com/watch?v=DodeWQw3N3A"
#     # available_qualities = get_available_qualities(youtube_link)
#     download_video(youtube_link,filename='file.mp4')
#     print(time.time()-start)