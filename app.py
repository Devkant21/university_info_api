import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

primary_url = 'https://www.getmyuni.com/'

url_dictionary = {
    "engineering": primary_url+"btech-colleges",
    "bba": primary_url+"bba-colleges",
    "medical": primary_url+"mbbs-colleges"
}

app = Flask(__name__)
# app.debug = True

@app.route('/university_info/<university_type>', methods=['GET'])
def scrape_colleges(university_type):
    if university_type in url_dictionary:
        url = url_dictionary[university_type]
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        colleges = soup.find_all('div', class_='collegeInfoCard')

        result = []
        for college in colleges:
            college_name = college.find('h3', class_='collegeName').text.strip()
            banner_image = college.find('div', class_='clgInfoCardHeader')['style'].split("url(")[1].split(")")[0]
            logo_image = college.find('div', class_='collegeLogo').find('img')['src']
            read_more_link = college.find('p', class_='collegeIntroText').find('a')['href']

            full_read_more_link = requests.compat.urljoin(primary_url, read_more_link.replace('/reviews', ''))
            print("full_read_more_link",full_read_more_link)
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
    else:
        return jsonify({'error': 'Invalid university type'})

if __name__ == '__main__':
    app.run()
