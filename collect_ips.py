import requests
from bs4 import BeautifulSoup
import re
import os

urls = [
    'https://monitor.gacjie.cn/page/cloudflare/ipv4.html',
    'https://ip.164746.xyz'
]

ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
headers = {'User-Agent': 'Mozilla/5.0'}

def is_valid_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            return False
    return True

if os.path.exists('ip.txt'):
    os.remove('ip.txt')

ips = set()  # 使用集合去重

for url in urls:
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if url == 'https://monitor.gacjie.cn/page/cloudflare/ipv4.html':
            elements = soup.find_all('tr')
        elif url == 'https://ip.164746.xyz':
            elements = soup.find_all('tr')
        else:
            elements = soup.find_all('li')
        
        for element in elements:
            element_text = element.get_text()
            ip_matches = re.findall(ip_pattern, element_text)
            for ip in ip_matches:
                if is_valid_ip(ip):
                    ips.add(ip)
    except Exception as e:
        print(f"处理 {url} 时出错: {e}")

with open('ip.txt', 'w') as file:
    for ip in ips:
        file.write(ip + '\n')

print(f"共保存 {len(ips)} 个IP到 ip.txt")
