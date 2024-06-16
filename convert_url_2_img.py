from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests
import torch
import torchvision.transforms as T
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import argparse


def fetch_product_image(url):
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        driver.get(url)
        # Wait for the image element to be present
        img_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, 'landingImage'))
        )

        # Get the page source and parse it with BeautifulSoup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the main product image
        img_tag = soup.find('img', {'id': 'landingImage'})

        if img_tag and 'src' in img_tag.attrs:
            img_url = img_tag['src']
            if not img_url.startswith('http'):
                img_url = 'https:' + img_url  # Fix relative URL if necessary

            try:
                img_response = requests.get(img_url, timeout=10)
                img_response.raise_for_status()
            except requests.RequestException as e:
                print(f"Error fetching the image: {e}")
                return

            img = Image.open(BytesIO(img_response.content))

            # Save the image
            img.save('product_image.jpg')
            print('Image saved as product_image.jpg')
        else:
            print('No image found')

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()


    # Load a pre-trained DeepLabV3 model for semantic segmentation
    model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet101', pretrained=True)
    model.eval()

    # Preprocess the image
    input_image = Image.open("product_image.jpg").convert("RGB")
    preprocess = T.Compose([
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)  # create a mini-batch as expected by the model

    # Move the input and model to GPU for speed if available
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    with torch.no_grad():
        output = model(input_batch)['out'][0]
    output_predictions = output.argmax(0)

    # Assuming class 15 is the shirt class
    shirt_class = 15
    shirt_mask = output_predictions == shirt_class

    # Convert the mask to a numpy array
    shirt_mask = shirt_mask.byte().cpu().numpy()

    # Create a 3-channel mask
    shirt_mask_3d = np.stack([shirt_mask]*3, axis=-1)

    # Apply the mask to the input image
    input_image_np = np.array(input_image)
    shirt_image = np.where(shirt_mask_3d, input_image_np, 0)

    # Display the extracted shirt
    plt.imshow(shirt_image)
    plt.axis('off')  # Turn off axis
    plt.show()

    # Convert the numpy array back to an image
    shirt_image_pil = Image.fromarray(shirt_image.astype('uint8'))

    # Save the image
    shirt_image_pil.save("segmented_garment.png")



parser=argparse.ArgumentParser()
parser.add_argument('--url', type=str, required=True,help='URL of the product page to scrape')
args=parser.parse_args()
# Replace this URL with the URL of the product page you want to scrape
url = args.url
fetch_product_image(url)
