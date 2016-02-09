from get_image_id_example import image_list_file  # Import the class we built
                                                  # get_image_id_example.py
filename = 'test_image_list.dat'  # input file name
imagefile = image_list_file(filename)  # this class needs a filename as input.
# print some attributes' Value for the test

print imagefile.filename
print imagefile.num_images
print imagefile.image_list[0:3]

# get requried images.
imid = imagefile.get_image_ids(3,5)
print imid

# Test the error message

imid = imagefile.get_image_ids(10,20)
