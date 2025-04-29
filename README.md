# 🧠 Pykaso AI unofficial wrapper

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)  
A user-friendly and efficient Python wrapper designed to facilitate seamless interaction with the [Pykaso AI](https://www.pykaso.ai) platform, allowing developers to easily integrate and utilize its powerful features in their applications.

---

## 📦 Features

- [x] Authenticate to get cookies (solely with email & password only, no Google)
- [x] Retrieve account balance
- [x] Generate AI images
- [x] List trained models
- [ ] Face swap
- [ ] Use different LoRA styles for AI images
- [ ] Use different models
- [ ] Seed usage
- [ ] Different aspect ratios
- [ ] Prompt adherence
- [ ] AI video generation
- [ ] Upscale
- [ ] Retrieve payment history

---

## 📥 Installation

```python
pip install requests
```


Clone or copy the `Client` class into your project.

---

## 🚀 Quick Start

```python
from client import Client  # Make sure to save the code as client.py or similar

client = Client('your-email@example.com', 'your-password')

# Get your current credit balance
balance = client.get_total_balance()
print(f"Balance: {balance}")

# Generate 2 portrait-style images from a prompt
result = client.generate_image(prompt="a futuristic cityscape", number_of_images=2)
print(result)

# Fetch summaries of all trained models
models = client.fetch_models_summary()
for model in models:
    print(model)
```

---

## 🧪 Reference

### `Client(username, password)`

Creates a new authenticated session with your Pykaso credentials.

---

### `get_total_balance() -> float`

Returns your current credit balance on the platform.

---

### `generate_image(prompt: str, number_of_images: int = 1) -> dict`

Generates 1–4 portrait-style images based on your prompt.

- `prompt`: Text describing what to generate.
- `number_of_images`: Number of images (max 4).
- Returns a dictionary with:
  - `response`: Raw response text or image-related data
  - `message`: Optional note if number of images was capped

---

### `fetch_models_summary(page: int = 1, page_size: int = 50, max_pages: int = None) -> list`

Fetches summaries of your trained models.

- `page`: Start page.
- `page_size`: Items per page (default: 50).
- `max_pages`: Max number of pages to fetch (None = all).

Each model is returned as:

```python
{
  'id': str,
  'name': str,
  'created_at': str
}
```

---

## 🛑 Disclaimer

This client is unofficial and reverse-engineered from the Pykaso web app. It may break if the site changes. Use responsibly and at your own risk.

---

## 📄 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
