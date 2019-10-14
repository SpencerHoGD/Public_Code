import requests


def get_html_json_data(keyword, page):
    url = 'https://tuchong.com/rest/search/posts'
    params = {
                "query": keyword,
                "count": 20,
                "page": page
             }

    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
    response = requests.get(url, params=params, headers=headers)

    return response.json()


def download_image(url, user_id, image_id):
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"}
    response = requests.get(url, headers=headers)

    with open("tuchong/{}-{}.jpg".format(user_id, image_id), 'wb') as f:
        f.write(response.content)


def main():
    for page in range(1, 6):
        json_data = get_html_json_data("私房", page)

        # 遍历每个图集
        for each_images in json_data['data']['post_list']:
            # 遍历每张照片
            for each_image in each_images['images']:
                url = each_image['source']['ft640']
                url = url.replace('ft640', 'f')
                user_id = each_image['user_id']
                image_id = each_image['img_id']

                # print(url, user_id, image_id)
                download_image(url, user_id, image_id)


if __name__ == '__main__':
    main()
    # json_data = get_html_json_data("猫", 1)
    # for count, each_images in enumerate(json_data['data']['post_list']):
    #     for num, each_image in enumerate(each_images['images']):
    #         url = each_image['source']['ft640']
    #         print(url)
