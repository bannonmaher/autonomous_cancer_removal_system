# Copyright and patents pending Jonathan Bannon Maher Corporation
# Inventor and author Jonathan Bannon Maher
# This software, when operating corresponding disclosed hardware,
# provides for the autonomous surgical removal of targeted cells including cancer,
# through artificial intelligence,
# while potentially leaving in tact all healthy cells.


# import the created image processing library

from image_processing import image_processing

# import a library for three dimensional arrays

import numpy as np

# import a library for system resource access

import sys

# import a library to connecting to the relay

import telnetlib

# import a library to pause program execution

import time

# import a library for accessing http resources

import urllib

# create variables holding the relay on off values

off = 0
on = 1

# create variables holding the relay board connection, IP address, username, and password

relay = None
relay_ip = "127.0.0.1"
relay_username = "admin"
relay_password = "admin"

# create variables holding the state of each relay on the relay board

relay_1_motor_vertical_1_1 = off
relay_2_motor_vertical_1_2 = off
relay_3_motor_vertical_2_1 = off
relay_4_motor_vertical_2_2 = off
relay_5_motor_rotational_1_1 = off
relay_6_motor_rotational_1_2 = off
relay_7_motor_rotational_2_1 = off
relay_8_motor_rotational_2_2 = off
relay_9_motor_arm_1_1 = off
relay_10_motor_arm_1_2 = off
relay_11_motor_arm_2_1 = off
relay_12_motor_arm_2_2 = off
relay_13_motor_head_1_1 = off
relay_14_motor_head_1_2 = off
relay_15_motor_head_2_1 = off
relay_16_motor_head_2_2 = off
relay_17_motor_blade_forward = off
relay_18_motor_blade_backward = off
relay_19_motor_suction_state = off

# create variables holding the step motor step millimeters, degrees, and seconds

motor_step_millimeters = 0.1
motor_step_degrees = 1.6
motor_step_seconds = 0.2

# initialize variables to hold the settings and log file

settings = None
log_file = None

# create variables holding the pixel minimum percent match for extraction,
# and the minimum image and shape percent match

pixel_minimum_percent_match = .05
match_threshold = .85

# initialize variables to hold the current color, shape, or image matching against,
# the current degree rotation, current degree flexion,
# and whether or not a match has been found in the current position

match_found = True
image_current = None
shape_current = 0
color_current = 0
degree_rotation_current = 0
degree_flexion_current = 0

# initialize a three dimensional array to hold the status of the tissue at each point

tissue_coordinates_array = np.zeros((1000,1000,1000))

# create variables for the values indicating tissue is good or bad

tissue_good = 1
tissue_bad = -1

# initialize variables to hold the current x, y, and z of the head unit

tissue_current_x = 0
tissue_current_y = 0
tissue_current_z = 0

# read the lines of the settings file into an array

settings_file_name = sys.argv[1]
settings_file = open(settings_file_name, "r")
settings_file_lines = settings_file.readlines()
settings_file.close()

# open the log file

log_file = open("log.txt","w+")

# create variables holding the camera IP address, username, and password

camera_ip = "127.0.0.2"
camera_username = "admin"
camera_password = "admin"


# create a function to update the relay board, first establishing a connection to the relay board,
# if it has not been initialized, or has been dropped, then creating a string sequence of relay states,
# and sending the states to the relay board

def update_relay():

    if not relay:
        relay = telnetlib.Telnet(relay_ip, 23)
        relay.read_until(b"User Name: ") 
        relay.write(
            relay_username.encode('ascii') + b"\n")
        relay.read_until(b"Password: ")
        relay.write(relay_password.encode('ascii') + b"\n")

    command = str(relay_1_motor_vertical_1_1)
    command+= str(relay_2_motor_vertical_1_2)
    command+= str(relay_3_motor_vertical_2_1)
    command+= str(relay_4_motor_vertical_2_2)
    command+= str(relay_5_motor_rotational_1_1)
    command+= str(relay_6_motor_rotational_1_2)
    command+= str(relay_7_motor_rotational_2_1)
    command+= str(relay_8_motor_rotational_2_2)
    command+= str(relay_9_motor_arm_1_1)
    command+= str(relay_10_motor_arm_1_2)
    command+= str(relay_11_motor_arm_2_1)
    command+= str(relay_12_motor_arm_2_2) 
    command+= str(relay_13_motor_head_1_1)
    command+= str(relay_14_motor_head_1_2)
    command+= str(relay_15_motor_head_2_1)
    command+= str(relay_16_motor_head_2_2) 
    command+= str(relay_17_motor_blade_forward)
    command+= str(relay_18_motor_blade_backward)
    command+= str(relay_19_motor_suction_state)
    relay.write(command.encode('ascii') + b"\n")


