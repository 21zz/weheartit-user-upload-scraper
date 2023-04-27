"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from urllib.error import HTTPError
import os
import sys
import urllib.request
import requests
import bs4
from pathlib import Path


name = input("Enter weheartit username\n>")

base_url = f"https://weheartit.com/{name}/uploads?date=&order=&utf8=✓&query=&unhearts=include&page="

print("Connecting....")

# attempt to make directory
path = os.path.join(os.getcwd(), name)
try:
    os.mkdir(path)
except FileExistsError:
    print("directory already exists, continuing...")
except IOError:
    # dumbass gimme permission
    print(f"there was an error writing to {path}")
    sys.exit(-1)
# info print
print(f"using directory {path}")

# image IDs are same in CDN and whi.com/entry/{id} links, so it makes it really easy to store 
image_ids: list[str] = []
print("\
-------------------------------------------\n\
--------------grab image links-------------\n\
-------------------------------------------")
      
page = 1
# for each page in pages, plus one since it excludes the last one
while True:
    # get site at that page
    response = requests.get(f"{base_url}{page}")
    soup: bs4.PageElement = bs4.BeautifulSoup(response.content, 'html.parser')
    imageurls: list[bs4.PageElement] = soup.select('div.entry-preview>a.js-entry-detail-link')
    if len(imageurls) == 0:
        break
    print(f"---------- page {page} ----------")
    # for each item in that class
    for item in imageurls:
        # get the href /entry/{id}
        img = item['href']
        print(img)
        if img == None:
            continue
        else:
            # the reason we add an image id to the list instead of the href itself is
            #   because the ID will be used later as a filename
            image_ids.append(str(img).split('/')[-1])
    page += 1
print("-----------------------------")
if len(image_ids) == 0:
    print("no uploads found")
    sys.exit(0)
print()
# for each direct image link
for i, image_id in enumerate(image_ids):
    print(i)
    # check if file exists
    if len(list(Path(path).glob(f'{image_id}.*'))) != 0:
        print(f'\t{image_id} exists')
        continue
        
    entry = f"https://weheartit.com/entry/{image_id}"
    # gather CDN url for the original image
    resp = requests.get(entry)
    image_url = bs4.BeautifulSoup(resp.content, 'html.parser').select_one('img.entry-image[src*="original"]')['src']
    # extension is last element in image_url which looks like this:
    #   https://data.whicdn.com/images/{id}/original.jpg
    ext = image_url.split('.')[-1]
    # this might fix something? test later
    try:
        # try to save at file path
        filepath = os.path.join(path, f"{image_id}.{ext}")
        if not os.path.exists(filepath):
            _, message = urllib.request.urlretrieve(image_url, filepath)
            print(f"\tsaved {filepath}")
        # if the filepath exists, then 
        else:
            print("\tdidn't detect entry as existing before now")
            print(entry)
    except HTTPError:
        print(f"{message}")

