# This is an example code for reading the SG2 image list.

class image_list(object):
    def __init__(self, filename): # The file name is an input argument.
        self.filename = filename
        self.image_list = None # set image list. Set is as None type
        self.num_images = 0    # Number of images.
        self.load_list()  # Run load_list class method, load image_list

    def load_list(self):   # Load all the file to memory.
                           # For a big file this is not recommended. But 6000
                           # ids is not a lot.
        f = open(self.filename, 'r')
        self.image_list = f.readlines()  # all the ids are in the image_list
        # Get the total number of images. since the first one is not id. we
        # subtract one
        self.num_images = len(self.image_list) - 1
        f.close()

    def get_image_ids(self, start_index, end_index):
        if any([x >  self.num_images for x in [start_index, end_index]]):
            #same as if star_index > self.num_images or end_index > self.num_images
            # if your request is greater then the number of images. raise error.
            raise ValueError('Your request index is more then the number of'
                             ' total image ids in the file. The file contains '
                             + str(self.num_images) + ' images.')

        result = []  # Set result as an empty list

        for ii in range(start_index, end_index+1):  # loop over all the request indexs
            result_id_str = self.image_list[ii].split() # Get the string from data list, and split from the space
            result_id = result_id_str[1].split('.')[0] # get the id from second element in result_id_str
                                                     # Split('.')[0] only get string without .jpg part
            result.append(result_id[7:])  # Add result id to the result list.

        return result  # The indent has to be the same with for. if it is under
                       # for loop, it will only run once.
    def get_simple_file_format(self, outfile):
        f = open(outfile,'w')
        for ii in range(1, self.num_images+1):
            result_id_str = self.image_list[ii].split() # Get the string from data list, and split from the space
            result_id = result_id_str[1].split('.')[0]
            out_string = result_id[7:] + ' ' + result_id_str[0].strip(',') + '\n'
            f.write(out_string)
        f.close()