# create a function that when called moves the embodiment in by providing power to the
# corresponding relay attached step motor in the sequence that will move it as desired
# by one full step sequence

def move_in():
    relay_1_motor_vertical_1_1 = on
    update_relay()
    time.sleep(motor_step_seconds)
    relay_1_motor_vertical_1_1 = off
    relay_2_motor_vertical_2_1 = on
    update_relay()
    time.sleep(motor_step_seconds)
    relay_2_motor_vertical_2_1 = off
    relay_4_motor_vertical_2_2 = on
    update_relay()
    time.sleep(motor_step_seconds)
    relay_4_motor_vertical_2_2 = off
    relay_3_motor_vertical_2_1 = on
    update_relay()
    time.sleep(motor_step_seconds)
    relay_3_motor_vertical_2_1 = off
    update_relay()


# create a function that when called moves the embodiment out by providing power to the
# corresponding relay attached step motor in the sequence that will move it as desired
# by one full step sequence

def move_out():
    relay_4_motor_vertical_2_2 = on
    update_relay()
    time.sleep(motor_step_seconds)
    relay_4_motor_vertical_2_2 = off
    relay_2_motor_vertical_1_2 = on
    update_relay()
    time.sleep(motor_step_seconds)
    relay_2_motor_vertical_1_2 = off
    relay_2_motor_vertical_2_1 = on
    update_relay()
    time.sleep(motor_step_seconds)
    relay_2_motor_vertical_2_1 = off
    relay_1_motor_vertical_1_1 = on
    update_relay()
    time.sleep(motor_step_seconds)
    relay_1_motor_vertical_1_1 = off
    update_relay()


# create a function that when called rotates the embodiment forward by providing power to the
# corresponding relay attached step motor in the sequence that will move it as desired
# by one full step sequence

def rotate_forward(requested_degrees):
    current_degrees = 0
    while current_degrees < requested_degrees:
        relay_5_motor_rotational_1_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_5_motor_rotational_1_1 = off
        relay_6_motor_rotational_2_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_6_motor_rotational_2_1 = off
        relay_8_motor_rotational_2_2 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_8_motor_rotational_2_2 = off
        relay_7_motor_rotational_2_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_7_motor_rotational_2_1 = off
        update_relay()
        current_degrees += motor_step_degrees*4


# create a function that when called rotates the embodiment backward by providing power to the
# corresponding relay attached step motor in the sequence that will move it as desired 
# by one full step sequence

def rotate_backward(requested_degrees):
    current_degrees = 0
    while current_degrees < requested_degrees:
        relay_8_motor_rotational_2_2 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_8_motor_rotational_2_2 = off
        relay_6_motor_rotational_1_2 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_6_motor_rotational_1_2 = off
        relay_7_motor_rotational_2_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_7_motor_rotational_2_1 = off
        relay_5_motor_rotational_1_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_5_motor_rotational_1_1 = off
        update_relay()
        current_degrees += motor_step_degrees*4


# create a function that when called moves the embodiment arm forward by the degrees in the function parameter
# by providing power to the corresponding relay attached step motor in the sequence
# that will move it as desired by full step sequences until the desired degrees have been achieved

def flex_forward(requested_degrees):
    current_degrees = 0
    while current_degrees < requested_degrees:
        relay_9_motor_arm_1_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_9_motor_arm_1_1 = off
        relay_11_motor_arm_2_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_11_motor_arm_2_1 = off
        relay_12_motor_arm_2_2 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_12_motor_arm_2_2 = off
        relay_10_motor_arm_2_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_10_motor_arm_2_1 = off
        update_relay()
        current_degrees += motor_step_degrees*4


# create a function that when called moves the embodiment arm backward by the degrees in the function parameter
# by providing power to the corresponding relay attached step motor in the sequence
# that will move it as desired by one full step sequence

