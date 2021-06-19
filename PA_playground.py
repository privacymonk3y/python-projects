import requests
from bs4 import BeautifulSoup
from pathlib import Path

PA_ROOT_ENDPOINT = "https://www.pentesteracademy.com"
PA_COURSE = "https://www.pentesteracademy.com/course?id="
PA_COOKIE = {
    "SACSID": input("What is your SACSID Cookie: "),
}

s = requests.Session()


def get_course_title(course_id):
    s = requests.Session()
    course_page = s.get(f"{PA_COURSE}{course_id}", cookies=PA_COOKIE)
    soup = BeautifulSoup(course_page.text, "html.parser")

    html_title = soup.find("h1", class_="font_color_heading").getText().strip()
    course_title = html_title.replace(" ", "_")
    Path(f"./{course_title}").mkdir(parents=True, exist_ok=True)
    return course_title


def link_scanner(link):
    video_links = []
    video_page = s.get(PA_ROOT_ENDPOINT + link, cookies=PA_COOKIE)
    soup2 = BeautifulSoup(video_page.text, "html.parser")
    sub_link = soup2.find_all("div", id="home")

    for link in sub_link:
        sub_link2 = link.find_all("a")
        for link in sub_link2:
            full_path = PA_ROOT_ENDPOINT + link.get("href")
            video_links.append(full_path)
    return video_links


def download_course_files(links):
    global download_folder
    for link_index in range(len(links)):
        for download_link in links[link_index]:
            if "labred" not in download_link:
                connection = requests.get(download_link, cookies=PA_COOKIE, allow_redirects=True)
                url_link = connection.url
                true_file_name = url_link.split('/')[-1].split("?")[0]

                print("Downloading file: %s" % true_file_name)
                with open(f"./{download_folder}/{true_file_name}", 'wb') as download:
                    for chunk in connection.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            download.write(chunk)
            else:
                continue


def search_course(course_id):
    video_links = []
    video_count = 0

    course_page = s.get(f"{PA_COURSE}{course_id}", cookies=PA_COOKIE)

    soup = BeautifulSoup(course_page.text, "html.parser")

    for heading in soup.find_all("h4"):
        for anchor in heading("a"):
            course_links = anchor.get("href")
            video_link = link_scanner(course_links)
            video_links.append(video_link)
    download_course_files(video_links)


select_course_id = input("What course ID would you like to download?: ")
download_folder = get_course_title(select_course_id)
search_course(select_course_id)
