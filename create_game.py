import requests

BODY = {
    "name": "jgzx25",
    "player1": "p1",
    "player2": "p2",
    "player1_host": "http://100.120.1.64:5000",
    "player2_host": "http://100.120.1.64:5010",
    # "seed": 10,
}


def main():
    response = requests.post('http://10.118.44.49:5555/competitions',json=BODY)
    print (response.status_code,response.json())

if __name__ == '__main__':
    main()