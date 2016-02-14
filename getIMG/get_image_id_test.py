from get_image_id_example import image_list_file  # Import the class we built
from sg2_img import ASTRO_IMG                        # get_image_id_example.py
filename = 'test_image_list.dat'  # input file name
imagefile = image_list_file(filename)  # this class needs a filename as input.
# print some attributes' Value for the test

print imagefile.filename
print imagefile.num_images
print imagefile.image_list[0:3]

# get requried images.
imid = imagefile.get_image_ids(3,5)
print imid

for i in imid:
    im = ASTRO_IMG(i)
    im.download_image()
    print im.page_url
    im.get_image_info()
    print im.image_info
    im.translate_info_as_data()
    for name in im.info_list:
        print name, getattr(im,name)

imagefile.get_simple_file_format('testsimple.dat')
