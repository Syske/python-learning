import ffmpeg

input_file = 'C://Users//syske//Videos//V30910-155116.mp4'
output_file = 'C://Users//syske//Videos//V30910-155116-2.mp4'

input_stream = ffmpeg.input(input_file)
output_stream = ffmpeg.output(input_stream, output_file)

ffmpeg.run(output_stream)