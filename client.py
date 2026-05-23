import requests

API_KEY = 'AIzaSyAVVD....'
API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent?key=' + API_KEY

def analyze_image(image_path):
    with open(image_path, 'rb') as img_file:
        img_bytes = img_file.read()
    # Gemini expects base64-encoded images
    import base64
    img_b64 = base64.b64encode(img_bytes).decode('utf-8')
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_b64
                        }
                    }
                ]
            }
        ]
    }
    response = requests.post(API_URL, json=payload)
    if response.ok:
        return response.json()
    else:
        print("Error:", response.text)
        return None

def main():
    image_path = input("Enter the path to your image: ")
    result = analyze_image(image_path)
    if result:
        print("Gemini says:", result)

if __name__ == "__main__":
    main()


