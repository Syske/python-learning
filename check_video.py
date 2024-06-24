from moviepy.editor import VideoFileClip
 
def check_video(video_path):
    try:
        video_clip = VideoFileClip(video_path)
        if video_clip.duration > 0:
            print(f"视频文件 {video_path} 是有效的")
            return True
        else:
            print(f"视频文件 {video_path} 是无效的，无法读取")
            return False
    except Exception as e:
        print(f"发生错误：{e}")
        return False
 
# 使用示例
video_path = 'C:\\Users\\syske\\Downloads\\6145daab-18de8aa582a-0006-ed9b-246-5143b.mp4'
check_video(video_path)