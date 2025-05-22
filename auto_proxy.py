import mitmproxy.ctx
from mitmproxy import ctx, http
import json
import configparser
import os
import schedule
import time
from datetime import datetime

class AutoProxy:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file = 'config.ini'
        self.captured_data = {}
        self.target_endpoints = [
            '/api/run/saveRunV2',
            '/api/auth/login',
            '/api/auth/getLoginToken'
        ]

    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file, encoding='utf-8')

    def save_captured_data(self):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'captured_data_{timestamp}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.captured_data, f, ensure_ascii=False, indent=2)
        ctx.log.info(f'已保存抓包数据到: {filename}')

    def request(self, flow: http.HTTPFlow) -> None:
        if not flow.request.pretty_url:
            return

        for endpoint in self.target_endpoints:
            if endpoint in flow.request.pretty_url:
                self.captured_data[endpoint] = {
                    'url': flow.request.pretty_url,
                    'method': flow.request.method,
                    'headers': dict(flow.request.headers),
                    'content': flow.request.content.decode('utf-8') if flow.request.content else None
                }
                ctx.log.info(f'已捕获请求: {endpoint}')

    def response(self, flow: http.HTTPFlow) -> None:
        for endpoint in self.target_endpoints:
            if endpoint in flow.request.pretty_url:
                if endpoint in self.captured_data:
                    self.captured_data[endpoint]['response'] = {
                        'status_code': flow.response.status_code,
                        'headers': dict(flow.response.headers),
                        'content': flow.response.content.decode('utf-8') if flow.response.content else None
                    }
                    ctx.log.info(f'已捕获响应: {endpoint}')

    def done(self):
        if self.captured_data:
            self.save_captured_data()

addons = [AutoProxy()]

def schedule_run():
    # 这里可以添加定时任务逻辑
    pass

def main():
    # 设置定时任务，每天早上6点运行
    schedule.every().day.at("19:20").do(schedule_run)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
