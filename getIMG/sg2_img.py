# This is a simple file that help sg2 to get images and class the images for
# NASA Astronaut photoes.
# Author : Jing, Aldo, and sg2 members
import urllib
import os

urlbase = 'http://eol.jsc.nasa.gov/DatabaseImages/ESC'
infopage = 'http://eol.jsc.nasa.gov/SearchPhotos/photo.pl?'
class ASTRO_IMG(object):
    """This is a class for astronaut image information.
    """
    def __init__(self,image_id,mission = None):
        self.image_id = image_id
        if mission is None:
            self.mission = self.get_mission(self.image_id)
        else:
            self.mission = mission
        self.image_url = self.get_url()
        self.page_url = self.get_page_url()
        self.img_category = None



    def get_mission(self, image_id):
        """Get astronaut photo taken mission for image id
        """
        image_id_field = image_id.split('-')
        return image_id_field[0]

    def get_url(self, large=False):
        """This is a function that get image url from data website.
        Parameter
        ----------
        large : bool, optional, default is False
            A flag to select the large image or not.
        return
        ----------
        url of the image in the data website.
        """
        if large:
            size = '/large/'
        else:
            size = '/small/'

        url = urlbase + size + self.mission + '/' + self.image_id + '.JPG'
        return url

    def get_page_url(self):
        """This is a function that get image information page url.
        """
        mission_part = 'mission=' + self.mission
        id_num = self.image_id.split('-')[2]
        id_part = 'roll=E&frame=' + id_num
        page_url = infopage + mission_part + '&' + id_part
        return page_url
        
    # This secret discovered by Aldo
    def download_image(self, download_path=None):
        """Save the image from url.
        Parameter
        ----------
        download_path : str
            the path to you download directory
        """
        if download_path is None:
            outfilename = self.image_id+'.jpg'
        else:
            outfilename = os.path.join(download_path,self.image_id + '.jpg')
        image = urllib.urlopen(self.image_url)
        data = image.read()
        if 'removed' in data:
            raise ValueError('The URL for image ' + self.image_id +
                             ' is invalid.')

        output = open(outfilename,"wb")
        output.write(data)
        output.close()
