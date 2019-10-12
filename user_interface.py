# Copyright and Patents Pending Jonathan Bannon Maher Corporation
# Inventor and author Jonathan Bannon Maher
# User interface for optional local or remote monitoring and human control


# import the libraries for http post and get

from flask import Flask
from flask import request
from flask import Response

# import the library for system resource access

import os

# define a function to provide control of the system though http and a web browser
# that is executed when the server is called through http

@application.route('/*', methods=['GET'])
def remote():

# create a variable holding any command provided with the http request

    command = get_args("command")

# if there was a command, build the command line call to the operating script

    if command:
        call = "python run.py "

# if the command is autonomous, append autonomous to the command line call

        if command == "autonomous":
            call+= "autonomous"

# if the command isn't autonomous, append manual to the command line call then append the user command

        else:
            call+= "manual " + command

# execute the command line call

        os.execute(call)

# create an array of available commands

    commands = ["autonomous", "in", "out", "forward",
        "backward", "rotate right", "rotate left"]

# create a variable to hold the display output

    output = "<html><meta refresh=5>"

# for each command, generate a link that will call this application through http with the command
# and add the link to the output

    for command in commands:
        output+= "<a href=\"/?command="
        + command + "\">" + command + "</a>"

# add the last image retrieved by the system to the user display

    output += "<img src=/current_image.jpg>"

# display the output the user

    return output

