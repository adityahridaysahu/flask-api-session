import requests
import base64
import codecs


BASE = "http://127.0.0.1:5000"

def main():

    id_key = "id"
    num_cop_key = "num_cop"
    title_key = "title"
    author_key = "author"

    with open("image1.jpeg", "rb") as file:
        binaryData = file.read()
        data = base64.b64encode(binaryData)
        str_data = codecs.decode(data, "UTF-8")

    input()

    response1 = requests.put(
        BASE + "/registerBook/new_id=1564",
        {
            "title": "The Midnight Library",
            "author": "Matt Haig",
            "cover_img": str_data,
            "num_cop": 4,
        },
    )

    json_resp1 = response1.json()
    print(f"Book registered on database with book id: {json_resp1[id_key]} and {json_resp1[num_cop_key]} copies")

    input()

    response2 = requests.put(
        BASE + "/registerBook/new_id=1564",
        {
            "title": "The Midnight Library",
            "author": "Matt Haig",
            "cover_img": str_data,
            "num_cop": 1,
        },
    )

    print(response2.json())
    input()

    response3 = requests.get(BASE + "/book/id=1564")
    json_resp3 = response3.json()
    print(f"Book ID: {json_resp3[id_key]}, Title: {json_resp3[title_key]}, Author: {json_resp3[author_key]}, Number of Copies Available: {json_resp3[num_cop_key]}")

    input()

    response4 = requests.get(BASE + "/book/id=1562")
    print(response4.json())

    input()

    response5 = requests.patch(BASE + "/updateCount/id=1564/inc=1")

    input()

    response6 = requests.patch(BASE + "/updateCount/id=1564/inc=0")

main()







