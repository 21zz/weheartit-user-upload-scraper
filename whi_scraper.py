from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import os
import urllib.request

options = Options()
options.headless = True  # headless
options.add_argument("--enable-automation")  # automation!!!!
options.add_argument("--disable-logging")  # disable logging

name = input("Enter weheartit username\n>")

print("Connecting....")
# url to user's first page of uploads
url = "https://weheartit.com/" + name + "/uploads?page=1"

# load driver and get going
driver = webdriver.Firefox(options=options)
driver.get(url)

# attempt to make directory
try:
    os.mkdir(os.getcwd() + "/" + name)
except FileExistsError:
    print("directory already exists, continuing...")
except IOError:
    # dumbass gimme permission
    print("there was an error writing to " + os.getcwd())
    os.sys.exit(-1)
# info print
print("using directory " + os.getcwd() + "/" + name)

# default pages has to be 1
pages = 1
try:
    # try to find pages element
    pages = driver.find_element_by_css_selector(
        "span.js-pagination-counter-total").text.split(" ")[1]
    print("pages: " + pages)
except:
    # if doesn't exist, keep her going
    print("there is no more than 1 page, or this shit just borked.")

# url structure for uploads without page
newurl = "https://weheartit.com/" + name + "/uploads?page="
# list of direct image links :)
real_image_links = []
print("\
-------------------------------------------\n\
--------------grab image links-------------\n\
-------------------------------------------")
# for each page in pages, plus one since it excludes the last one
for i in range(1, int(pages)+1):
    print("page " + str(i) + "...")
    # get site at that page
    driver.get(newurl + str(i))
    # select element a.js-download-image <a class="js-download-image">
    imageurls = driver.find_elements_by_css_selector("a.js-download-image")
    # for each item in that class
    for item in imageurls:
        # get the href (link to the image)
        img = item.get_attribute("href")
        print(img)
        if img == None:
            continue
        else:
            # add to image links list if it exists
            real_image_links.append(str(img))
print("-------------------------------------------")


print("-------------------------------------------")
# for each direct image link
for i in range(0, real_image_links.__len__()):
    # get a url
    real_image = real_image_links[i]
    # split it at the forward slashes
    tmp_real = real_image.split("/")
    # the second to last index happens to be some kind of internal ID, so we use that
    real_filename = tmp_real[tmp_real.__len__() - 2]
    # the last index is the filename (original.jpg),
    # then split that at period and index 1 is extension
    real_ext = tmp_real[tmp_real.__len__() - 1].split(".")[1]

    print(str(i) + "\tReal image:\t" + real_image)
    print("\tExtracted name:\t" + real_filename)
    try:
        # try to save at file path
        filepath = os.getcwd() + "/" + name + "/" + real_filename + "." + real_ext
        urllib.request.urlretrieve(real_image, filepath)
        print("saved " + filepath)
    except FileExistsError:
        # already exists so continue
        print(str(i) + "\tfile already exists")
    except IOError:
        # io error bruh fix yo shit
        print(str(i) + "\tthere was an error writing to " + filepath)
        os.sys.exit(2)
