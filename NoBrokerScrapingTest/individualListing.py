from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from time import sleep

"""
Defining Custom Functions
"""


class Page:
    br = None

    def __init__(self,url):
        opt = Options()
        opt.add_argument("--headless")
        firefoxProfile = FirefoxProfile()
        # Disable CSS
        firefoxProfile.set_preference('permissions.default.stylesheet', 2)
        # Disable images
        firefoxProfile.set_preference('permissions.default.image', 2)
        # Disable Flash
        firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
        self.br = webdriver.Firefox(executable_path="../venv/geckodriver", options=opt, firefox_profile=firefoxProfile)

        # self.br = webdriver.Firefox(executable_path="../venv/geckodriver")
        self.br.get(url)

    def get_stats(self):
        stats = self.br.find_element_by_css_selector("div.resale-summary-sec.rent")
        bhk = int(str(stats.find_element_by_css_selector("div.bedroomCount h4").text).replace(" Bedroom", ""))
        balcony = int(stats.find_element_by_css_selector("div.balconyCount h4").text)

        overview = self.br.find_elements_by_css_selector("div#propDetailRow.row.border-radius-3 div.col-md-8.padding-left-0 div.panel-body h5")
        i=0
        while i<len(overview):
            try:
                overview.pop(i)
            except IndexError:
                print("Tried to access idx {} with max addressable idx of {}".format(i, len(overview)-1))
            i += 1
        overview = [str(data.text).replace(" Baths","").replace(" Bath", "") for data in overview][3:]
        # Converting to appropriate formats
        for i, item in enumerate(overview):
            try:
                int(item)   # If an error isn't generated here, item is an integer.
                overview[i] = int(item)
            except ValueError:
                if item == "Yes":
                    overview[i] = True
                elif item == "No":
                    overview[i] = False
                else:
                    print("Some kind of error happened! Found {} of type {} at overview[{}]".format(item, type(item), i))
                    exit(3)
        self.br.quit()
        return tuple(overview) # Floors, bathroom, cupboard, non-veg, gated-security