def flex_backward(requested_degrees):
    current_degrees = 0
    while current_degrees < requested_degrees:
        relay_12_motor_arm_2_2 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_12_motor_arm_2_2 = off
        relay_10_motor_arm_1_2 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_10_motor_arm_1_2 = off
        relay_11_motor_arm_2_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_11_motor_arm_2_1 = off
        relay_9_motor_arm_1_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_9_motor_arm_1_1 = off
        update_relay()
        current_degrees += motor_step_degrees*4


# create a function that when called moves the embodiment head forward by the degrees specified in the parameter
# by providing power to the corresponding relay attached step motor in the sequence that will
# move it as desired by full step sequences until the desired angle is achieved

def head_forward(requested_degrees):
    current_degrees = 0
    while current_degrees < requested_degrees:
        relay_13_motor_head_1_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_13_motor_head_1_1 = off
        relay_15_motor_head_2_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_15_motor_head_2_1 = off
        relay_16_motor_head_2_2 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_16_motor_head_2_2 = off
        relay_14_motor_head_2_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_14_motor_vertical_2_1 = off
        update_relay()
        current_degrees += motor_step_degrees*4


# create a function that when called moves the embodiment head backward by the degrees specified in the parameter
# by providing power to the corresponding relay attached step motor in the sequence that will
# move it as desired by one full step sequence

def head_backward(requested_degrees):
    current_degrees = 0
    while current_degrees < requested_degrees:
        relay_16_motor_head_2_2 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_16_motor_head_2_2 = off
        relay_14_motor_head_1_2 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_14_motor_head_1_2 = off
        relay_15_motor_head_2_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_15_motor_head_2_1 = off
        relay_13_motor_head_1_1 = on
        update_relay()
        time.sleep(motor_step_seconds)
        relay_13_motor_head_1_1 = off
        update_relay()
        current_degrees += motor_step_degrees*4


# create a function that when called turns the suction machine on then operates the motor 
# connected to the blade wire to move the blade back and forth to cut the tissue,
# then turns the suction machine off

def suction_cut():
    relay_19_suction_state = on
    update_relay()
    time.sleep(.25)
    relay_17_motor_cut_forward = on
    update_relay()
    time.sleep(.5)
    relay_17_motor_cut_forward = off
    relay_18_motor_cut_backward = on
    update_relay()
    time.sleep(.5)
    relay_18_motor_cut_backward = off
    update_relay()
    time.sleep(.25)
    relay_19_suction_state = off
    update_relay()


# create a function to take a snapshot from the camera

def snapshot():

    # access the current camera image

    camera_image_url = "http://%/?username=%&password=%" (camera_ip, camera_username, camera_password)
    camera_image = urllib2.urlopen(camera_image_url).read()

    # write the current camera image to a file so that its accessible to the both the system
    # and the user interface

    image_file = open("snapshot.jpg","wb")
    image_file.write(image)
    image_file.close()


# define a function to process the tissue at the current location

def process():

    # retrieve the current camera image

    camera_image_url = "http://%/?username=%&password=%" (camera_ip, camera_username, camera_password)
    camera_image = urllib2.urlopen(camera_image_url).read()

    # initialize a variable specifying if a match was found

    match_found = False

    # iterate through each setting

    for setting in settings:

        # create a variable for whether or not to remove the tissue if there's a match
        # and set it to the value from the setting

        remove = False
        if setting.find("remove"):
            remove = True

        # create a variable holding the setting match string

        match_string = setting[0]

        # create a variable for the match method and with a default of image recognition

        recognition_method = "image"

        # if the match string contains coordinates set the recognition method to shape

        if setting.find(",") > -1:
            recognition_method = "shape"

        # if the match string doesn't contain an image file or coordinates set the recognition method to color

        if setting.find(",") == -1 and setting.find(".") ==-1:
            recognition_method = "color"

        # split the setting by spaces to an array

        setting = setting.split(" ")

        # if the recognition mode is color, send the image to the function that checks if the color
        # in the setting exists in the image

        if recognition == "color":
            match_found = image_processing.image_contains_color(camera_image, color, match_threshold)

        # if the recognition mode is shape, send the image to the function that checks if the shape
        # in the setting exists in the image

        if recognition == "shape":
            match_found = image_processing.image_contains_shape(camera_image, setting[0])

        # if the recognition mode is image, check if the image in the setting exists in the image

        if recognition == "image":
            match_found  = image_processing.image_contains_image(current_image, image_file)

        # if a match was found, save the image to an incrementally numbered file and record the time,
        # file name, and setting, to the log file

        if match_found:
            image_file_name = "image-" + image_counter + ".jpg"
            image_file = open(image_file_name, "wb")
            image_file.write(camera_image)
            image_file.close()
            log_file_line = str(sys.time()) + " " + image_file_name + " " + setting

            # record the status of the tissue at the current x, y, z as bad

            coordinates_array[x,y,z] = tissue_bad

            # if the tissue match is to be removed according to the setting, call the function
            # to suction cut the tissue

            if remove:
                suction_cut()

        # if the no match was found, record the status of the tissue at the current x, y, z as good

        if not match_found:
            coordinates_array [x,y,z] = tissue_good


