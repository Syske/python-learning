import ffmpeg
 
def check_video_file(video_path, timeout=10):
    try:
        probe = ffmpeg.probe(video_path, timeout=timeout)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        if video_stream is None:
            print(f"No video stream found in {video_path}")
            return False
        
        # 尝试读取一帧
        (
            ffmpeg
            .input(video_path, ss=0, t=1, frames=1)
            .output('pipe:', vframes=1, format='image2')
            .run(quiet=True)
        )
        print(f"Video file {video_path} is likely not corrupted.")
        return True
    except ffmpeg.Error as e:
        print(f"Video file {video_path} is corrupted: {e.stderr.decode('utf8')}")
        return False
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return False
        
def check_video_file2(video_path):
    try:
        # 仅仅使用ffprobe来检查文件
        probe = ffmpeg.probe(video_path)
        print(f"Video file {video_path} is likely not corrupted.")
        return True
    except ffmpeg.Error as e:
        print(f"Error occurred while probing the video file {video_path}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return False
 
# 使用示例
check_video_file2('C:\\Users\\syske\\Downloads\\6145daab-18de8aa582a-0006-ed9b-246-5143b.mp4')