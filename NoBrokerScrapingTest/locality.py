# Wards according to BBMP (Bangalore Municipality)

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

opt = Options()
opt.add_argument("--headless")
firefoxProfile = FirefoxProfile()
firefoxProfile.set_preference('permissions.default.stylesheet', 2)
firefoxProfile.set_preference('permissions.default.image', 2)
firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

b = webdriver.Firefox(options=opt, executable_path="../venv/geckodriver", firefox_profile=firefoxProfile)
b.get("http://www.vigeyegpms.in/bbmp/?module=public&action=wards")

# Prepare for bullshit - the BBMP site is a goddamn mess. They still use tables to align elements instead of CSS. -_- What is this, 1999?!
loc = [data.text for data in b.find_elements_by_css_selector(".table_middle > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(3) > table:nth-child(2) td:nth-child(2) a")]
b.quit()

for i,l in enumerate(loc):  # Use sorted(loc) for sorted list
    print("{:>3} - {}".format(i+1, l))