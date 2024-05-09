import requests

TICKTICK_ACCESS_TOKEN = "9f4288b1-cb01-4266-95c7-5fc382351393"
NOTION_TOKEN = "secret_Hgr4eGMRUZpg9Ccc0e2hxajp2iOEkCBU4TEVLj0ocLW"
NOTION_DATABASE_ID = "92ba7e23-0e49-40db-8ac4-6d60b97262a7"
PROJECT_IDS = '["5eda705b22d41a54616a99b2","5eda70b022d41a54616a99b4","5eda719322d42c5b06e12642","5eda71b322d42c5b06e12643","5edad17122d41a54db098e2a","649aa6a90774056642fe2684","64f72011c45453f703823120","65b97122dc34e0f447c57b7b","663c8a0d8f088ed74042412b"]'
SYNC_INTERVAL = "30"

url = f'https://api.ticktick.com/open/v1/project/{PROJECT_IDS[0]}/data'
print(url)
headers = {
        'Authorization': f'Bearer {TICKTICK_ACCESS_TOKEN}',
        'Cookie': 'AWSALB=INSERT_YOUR_COOKIE_HERE',  # Update this if necessary
        'User-Agent': 'PostmanRuntime/7.37.3',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
response = requests.get(url, headers=headers)

print(response.json())