import requests
from bs4 import BeautifulSoup
from PIL import Image
from fpdf import FPDF
from io import BytesIO
import sys

def download_image(img_url):
    response = requests.get(img_url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print(f"Falha ao baixar a imagem: {img_url}")
        return None

def images_to_pdf(manga_name, chapter_number):
    url = f"https://mangaonline.biz/capitulo/{manga_name}-capitulo-{chapter_number}/"
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Falha ao acessar a página: {url}")
        return

    if not os.path.exists('temp'):
        os.makedirs('temp')
    
    soup = BeautifulSoup(response.content, 'html.parser')
    images = []
    for p_tag in soup.find_all('p'):
        img_tag = p_tag.find('img')
        if img_tag and 'src' in img_tag.attrs:
            img_url = img_tag.attrs['src']
            if not img_url.startswith('http'):
                img_url = url.rstrip('/') + '/' + img_url.lstrip('/')
            images.append(img_url)
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    for page_number, img_url in enumerate(images, start=1):
        img = download_image(img_url)
        if img:
            img_width, img_height = img.size
            pdf.add_page()
            img_path = f"temp/temp_image_{page_number}.png"
            img.save(img_path)
            pdf.image(img_path, x = 10, y = 10, w = 180)  
    
    pdf_output = f"{manga_name}_capitulo_{chapter_number}.pdf"
    pdf.output(pdf_output)
    print(f"PDF gerado com sucesso: {pdf_output}")

if len(sys.argv) != 3:
    print("Uso correto: python script.py <nome-do-manga> <numero_do_capitulo>")
else:
    manga_name = sys.argv[1]
    chapter_number = sys.argv[2] 
    images_to_pdf(manga_name, chapter_number)