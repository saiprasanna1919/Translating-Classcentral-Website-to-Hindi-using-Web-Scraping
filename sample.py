import requests
from bs4 import BeautifulSoup
from googletrans import Translator
import os


def convert_website_to_hindi(url,main_url,trans,headers):
    os.chdir(r"current path")
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    for element in soup.find_all(text=True):
        if element.parent.name in ['style', 'script']:
            continue
        try:
            translation = trans.translate(element.strip(), dest='hi',src='en')
            element.replace_with(translation.text)
        except:
            continue
    file_name = ''
    folder_name = ''
    count_slash = 0
    if url == main_url or url == 'https://www.classcentral.com/':
        with open('index.html','wb') as f:
            f.write(str(soup.prettify()).encode())
    else:
        for i in range(0,len(url)):
            if url[i] == "/":
                count_slash += 1

        if count_slash == 3:
            for i in range(len(url)-1,0,-1):
                if url[i] != '/':
                    file_name = file_name+url[i]
                else:
                    break
            folder_name = r"folder name"
            file_name = file_name

        elif count_slash == 4:
            for i in range(len(url)-1,0,-1):
                if url[i] != '/':
                    file_name = file_name+url[i]
                else:
                    break
            for i in range(29,len(url)):
                if url[i] != "/":
                    folder_name = folder_name+url[i]
                else:
                    break
            file_name = file_name[::-1]
        try:
            os.mkdir(folder_name)
            os.chdir(folder_name)
            with open(file_name[::-1]+'.html','wb') as f:
                f.write(str(soup.prettify()).encode())
        except OSError as err:
            os.chdir(folder_name)
            with open(file_name[::-1]+'.html','wb') as f:
                f.write(str(soup.prettify()).encode())


def main():
    main_url = 'https://www.classcentral.com'
    headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/71.0.3578.98 Safari/537.36", 
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"}
    trans = Translator()

    response = requests.get(main_url,headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')
    links_list = []
    all_links_list = []
    for link in links:
        listing_url = link.get('href')
        all_links_list.append(listing_url)
        if listing_url not in links_list:
            links_list.append(listing_url)
    print("length of all urls",len(all_links_list))
    print("length of unique urls",len(links_list))
    for i in links_list[:100]:
        if i == "/":
            convert_website_to_hindi(main_url,main_url,trans,headers)
        elif i[0] =="/":
            url = main_url + i
            convert_website_to_hindi(url,main_url,trans,headers)
        else:
            convert_website_to_hindi(i,main_url,trans,headers)

main()

print("Done Everything")