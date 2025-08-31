from flask import Flask, request, jsonify, redirect
import requests
from bs4 import BeautifulSoup
import re
import random

app = Flask(__name__)

# 默认UA
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'

@app.route('/')
def parse_lanzou():
    # 获取参数
    url = request.args.get('url', '')
    pwd = request.args.get('pwd', '')
    dl_type = request.args.get('type', '')
    
    # 校验URL参数
    if not url:
        return jsonify(code=400, msg='请输入URL'), 400
    
    try:
        # 提取文件ID
        file_id = re.search(r'com/([^/]+)', url).group(1)
        full_url = f'https://www.lanzoup.com/{file_id}'
        
        # 获取页面内容
        html = requests.get(full_url, headers={'User-Agent': USER_AGENT}).text
        
        # 检查文件是否失效
        if '文件取消分享了' in html:
            return jsonify(code=400, msg='文件取消分享了'), 400
        
        # 提取文件名和大小
        soup = BeautifulSoup(html, 'lxml')
        soft_name = soup.select_one('div[style*="font-size: 30px"]') or \
                    soup.select_one('.n_box_3fn') or \
                    soup.select_one('.b > span')
        soft_name = soft_name.text.strip() if soft_name else ''
        
        soft_size = soup.select_one('.n_filesize') or \
                    soup.select_one('.p7')
        soft_size = soft_size.next_sibling.strip() if soft_size else ''
        
        # 处理带密码文件
        if 'function down_p()' in html:
            if not pwd:
                return jsonify(code=400, msg='请输入分享密码'), 400
            
            # 提取签名数据
            sign = re.search(r"'sign':'([^']+)'", html).group(1)
            ajaxm = re.search(r"ajaxm\.php\?file=(\d+)", html).group(0)
            
            # 提交密码表单
            post_url = f'https://www.lanzoup.com/{ajaxm}'
            data = {'action': 'downprocess', 'sign': sign, 'p': pwd}
            resp = requests.post(post_url, data=data, headers={
                'Referer': full_url,
                'User-Agent': USER_AGENT
            }).json()
            
            if resp['zt'] != 1:
                return jsonify(code=400, msg=resp['inf']), 400
                
            down_url = get_down_url(resp['dom'] + '/file/' + resp['url'])
        else:
            # 处理普通文件
            iframe_src = soup.select_one('iframe[src]')['src']
            iframe_url = f'https://www.lanzoup.com/{iframe_src}'
            
            # 获取iframe内容
            iframe_html = requests.get(iframe_url, headers={
                'Referer': full_url,
                'User-Agent': USER_AGENT
            }).text
            
            # 提取直链
            sign = re.search(r"wp_sign = '([^']+)'", iframe_html).group(1)
            ajaxm = re.findall(r"ajaxm\.php\?file=(\d+)", iframe_html)[1]
            
            # 提交表单
            post_url = f'https://www.lanzoup.com/ajaxm.php?file={ajaxm}'
            data = {'action': 'downprocess', 'sign': sign}
            resp = requests.post(post_url, data=data, headers={
                'Referer': iframe_url,
                'User-Agent': USER_AGENT
            }).json()
            
            if resp['zt'] != 1:
                return jsonify(code=400, msg=resp['inf']), 400
                
            down_url = get_down_url(resp['dom'] + '/file/' + resp['url'])
        
        # 移除敏感参数
        down_url = re.sub(r'pid=[^&]+&', '', down_url)
        
        # 处理下载类型
        if dl_type == 'down':
            return redirect(down_url)
        else:
            return jsonify(
                code=200,
                msg='解析成功',
                name=soft_name,
                filesize=soft_size,
                downUrl=down_url
            )
            
    except Exception as e:
        return jsonify(code=500, msg=f'解析失败: {str(e)}'), 500

def get_down_url(url):
    """获取最终下载链接"""
    try:
        resp = requests.head(url, headers={
            'User-Agent': USER_AGENT,
            'Referer': 'https://developer.lanzoug.com'
        }, allow_redirects=True)
        return resp.url
    except:
        return url

def rand_ip():
    """生成随机IP"""
    return f"{random.randint(60,255)}.{random.randint(60,255)}.{random.randint(60,255)}.{random.randint(60,255)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)