# YouTube Video Recorder and Uploader with Night Vision on Raspberry Pi
#
# Raspberry Pi 3B+
# 
# By Kutluhan Aktar
#
# Develop a GUI to record videos with the selected image settings and effects and upload them to your YouTube channel
# with the given parameters (description, title, category, e.g.,).
# 
# Get more information on the project page:
# https://theamplituhedron.com/projects/YouTube-Video-Recorder-and-Uploader-GUI-with-Night-Vision-on-Raspberry-Pi/


from guizero import App, Box, Text, TextBox, PushButton, ButtonGroup, Combo, Slider, ListBox, MenuBar, info
from picamera import PiCamera
from time import sleep
from subprocess import call, Popen
import datetime
import webbrowser
import glob

# Create the YouTube_Recorder_Uploader class with the required settings:
class YouTube_Recorder_Uploader:
    def __init__(self, r_x, r_y, framerate):
        # Define the camera module settings.
        self.camera = PiCamera()
        self.camera.resolution = (r_x, r_y)
        self.camera.framerate = framerate
    def open_folder(self):
        # Open the parent folder to inspect videos.
        webbrowser.open("//home//pi//YouTube-Recorder-and-Uploader//")
    def about(self):
        # Define the information box.
        info('About', 'Learn how create a GUI by which you can record videos with the selected image settings and upload them to your YouTube channel using Google API (YouTube Data v3) with the given parameters :)')
    def tutorial(self):
        # Go to the project tutorial page.
        webbrowser.open("https://theamplituhedron.com/projects/YouTube-Video-Recorder-and-Uploader-GUI-with-Night-Vision-on-Raspberry-Pi/")
    def get_existing_videos(self):
        # Get the mp4 videos in the Recorded folder to be able to select a video to upload or play via this GUI.
        files = [f for f in glob.glob("/home/pi/YouTube-Recorder-and-Uploader/Recorded/*.mp4")]
        # Insert new list to the ListBox and remove the old items.
        u_select_input.clear()
        for f in files:
            u_select_input.append(f)
    def show_selected_video(self):
        # Create a pop-up including the selected video.
        info("Selected Video", u_select_input.value)
    def record(self):
        # Get the current date as the timestamp to generate unique file names.
        date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
        # Get the entered video settings to record a video.
        filename = r_name_input.value[:-1]
        annotate = r_annotate_input.value[:-1]
        effect = r_effect_input.value
        duration = r_duration_input.value
        # Define video file path and location.
        path = '/home/pi/YouTube-Recorder-and-Uploader/Recorded/'
        video_h264 = path + filename + '-' + date + '.h264'
        video_mp4 = path + filename + '-' + date + '.mp4'
        # Record a video with the given settings.
        print("\r\nRecording Settings:\r\nLocation => " + video_h264 + "\r\nAnnotate => " + annotate + "\r\nEffect => " + effect + "\r\nDuration => " + str(duration))
        self.camera.annotate_text = annotate
        self.camera.image_effect = effect
        self.camera.start_preview()
        self.camera.start_recording(video_h264)
        sleep(int(duration))
        self.camera.stop_recording()
        self.camera.stop_preview()
        print("Rasp_Pi => Video Recorded! \r\n")
        # Convert the h264 format to the mp4 format to upload videos in mp4 format to YouTube.
        command = "MP4Box -add " + video_h264 + " " + video_mp4
        call([command], shell=True)
        print("\r\nRasp_Pi => Video Converted! \r\n")
        # Update the video list after recording a new video.
        self.get_existing_videos()
    def upload(self):
        # Get the entered YouTube video parameters (title, description, e.g.,).
        title = u_title_input.value
        description = u_description_input.value
        keywords = u_keywords_input.value
        category = u_category_input.value
        privacy = u_privacy_input.value
        selected_video = u_select_input.value
        # Print the given uploading settings (parameters).
        print("\r\nYouTube Uploading Settings:\r\nTitle => " + title + "Description => " + description + "Keywords => " + keywords + "Category => " + category + "\r\nPrivacy Status => " + privacy + "\r\nSelected Video => " + selected_video)
        # Upload video to the registered YouTube account by transferring uploading settings to the upload_video.py file.
        command = (
           'sudo python /home/pi/YouTube-Recorder-and-Uploader/upload_video.py --file="'+ selected_video
         + '" --title="' + title[:-1]
         + '" --description="' + description[:-1]
         + '" --keywords="' + keywords[:-1]
         + '" --category="' + category
         + '" --privacyStatus="' + privacy + '"'
        )
        print("\r\nTerminal Command => " + command + "\r\n")
        call([command], shell=True)
        print("\r\nRasp_Pi => Attempted to upload the selected video via Google Client API! \r\n")
    def play(self):
        # Play the selected video using omxplayer.
        print("\r\nRasp_Pi => Selected Video Played on the omxplayer! \r\n")
        selected_video = u_select_input.value
        omxplayer = Popen(['omxplayer',selected_video])
      
        
# Define a new class object named as 'video'.
video = YouTube_Recorder_Uploader(800, 600, 15)
        
