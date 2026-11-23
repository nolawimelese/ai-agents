import requests

def main():
    response = requests.get("http://localhost:1235/v1/models")
    models = response.json()["data"]

    for model in models:
        print(model["id"])

if __name__ == "__main__":
    main()
