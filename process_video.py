# # import ffmpeg
# import json
# import subprocess
# with open('config.json') as f:
#     dir_path = json.load(f)['videos_path']
#
# def check_time_stamp():
#     pass
#
# def trim_video(filename,start,end):
#     # start = check_time_stamp()
#     # end = check_time_stamp()
#
#     command = f"ffmpeg -i {dir_path+filename} -ss {start} -t {end} -c copy {dir_path+'trimmed-'+filename}"
#     print(command)
#     result = subprocess.run(command, shell=True, capture_output=True, text=True)
#     print("Output:", result.stdout)
#     if result.stderr:
#         print("Error:", result.stderr)
#     print('='*30)
#     print('Video has been trimmed')
#     print('=' * 30)
#
# if __name__ == '__main__':
#     import time
#     start = time.time()
#     dir_path = r'C:\\Users\\hardik\\PycharmProjects\\TeleGramBot\\TrimmedVideoDownloaded\\'
#     trim_video('40118b62.mp4',100,500)
#     print(time.time() - start)