# Create the YouTube Video Recorder and Uploader GUI:
appWidth = 1024
appHeight = 600
app = App(title="YouTube Video Recorder and Uploader", bg="#1F2020", width=appWidth, height=appHeight)
# Define menu bar options.
menubar = MenuBar(app, toplevel=["Files", "About"],
                  options=[
                      [ ["Open In Folder", video.open_folder] ],
                      [ ["Tutorial", video.tutorial], ["Information", video.about] ]
                  ])
# Design the application interface.
app_header = Box(app, width="fill", height=50, align="top")
app_header_text = Text(app_header, text="YouTube Video Recorder and Uploader", color="white", size=20)
app_record = Box(app, width="fill", height="fill", layout="grid", align="left")
app_upload = Box(app, width="fill", height="fill", layout="grid", align="right")
app_upload.bg = "#A5282C"
# Create the record menu to be able to change the video settings.
r_name_label = Text(app_record, text="Filename : ", color="#A5282C", size=15, grid=[0,0], align="left")
r_name_input = TextBox(app_record, width=40, grid=[1,0], height=2, multiline=True)
r_name_input.bg = "#A5282C"
r_name_input.text_color = "white"
r_annotate_label = Text(app_record, text="Annotate : ", color="#A5282C", size=15, grid=[0,1], align="left")
r_annotate_input = TextBox(app_record, width=40, grid=[1,1], height=2, multiline=True)
r_annotate_input.bg = "#A5282C"
r_annotate_input.text_color = "white"
r_effect_label = Text(app_record, text="Image Effect : ", color="#A5282C", size=15, grid=[0,2], align="left")
r_effect_input = Combo(app_record, grid=[1,2], align="right", options=["none", "negative", "solarize", "sketch", "pastel", "watercolor", "film", "blur", "saturation", "posterise", "cartoon", "colorpoint", "colorbalance"], selected="none")
r_effect_input.bg = "#A5282C"
r_effect_input.text_color = "white"
r_effect_input.text_size = 20
r_duration_label = Text(app_record, text="Duration : ", color="#A5282C", size=15, grid=[0,3], align="left")
r_duration_input = Slider(app_record, end=250, grid=[1,3], align="right")
r_duration_input.bg = "#A5282C"
r_duration_input.text_color = "white"
r_duration_input.text_size = 20
r_submit = PushButton(app_record, text="Record", width=10, grid=[0,4], command=video.record, padx=15, pady=15)
r_submit.bg = "#A5282C"
r_submit.text_color = "white"
r_submit.text_size = 25
# Create the upload menu to be able to upload the selected video with the given parameters to YouTube.
u_title_label = Text(app_upload, text="Title : ", color="#F3D060", size=15, grid=[0,0], align="left")
u_title_input = TextBox(app_upload, grid=[1,0], width=35, height=2, multiline=True)
u_title_input.bg = "#F3D060"
u_title_input.text_color = "white"
u_description_label = Text(app_upload, text="Description : ", color="#F3D060", size=15, grid=[0,1], align="left")
u_description_input = TextBox(app_upload, grid=[1,1], width=35, height=2, multiline=True)
u_description_input.bg = "#F3D060"
u_description_input.text_color = "white"
u_keywords_label = Text(app_upload, text="Keywords : ", color="#F3D060", size=15, grid=[0,2], align="left")
u_keywords_input = TextBox(app_upload, grid=[1,2], width=35, height=2, multiline=True)
u_keywords_input.bg = "#F3D060"
u_keywords_input.text_color = "white"
u_category_label = Text(app_upload, text="Category : ", color="#F3D060", size=15, grid=[0,3], align="left")
# You can find more information regarding the YouTube category numbers on the project page.
u_category_input = Combo(app_upload, grid=[1,3], align="right", options=["22", "1", "10", "20", "21", "23", "24", "25", "26", "27", "28", "30"], selected="22")
u_category_input.bg = "#F3D060"
u_category_input.text_color = "white"
u_category_input.text_size = 20
u_privacy_label = Text(app_upload, text="Privacy Status : ", color="#F3D060", size=15, grid=[0,4], align="left")
u_privacy_input = ButtonGroup(app_upload, grid=[1,4], horizontal=True, align="right", options=["public", "private", "unlisted"], selected="private")
u_privacy_input.bg = "#F3D060"
u_privacy_input.text_color = "white"
u_privacy_input.text_size = 12
u_select_label = Text(app_upload, text="Select a Video : ", color="#F3D060", size=15, grid=[0,5], align="left")
# Get the paths of the recorded videos in the Recorded folder.
u_select_input = ListBox(app_upload, grid=[1,5], align="right", width=200, height=150, command=video.show_selected_video, items=["none"], scrollbar=True)
video.get_existing_videos()
u_select_input.bg = "#F3D060"
u_select_input.text_color = "white"
u_select_input.text_size = 15
u_p_submit = PushButton(app_upload, text="Play", grid=[0,6], align="left", command=video.play, padx=30, pady=10)
u_p_submit.bg = "#F3D060"
u_p_submit.text_color = "white"
u_p_submit.text_size = 25
u_u_submit = PushButton(app_upload, text="Upload", grid=[0,7], align="left", command=video.upload, padx=15, pady=10)
u_u_submit.bg = "#F3D060"
u_u_submit.text_color = "white"
u_u_submit.text_size = 25
# Initiate the application loop.
app.display()