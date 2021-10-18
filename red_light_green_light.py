#!/usr/bin/env python3

import anki_vector
from anki_vector.util import degrees, Angle, Pose
from anki_vector.events import Events
import time
#from serials import (N7N9, K1X1)
import random
import os
from PIL import Image
import sys

#random time to wait between stages
r = random.randint(1,3)
#generates a random number for the player, to keep it authentic, could use registered faces instead in future iterations?
player = random.randint(1,456)

detected = False

def test_subscriber(robot, event_type, event):
    for face in robot.world.visible_faces:
        robot.events.unsubscribe(test_subscriber, Events.robot_observed_face)
        detection()
        
def detection():
    global detected
    if not detected:
        detected = True
        print("I see a face")
#       this line sends a signal to turn on my laser, replace this line with an action you want carried out on detection
        os.system("ssh 'pi@192.168.0.102' /var/www/rfoutlet/codesend 11063192 -l 600 -p 6")
        robot.behavior.say_text(f"Player moved. Player :{player} eliminated")
        time.sleep(2)
#        this line sends a signal to turn off my laser, replace this line with the action you want cancelled after detection
        os.system("ssh 'pi@192.168.0.102' /var/www/rfoutlet/codesend 11063188 -l 600 -p 6")
        detected = False
        print("detected = False")
        green_light()

def red_light():
    global detected
    if not detected:
        print("Red Light")
        robot.behavior.say_text("Red Light")
        robot.behavior.turn_in_place(degrees(180))
        robot.events.subscribe(test_subscriber, Events.robot_observed_face)
        robot.behavior.set_eye_color(0.00, 1.00)
        time.sleep(r)
        green_light()
    
def green_light():
    global detected
    if not detected:
        print("Green Light")
        robot.behavior.turn_in_place(degrees(180))
        robot.behavior.set_eye_color(0.39, 1.00)
        
        robot.behavior.say_text("Green Light")
        robot.audio.stream_wav_file("rlgl_audio_short.wav")
        if (robot.touch.last_sensor_reading.is_being_touched):
            print("Touch Registered")
            robot.behavior.turn_in_place(degrees(180))
            robot.behavior.say_text("You Won!")
            robot.anim.play_animation_trigger('PounceWProxForward')
            robot.behavior.say_text("Play again?")
            time.sleep(2)
            if (robot.touch.last_sensor_reading.is_being_touched):
                print("Touch Registered")
                red_light()
            else:
                sys.exit()
        else:
            red_light()

#with anki_vector.Robot(N7N9, enable_face_detection=True) as robot:
with anki_vector.Robot(enable_face_detection=True) as robot:
    image_file1 = Image.open('squid_1.jpg')
    screen_data1 = anki_vector.screen.convert_image_to_screen_data(image_file1)
    image_file2 = Image.open('squid_2.jpg')
    screen_data2 = anki_vector.screen.convert_image_to_screen_data(image_file2)
    image_file3 = Image.open('squid_3.jpg')
    screen_data3 = anki_vector.screen.convert_image_to_screen_data(image_file3)

    robot.behavior.set_lift_height(0.0)
    robot.behavior.set_head_angle(anki_vector.util.degrees(33.0))
    robot.screen.set_screen_with_image_data(screen_data3, 3.0)
    robot.screen.set_screen_with_image_data(screen_data2, 2.5)
    robot.screen.set_screen_with_image_data(screen_data1, 6.0)
    robot.audio.stream_wav_file("rlgl_audio.wav")
    print("Lets play red light, green light")
    robot.behavior.say_text("Lets play red light, green light")
    robot.behavior.drive_off_charger()
    green_light()
    try:
        time.sleep(10000)
    except KeyboardInterrupt:
        robot.disconnect()