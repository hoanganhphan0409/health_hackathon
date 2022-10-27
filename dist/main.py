import cv2
import mediapipe as mp
from utils import *
from tkinter import filedialog
from datetime import datetime

def main_function(device = 'CAMERA_LAPTOP',url =''):
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d%m_%Y_%Hh%Mm%Ss")
    name_video = f"resources\good_posture\{dt_string}.mp4"

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_pose = mp.solutions.pose

    # Initialize frame counters.
    good_frames = 0
    bad_frames = 0

    # Font type.
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Colors.
    blue = (255, 127, 0)
    red = (50, 50, 255)
    green = (127, 255, 0)
    dark_blue = (127, 20, 0)
    light_green = (127, 233, 100)
    yellow = (0, 255, 255)
    pink = (255, 0, 255)

    if device == 'CAMERA_LAPTOP':
        cap = cv2.VideoCapture(0)
    elif device == 'VIDEO':
        try:
            file_path = filedialog.askopenfilename()
            cap = cv2.VideoCapture(file_path)
        except: return

    elif device == 'CAMERA_PHONE':
        try:
            cap = cv2.VideoCapture(url)
        except:
            print('wrong url')
            return
    # Meta
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    size = (frame_width, frame_height)

    # Below VideoWriter object will create
    # a frame of above defined The output
    # is stored in 'filename.avi' file.
    result = cv2.VideoWriter(name_video,
                            cv2.VideoWriter_fourcc(*'MP4V'),
                            10, size)


    with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                if device == 'VIDEO':
                    cv2.destroyAllWindows()
                    return
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image)

            # Draw the pose annotation on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            #image = cv2.resize(image, (1080, 1920))
            h, w = image.shape[:2]
            # mp_drawing.draw_landmarks(
            #     image,
            #     results.pose_landmarks,
            #     mp_pose.POSE_CONNECTIONS,
            #     landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            lm = results.pose_landmarks
            if lm is not None:
                lmPose = mp_pose.PoseLandmark

                # Left shoulder.
                l_shldr_x = int(lm.landmark[lmPose.LEFT_SHOULDER].x * w)
                l_shldr_y = int(lm.landmark[lmPose.LEFT_SHOULDER].y * h)

                # Right shoulder.
                r_shldr_x = int(lm.landmark[lmPose.RIGHT_SHOULDER].x * w)
                r_shldr_y = int(lm.landmark[lmPose.RIGHT_SHOULDER].y * h)

                # Left ear.
                l_ear_x = int(lm.landmark[lmPose.LEFT_EAR].x * w)
                l_ear_y = int(lm.landmark[lmPose.LEFT_EAR].y * h)

                # Left hip.
                l_hip_x = int(lm.landmark[lmPose.LEFT_HIP].x * w)
                l_hip_y = int(lm.landmark[lmPose.LEFT_HIP].y * h)

                # Calculate distance between left shoulder and right shoulder points.
                offset = findDistance(l_shldr_x, l_shldr_y, r_shldr_x, r_shldr_y)

                # Assist to align the camera to point at the side view of the person.
                # Offset threshold 30 is based on results obtained from analysis over 100 samples.
                if offset < 100:
                    cv2.putText(image, str(int(offset)) + ' Aligned', (w - 140, 30), font, 0.7, green, 2)
                else:
                    cv2.putText(image, str(int(offset)) + ' Not Aligned', (w - 200, 30), font, 0.7, red, 2)

                # Calculate angles.
                neck_inclination = findAngle(l_shldr_x, l_shldr_y, l_ear_x, l_ear_y)
                torso_inclination = findAngle(l_hip_x, l_hip_y, l_shldr_x, l_shldr_y)

                # Draw landmarks.
                cv2.circle(image, (l_shldr_x, l_shldr_y), 7, yellow, -1)
                cv2.circle(image, (l_ear_x, l_ear_y), 7, yellow, -1)

                # Let's take y - coordinate of P3 100px above x1,  for display elegance.
                # Although we are taking y = 0 while calculating angle between P1,P2,P3.
                cv2.circle(image, (l_shldr_x, l_shldr_y - 100), 7, yellow, -1)
                cv2.circle(image, (r_shldr_x, r_shldr_y), 7, pink, -1)
                cv2.circle(image, (l_hip_x, l_hip_y), 7, yellow, -1)

                # Similarly, here we are taking y - coordinate 100px above x1. Note that
                # you can take any value for y, not necessarily 100 or 200 pixels.
                cv2.circle(image, (l_hip_x, l_hip_y - 100), 7, yellow, -1)

                # Put text, Posture and angle inclination.
                # Text string for display.
                angle_text_string = 'Neck: ' + str(int(neck_inclination)) + '  Torso: ' + str(int(torso_inclination))

                # Determine whether good posture or bad posture.
                # The threshold angles have been set based on intuition.
                if neck_inclination < 18 and torso_inclination < 12:
                    bad_frames = 0
                    good_frames += 1
                    if device != 'VIDEO':
                        cv2.putText(image, angle_text_string, (10, 30), font, 0.7, dark_blue, 2)
                        cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.7, light_green, 2)
                        cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.7, light_green, 2)

                    # Join landmarks.
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), green, 4)
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), green, 4)
                    cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), green, 4)
                    cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), green, 4)
                    result.write(image)

                else:
                    good_frames = 0
                    bad_frames += 1
                    if device != 'VIDEO':
                        cv2.putText(image, angle_text_string, (10, 30), font, 0.7, dark_blue, 2)
                        cv2.putText(image, str(int(neck_inclination)), (l_shldr_x + 10, l_shldr_y), font, 0.7, red, 2)
                        cv2.putText(image, str(int(torso_inclination)), (l_hip_x + 10, l_hip_y), font, 0.7, red, 2)

                    # Join landmarks.
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_ear_x, l_ear_y), red, 4)
                    cv2.line(image, (l_shldr_x, l_shldr_y), (l_shldr_x, l_shldr_y - 100), red, 4)
                    cv2.line(image, (l_hip_x, l_hip_y), (l_shldr_x, l_shldr_y), red, 4)
                    cv2.line(image, (l_hip_x, l_hip_y), (l_hip_x, l_hip_y - 100), red, 4)

                # Calculate the time of remaining in a particular posture.
                good_time = (1 / fps) * good_frames
                bad_time = (1 / fps) * bad_frames

                # Pose time.
                if good_time > 0:
                    time_string_good = 'Good Posture Time: ' + str(round(good_time, 1)) + 's'
                    if device != 'VIDEO':
                        cv2.putText(image, time_string_good, (7, h - 15), font, 0.7, green, 2)
                else:
                    time_string_bad = 'Bad Posture Time: ' + str(round(bad_time, 1)) + 's'
                    if device != 'VIDEO':
                        cv2.putText(image, time_string_bad, (7, h - 15), font, 0.7, red, 2)

                # If you stay in bad posture for more than 3 minutes (180s) send an alert.
                if bad_time > 180:
                    sendWarning()

                cv2.putText(image,'Press Q to exit',(w-180,h-15),font,0.7,yellow,2)
            # Flip the image horizontally for a selfie-view display.
            window = 'MediaPipe Pose'
            cv2.namedWindow(window, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(window, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            # cv2.imshow('MediaPipe Pose', cv2.flip(image, 0))
            cv2.imshow(window, image)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
    result.release()
    cap.release()

#main_function('CAMERA_LAPTOP')