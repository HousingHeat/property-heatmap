from selenium import webdriver
b = webdriver.Firefox(executable_path="../venv/geckodriver")
b.get("https://www.commonfloor.com/sitemap/index/city/Bangalore")

loc = [data.text for data in b.find_elements_by_css_selector("#stupidtable-locality a strong")][:-1]
b.quit()

for i,l in enumerate(loc):
    print("{:>3} - {}".format(i+1, l))