import cv2

def check_video_frames(video_path):
    # 打开视频文件
    video = cv2.VideoCapture(video_path)

    # 检查视频是否成功打开
    if not video.isOpened():
        print(f"无法打开视频文件：{video_path}")
        return False

    # 读取视频的帧速率
    fps = video.get(cv2.CAP_PROP_FPS)

    # 逐帧读取视频
    frame_count = 0
    while True:
        # 读取下一帧
        ret, frame = video.read()

        # 如果无法读取下一帧，表示视频已经结束
        if not ret:
            break

        # 在这里进行帧校验的操作
        # 例如，可以检查帧是否为空，或者进行更复杂的图像分析
        if frame is None or frame.size == 0:
            print(f"帧校验失败：第 {frame_count} 帧为空或无效")
            return False

        # 计数
        frame_count += 1

        # 可选：显示或处理当前帧
        # cv2.imshow("Frame", frame)
        # cv2.waitKey(int(1000 / fps))

    # 释放视频文件
    video.release()

    # 校验成功
    print(f"视频校验成功，共读取了 {frame_count} 帧")
    return True

# 使用示例
video_path = 'C:\\Users\\syske\\Downloads\\6145daab-18de8aa582a-0006-ed9b-246-5143b.mp4'
check_video_frames(video_path)