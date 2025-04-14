import requests
from bs4 import BeautifulSoup
import re
import os
import time
from requests.exceptions import RequestException

# 配置参数
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
REQUEST_DELAY = 2  # 请求延迟(秒)
OUTPUT_FILE = 'ip.txt'

# 目标URL列表
URLS = [
    {'url': 'https://monitor.gacjie.cn/page/cloudflare/ipv4.html', 'element': 'tr'},
    {'url': 'https://ip.164746.xyz', 'element': 'tr'},
    # 可以继续添加更多URL和对应的元素选择器
]

# 正则表达式用于匹配IP地址(更精确的IPv4匹配)
IP_PATTERN = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

def fetch_html(url, headers, timeout=10):
    """获取网页HTML内容"""
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()  # 检查请求是否成功
        return response.text
    except RequestException as e:
        print(f"请求 {url} 失败: {e}")
        return None

def extract_ips_from_text(text, pattern):
    """从文本中提取IP地址"""
    return re.findall(pattern, text)

def save_ips_to_file(ip_set, filename):
    """将IP地址保存到文件"""
    try:
        with open(filename, 'w') as f:
            f.write('\n'.join(sorted(ip_set)))
        print(f"成功保存 {len(ip_set)} 个唯一IP地址到 {filename}")
    except IOError as e:
        print(f"写入文件 {filename} 失败: {e}")

def main():
    # 准备请求头
    headers = {'User-Agent': USER_AGENT}
    
    # 使用集合自动去重
    unique_ips = set()
    
    # 删除已存在的输出文件
    if os.path.exists(OUTPUT_FILE):
        try:
            os.remove(OUTPUT_FILE)
            print(f"已删除旧文件 {OUTPUT_FILE}")
        except OSError as e:
            print(f"删除文件 {OUTPUT_FILE} 失败: {e}")
            return

    # 遍历所有URL
    for site in URLS:
        url = site['url']
        element = site['element']
        
        print(f"正在处理: {url}")
        
        # 获取HTML内容
        html = fetch_html(url, headers)
        if not html:
            continue
            
        # 解析HTML
        try:
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.find_all(element)
            
            # 提取IP地址
            for el in elements:
                text = el.get_text()
                ips = extract_ips_from_text(text, IP_PATTERN)
                unique_ips.update(ips)
                
            print(f"从 {url} 中找到 {len(ips)} 个IP地址(去重前)")
            
        except Exception as e:
            print(f"解析 {url} 时出错: {e}")
        
        # 添加延迟，避免请求过于频繁
        time.sleep(REQUEST_DELAY)
    
    # 保存结果
    if unique_ips:
        save_ips_to_file(unique_ips, OUTPUT_FILE)
    else:
        print("没有找到任何有效的IP地址")

if __name__ == '__main__':
    main()
