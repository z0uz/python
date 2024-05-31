import requests
from bs4 import BeautifulSoup
import subprocess
import os

def fetch_metadata(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None, None

    soup = BeautifulSoup(response.content, 'lxml')
    metadata = {}
    for meta in soup.find_all('meta'):
        if meta.get('name'):
            metadata[meta.get('name')] = meta.get('content')
        elif meta.get('property'):
            metadata[meta.get('property')] = meta.get('content')

    title = soup.find('title')
    if title:
        metadata['title'] = title.text

    important_info = {
        'headers': {},
        'paragraphs': [],
        'links': [],
        'images': []
    }
    
    for header_tag in ['h1', 'h2', 'h3']:
        headers = soup.find_all(header_tag)
        important_info['headers'][header_tag] = [header.text.strip() for header in headers]
    
    paragraphs = soup.find_all('p')
    important_info['paragraphs'] = [para.text.strip() for para in paragraphs]
    
    links = soup.find_all('a', href=True)
    important_info['links'] = [{'text': link.text.strip(), 'url': link['href']} for link in links]
    
    images = soup.find_all('img', src=True)
    important_info['images'] = [{'alt': img.get('alt', '').strip(), 'url': img['src']} for img in images]
    
    return metadata, important_info

def scan_subdomains(domain):
    print("Scanning for subdomains...")
    result = subprocess.run(['sublist3r', '-d', domain, '-o', 'subdomains.txt'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to scan subdomains: {result.stderr}")
        return []
    with open('subdomains.txt', 'r') as f:
        subdomains = f.read().splitlines()
    os.remove('subdomains.txt')
    return subdomains

def scan_directories(url):
    print("Scanning for directories...")
    result = subprocess.run(['dirsearch', '-u', url, '-e', '*', '-x', '400,403,404', '-o', 'directories.txt'], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Failed to scan directories: {result.stderr}")
        return []
    with open('directories.txt', 'r') as f:
        directories = f.read().splitlines()
    os.remove('directories.txt')
    return directories

def main():
    url = input("Please enter the website URL: ")
    domain = url.split("//")[-1].split("/")[0]

    metadata, important_info = fetch_metadata(url)
    if metadata is None or important_info is None:
        print("Failed to fetch website data.")
        return

    subdomains = scan_subdomains(domain)
    directories = scan_directories(url)

    output_file = "website_info.txt"
    with open(output_file, 'w') as f:
        f.write("Metadata:\n")
        for key, value in metadata.items():
            f.write(f"{key}: {value}\n")
        
        f.write("\nImportant Information:\n")
        for header_tag, headers in important_info['headers'].items():
            f.write(f"{header_tag.upper()} tags:\n")
            for header in headers:
                f.write(f"- {header}\n")
        
        f.write("\nParagraphs:\n")
        for para in important_info['paragraphs']:
            f.write(f"- {para}\n")
        
        f.write("\nLinks:\n")
        for link in important_info['links']:
            f.write(f"- {link['text']} ({link['url']})\n")
        
        f.write("\nImages:\n")
        for img in important_info['images']:
            f.write(f"- {img['alt']} ({img['url']})\n")

        f.write("\nSubdomains:\n")
        for subdomain in subdomains:
            f.write(f"- {subdomain}\n")

        f.write("\nDirectories:\n")
        for directory in directories:
            f.write(f"- {directory}\n")

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
