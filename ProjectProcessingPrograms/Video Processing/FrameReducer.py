from moviepy.editor import *

# Input and output video paths
path = "Source/Edited.mp4"
pathOutput = "Short/OreToolsFPS6.mp4"

# Reading input video
clip = VideoFileClip(path)
# Setting its fps
clip = clip.set_fps(6)
#Saving the Video with change FPS
clip.write_videofile(pathOutput)
# Reading the saved image to check fps
output = VideoFileClip(pathOutput)
clip = VideoFileClip(path)
# Output results
print("Input Video Frame rate = ",clip.fps)
print("Output Video Frame rate = ",output.fps)