import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify
primary_url = 'https://www.getmyuni.com/btech-colleges'

app = Flask(__name__)
app.debug = True

@app.route('/university_info', methods=['GET'])
def scrape_colleges():
    url = primary_url
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    colleges = soup.find_all('div', class_='collegeInfoCard')

    result = []
    for college in colleges:
        college_name = college.find('h3', class_='collegeName').text.strip()
        banner_image = college.find('div', class_='clgInfoCardHeader')['style'].split("url(")[1].split(")")[0]
        logo_image = college.find('div', class_='collegeLogo').find('img')['src']
        read_more_link = college.find('p', class_='collegeIntroText').find('a')['href']

        full_read_more_link = requests.compat.urljoin(url, read_more_link.replace('/reviews', ''))
        response_inner = requests.get(full_read_more_link)
        soup_inner = BeautifulSoup(response_inner.content, 'html.parser')
        page_data = soup_inner.find('div', class_='pageData pageInfo').text.strip()

        page_info_div = soup_inner.find('div', class_='pageData pageInfo')
        page_info_span = page_info_div.find(class_=None, recursive=False)

        college_data = {
            'university_name': college_name,
            'banner_image': banner_image,
            'university_logo': logo_image,
            'short_info': page_info_span.text.strip() if page_info_span else None,
            'full_info': page_data           
        }
        result.append(college_data)

    return jsonify(result)

if __name__ == '__main__':
    app.run()
