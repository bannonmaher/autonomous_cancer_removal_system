# Copyright and Patents Pending Jonathan Bannon Maher Corporation
# Inventor and author Jonathan Bannon Maher
# This class aggregates and extends the functionality of various means of image recognition and processing.


# import image analysis libraries that provide for identifying image pixel colors,
# extracting and comparing shapes in images, and comparing two images overall similarity

import cv2
from shapely import geometry
from PIL import Image
import ImageChops


# define a class for image processing

class image_processing():

    # create variables holding the minimum and maximum percent of image expansion for matching,
    # the image expansion step percent, and the image rotation degree step

    image_size_minimum = 0.8
    image_size_maximum = 1.2
    image_size_step = .02
    image_degree_step = 2


    # create a function that determines whether or not a larger image contains a smaller image

    def image_contains_image(image_large, image_small):

        # initialize an array to hold every possible cut out of the large image
        # of the size of the smaller image

        image_large_array = []

        # initialize a variable to hold the current small image degree rotation

        degree = 0

        # iterate though each image degree rotation while rotation is less than 360 degrees,
        # with all images always being circles since a microscope provides circles both for
        # live images and stored images, which also happens to allow for easy image rotation

        while degree < 360:

            # iterate through each image percent size between the previously specified
            # image size minimum and maximum, utilizing the specified step size

            size = image_size_minimum
            while size <= image_size_maximum:
                width = image_large.width*size
                height = image_large.height*size

                # generate the image using the determined rotation and sizing

                image_large_adjusted = img.rotate(
                    degrees, expand=True)
                image_large_adjusted = img.resize(
                    (width,height), PIL.Image.ANTIALIAS)

                # append the image to the modified images array

                image_large_array.append(
                    image_large_adjusted)

                # increment the image step size

                size += image_size_step

                # increment the image degree rotation

                degree += image_degree_step

            # iterate through each image in the modified images array

            for large_adjusted in large_image_array:

                # create variables holding the dimensions of the large image and the small image

                large_width = large_adjusted.width
                large_height = large_adjusted.height
                small_width = image_small.width
                small_height = image_small.height

                # initialize top left starting point x and y variables to iterate through large image

                x = 0
                y = 0

            # loop through each top left x and y point within the large image that and take a cut out
            # the size of the small image

            while (x + small_width <= large_width):
                while (y + small_height <= large_height):
                    large_cutout = large_adjusted.crop(
                        (x, y, small_width, small_height))

                    # if the cut out of the large image matches the small image at or above the
                    # previously specified match threshold, return that a match was found

                    if ImageChops.difference(large_cutout, image_small) >= match_threshold:
                        return True

                    # increment the y position

                    y = y+1

                # increment the x position

                x = x+1

                # if no match was found, return false

                return False


    # create a function to check if an image contains a color

    def image_contains_color(
        image_source, color, image_match_threshold):

        # load the individual pixel colors from the image into an array using the corresponding
        # previously imported library

        pixels = image_source.load()

        # initialize variables holding the number of pixels processed and found

        pixel_count = 0
        pixel_found_count = 0

        # iterate through each image pixel, increment the pixel counter, and if the pixel color
        # matches the specified color, increment the pixel found counter

        for x in range(image_source.width):
            for y in range(image_source.height):
                pixel_count += 1
                pixel_color = pixels[x,y]
                if pixel_color == color:
                    pixel_found_count += 1

        # if the percent of pixels matching the specified color are above the previously set
        # threshold return true, otherwise return false  

        if pixel_count > 0:
            if (pixel_found_count/pixel_count) > image_match_threshold:
                return True
        return False


    # create a function to determine if the image contains a shape

    def image_contains_shape(
        coordinates, image_large):

        # create a variable specifying if the shape was found in the image

        found = False

        # initialize a coordinate pairs array

        cordinates_array = []

        # split the coordinate pairs from the line in the settings file into an array

        coordinates = coordinates.split(";")

        # iterate through each coordinate pair

        for coordinate in coordinates:

            # split the coordinate pair into x and y

            coordinate = coordinate.split(",")
            x = coordinate[0]
            y = coordinate[1]

            # append the x,y coordinates to the coordinates array

            coordinates_array.append([x,y])

            # generate a polygon from the coordinates using an the corresponding imported library

            coordinates_polygon = geometry.Polygon(
                [[p.x, p.y] for p in points])

            # generate an array of all polygons in the image using the corresponding imported library

            image_polygons = cv2.findContours(image_large)

            # iterate through each polygon found in the image

            for image_polygon in image_polygons:

                # check if the polygon in the image matches the polygon specified in the
                # settings file within the threshold previously specified and if so
                # set the found variable equal to true

                if image_polygon.almost_equals(
                    coordinated_polygon, decimal=
                    match_threshold):
                    found = True

            # return the variable indicating whether or not the shape was found in the image


        return found

