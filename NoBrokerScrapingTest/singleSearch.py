from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from time import sleep

# Custom Module Imports
from individualListing import Page

# Making the browser headless and disabling CSS, Image loading and flash
opt = Options()
opt.add_argument("--headless")

firefoxProfile = FirefoxProfile()
# Disable CSS
firefoxProfile.set_preference('permissions.default.stylesheet', 2)
# Disable images
firefoxProfile.set_preference('permissions.default.image', 2)
# Disable Flash
firefoxProfile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

b = webdriver.Firefox(options=opt, executable_path="../venv/geckodriver", firefox_profile=firefoxProfile)

url = "https://www.nobroker.in/property/rent/bangalore/JP%20Nagar/?nbPlace=ChIJK6dJcw0VrjsRRj3d4aE-0PM&&lat_lng=12.910491,77.5857168&sharedAccomodation=0&type=BHK1&orderBy=nbRank,desc&radius=2&propertyType=rent"
b.get(url)

resCount = int(b.find_element_by_css_selector("#resultsCount").text)

# Handling Infinite Scroll
while True:     # Emulating a do-while loop
    listingsContainer = b.find_elements_by_css_selector("a.card-link-detail")
    loadedElements = len(listingsContainer)
    if not loadedElements < resCount:
        print()
        break
    else:
        print(loadedElements, "/", resCount, "elements in the list; Scrolling...")
        b.execute_script('window.scroll(0, document.body.scrollHeight);')
        sleep(1)

basicStatsCon = [str(data.text).replace(" sqft","") for data in b.find_elements_by_css_selector("div.overview.open_detail_page div h3")][:(resCount*3)]
siteID = [data.get_attribute("data-id") for data in b.find_elements_by_css_selector("div.overview.open_detail_page")]

# Grepping data for furnishing status, building age and tenantType
furnishStat = [data.text for data in b.find_elements_by_css_selector(".property-furnishing h5")]
buildingAge = [int(data.text.replace(" year old", "").replace("Newly Constructed", "0")) for data in b.find_elements_by_css_selector(".property-age h5")]
tenantType = [data.text for data in b.find_elements_by_css_selector(".row.detail-summary.open_detail_page div:nth-child(2) > div:nth-child(1) > h5:nth-child(2)")]

# Additional data about address and map location
mapLat=[]
mapLong=[]
addr = [data.text for data in b.find_elements_by_css_selector(".card-header-title h5")]
mapLoc = [str(data.get_attribute("onclick")).replace("intiateMapViewInPopup(","").replace(");", "").replace("'","").split(",")
          for data in b.find_elements_by_css_selector(".card-header-title h5 span")]
for coord in mapLoc:
    mapLat.append(float(coord[0]))
    mapLong.append(float(coord[1]))

listings = []
listLinks = []
area=[]
dep=[]
rent=[]
priceSqftRatio=[]

for each_link in listingsContainer:
    listLinks.append(each_link.get_attribute("href"))
    listings.append(each_link.find_element_by_css_selector("h2").text)

b.quit()

rng = (len(basicStatsCon))
i=0
while i+2<rng:
    try:
        v1 = int(basicStatsCon[i].replace(",", ""))
        v2 = float(basicStatsCon[i+1].replace(",", ""))
        v3 = float(basicStatsCon[i+2].replace(",", ""))
    except ValueError:
        #print("Skipping invalid data {:>3}/{:>3} : (".format((i//3 + 1), rng//3), basicStatsCon[i], ", ", basicStatsCon[i + 1], ", ", basicStatsCon[i + 2], ") ", sep="")
        basicStatsCon.pop(i + 2)
        basicStatsCon.pop(i + 1)
        basicStatsCon.pop(i)  # Written in reverse to avoid problems with shifting index!
        resCount -= 1
        rng = (len(basicStatsCon))
        continue
    except IndexError:
        print("MaxIdx:", rng-1, "Attempted Idx:", i)
        exit(2)
    i += 3

    area.append(v1)
    dep.append(v2)
    rent.append(v3)
    priceSqftRatio.append(v3/v1)

floor=[]
bathroom=[]
cupboard=[]
nonVeg=[]
gatedSec=[]

for i in range(resCount):
    if i>resCount or i>=len(listings):
        break

    (f, b, c, n, g) = Page(listLinks[i]).get_stats()
    floor.append(f)
    bathroom.append(b)
    cupboard.append(c)
    nonVeg.append(n)
    gatedSec.append(g)
    print("%3d" % (i+1), "-", listings[i], "; ----------------------------------\nRent/Area Ratio:", priceSqftRatio[i],
          "; Area:", area[i], "; Deposit:", dep[i], "; Rent:", rent[i], "; Link -", listLinks[i], "; ID:", siteID[i],
          "\nFurnishing:", furnishStat[i], "; Building Age:", buildingAge[i], "; Tenant Type:", tenantType[i], "; Address:", addr[i],
          "; \nLat:", mapLat[i], "; Long:", mapLong[i], "; Floor:", floor[i] , "; Bathrooms:", bathroom[i], "; Cupboards:",
          cupboard[i], "; Non-Veg:", nonVeg[i], "; Gated Security:", gatedSec[i], "\n")

