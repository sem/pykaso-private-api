import requests
import json

class Client:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.cookies = {}
        self.authenticate()

    def authenticate(self):
        response = self.session.get('https://app.pykaso.ai/api/auth/csrf')
        csrf_token = response.json().get('csrfToken')

        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://app.pykaso.ai',
            'priority': 'u=1, i',
            'referer': 'https://app.pykaso.ai/sign-in',
            'sec-ch-ua': '\'Google Chrome\';v=\'135\', \'Not-A.Brand\';v=\'8\', \'Chromium\';v=\'135\'',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '\'macOS\'',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'x-auth-return-redirect': '1'
        }

        data = {
            'username': self.username,
            'password': self.password,
            'redirect': 'false',
            'callbackUrl': '/',
            'csrfToken': csrf_token
        }

        response = self.session.post(
            'https://app.pykaso.ai/api/auth/callback/credentials?',
            headers=headers,
            data=data
        )

        if response.status_code != 200:
            raise Exception(f'Login failed: {response.status_code}, {response.text}')

        self.cookies = self.session.cookies.get_dict()

    def get_total_balance(self) -> float:
        url = 'https://app.pykaso.ai/api/user/balance'

        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'priority': 'u=1, i',
            'referer': 'https://app.pykaso.ai/sign-in',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36'
        }

        response = self.session.get(url, headers=headers, cookies=self.cookies)

        if response.status_code != 200:
            raise Exception(f'Failed to fetch balance: {response.status_code}, {response.text}')

        return response.json().get('total', 0.0)

    def generate_image(self, prompt: str, number_of_images: int = 1) -> dict:
        message = None

        if number_of_images < 1:
            number_of_images = 1
        elif number_of_images > 4:
            message = f"Requested {number_of_images} images, but the maximum allowed is 4. Set to 4."
            number_of_images = 4

        url = 'https://app.pykaso.ai/ai-image-generator'

        headers = {
            'accept': 'text/x-component',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'text/plain;charset=UTF-8',
            'next-action': '7f7862f27e4fb94ddff6956b38041d44889f1a8bab',
            'next-router-state-tree': '%5B%22%22%2C%7B%22children%22%3A%5B%22(dashboard)%22%2C%7B%22children%22%3A%5B%22(tools)%22%2C%7B%22children%22%3A%5B%22ai-image-generator%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2Fai-image-generator%22%2C%22refresh%22%5D%7D%5D%7D%5D%7D%2Cnull%2Cnull%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
            'origin': 'https://app.pykaso.ai',
            'priority': 'u=1, i',
            'referer': 'https://app.pykaso.ai/ai-image-generator',
            'sec-ch-ua': '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'x-deployment-id': 'dpl_H4VrPm44rdRmJMFPmEpC11UXocmb',
        }

        payload = [{
            "aspectRatio": "portrait",
            "trainingId": "4Xobp7PvMIXgw39GtIgyR",
            "prompt": prompt,
            "numberOfImages": number_of_images,
            "guidanceScale": 3,
            "seed": "",
            "modelId": 1,
            "extraLoraId": None
        }]

        response = self.session.post(
            url,
            headers=headers,
            cookies=self.cookies,
            data=json.dumps(payload)
        )

        if response.status_code != 200:
            raise Exception(f'Failed to generate image: {response.status_code}, {response.text}')

        return {
            "response": response.text,
            "message": message
        }
    
    def fetch_models_summary(self, page: int = 1, page_size: int = 50, max_pages: int = None) -> list:
        url_base = "https://app.pykaso.ai/api/models"
        headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "priority": "u=1, i",
            "referer": "https://app.pykaso.ai/ai-image-generator",
            "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        }

        all_models = []

        while True:
            url = f"{url_base}?page={page}&page_size={page_size}"
            response = self.session.get(url, headers=headers, cookies=self.cookies)

            if response.status_code != 200:
                raise Exception(f'Failed to fetch models: {response.status_code}, {response.text}')

            data = response.json()

            trainings = data.get('data', {}).get('trainings', [])

            if not trainings:
                break

            for model in trainings:
                all_models.append({
                    'id': model.get('id'),
                    'name': model.get('modelName'),
                    'created_at': model.get('createdAt')
                })

            current_page = data.get('data', {}).get('pagination', {}).get('currentPage', page)
            total_pages = data.get('data', {}).get('pagination', {}).get('totalPages', current_page)

            if (max_pages and page >= max_pages) or (current_page >= total_pages):
                break
            page += 1

        return all_models
    
if __name__ == "__main__":
    client = Client('mail@europe.com', '$Password')

    print(client.cookies)

    balance = client.get_total_balance()
    print(f"Balance: {balance}")

    models = client.fetch_models_summary(page=1, page_size=50, max_pages=None)

    print(f"Fetched {len(models)} models:")
    for model in models:
        print(f"- ID: {model['id']}, Name: {model['name']}, Created at: {model['created_at']}")