# create a function that allows the embodiment to extract tissue in an automated manner
# through image recognition, where if moving horizontally on x,
# and a point before that horizontally is clear x with the same y and z, skip=true to next point,
# if moving vertically and point before vertically, skip to next point,
# also for rotating, point array is of .2 mm increments as determined by stepper motors

def autonomous():

    # create variable that holds whether or not a match was found by retrieving the result of the function
    # to process tissue at the current location

    match_found = process()

    # while a match was found move in, while incrementing the y position of the embodiment,
    # and then setting whether or not a current match was found by calling the function to process tissue
    # at the current location

    while match_found:
        move_in()
        tissue_current_y += 1
        match_found = process()

        # move the embodiment head forward 90 degrees

        head_forward(90)
        tissue_x_current += 1
        rotation_current = 0

        # continue while the current arm rotation degree is less than one revolution,
        # then return the embodiment to zero degrees of rotation

        while rotation_current < 360:
            rotate_forward(45)
            rotation_current +=45

            # proceed while the y position is not equal to the point of origin

            while tissue_current_y >= 0:
                move_out()
                tissue_current_y -= 1
                match_found = process()

                # proceed while the current arm flexion degree is less than one revolution,
                # then return the embodiment to zero degrees of rotation

                while flexion_current < 360:
                    flex_forward(45)
                    flexion_current += 45
                    found = process()
                    flex_backward(360)


# create a function to provide manual operation of the embodiment

def manual(action):

    # if the action requested is to move in call the function to do so

    if action == "move_in":
                    move_in()

    # if the action requested is to move out call the function to do so

    if action == "move_out":
        move_out()

    # if the action requested is to flex forward call the function to do so


    if action == "flex_forward":
        flex_forward(motor_step_degrees)

    # if the action requested is to flex backward call the function to do so

    if action == "flex_backward":
        flex_backward(motor_step_degrees)

    # if the action requested is to rotate forward call the function to do so

    if action == "rotate_forward":
        rotate_forward(motor_step_degrees)

    # if the action requested is to rotate backward call the function to do so

    if action == "rotate_backward":
        rotate_backward(motor_step_degrees)

    # if the action requested is to move the head forward call the function to do so

    if action == "head_forward":
        head_forward(motor_step_degrees)

    # if the action requested is to move the head backward call the function to move in

    if action == "head_backward":
        head_backward(motor_step_degrees)

    # if the action requested is to suction cut call the function to do so

    if action == "suction_cut":
        suction_cut()


# create a function to be called  upon program execution

def main():

    # retrieve any command line arguments, including  the settings file name, the log file name,
    # and any requested embodiment action

    parameters = sys.argv
    settings_file_name = ""
    log_file_name = ""
    try:
        settings_file_name = parameter[1]
        log_file_name = parameter[2]
        action = parameter[3]
    except:
        pass

    # if the setting file name was named snapshot, then call the function that saves a picture
    # of the current embodiment camera image

    if settings_file_name  == "snapshot":
        snapshot()

    # proceed if the a snapshot was not specified

    else:

        # open the log file to record unit operation

        log_file = open(log_file_name, "w+")

        # if the request to the embodiment was to perform a manually action,
        # send that action to the function that performs manual actions

        if settings_file_name == "manual":
            if action:
                manual(action)

        # if the embodiment is be operated autonomously, retrieve the settings file,
        # and call the function to begin autonomous operation

        else:
            settings = open(settings_file_name,"r").split("\n")
            autonomous()

