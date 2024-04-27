from moviepy.editor import VideoFileClip
dir_path = 'C:\\Users\\hardik\\PycharmProjects\\TeleGramBot\\TrimmedVideoDownloaded\\'

def trim_video(filename,start,end):
    with VideoFileClip(filename) as video:
        trimmed_video = video.subclip(start,end)
        trimmed_video.write_videofile(dir_path+'trimmed-'+filename)
        trimmed_video.close()


if __name__ == '__main__':
    trim_video(r'C:\Users\hardik\PycharmProjects\TeleGramBot\TrimmedVideoDownloaded\Saari Duniya Jalaa Denge.mp4',1,180)