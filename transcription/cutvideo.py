# Import everything needed to edit video clips  
from moviepy.editor import *
     
# loading video dsa gfg intro video  
clip = VideoFileClip("Sample01.mp4")  
      
# getting only first 2:30   
clip = clip.subclip(0, 150)  
# clip = clip.subclip(150, 300)  

# saving the clip
clip.write_videofile("output01.mp4")
