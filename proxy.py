from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # 这里可以拦截和修改请求
    print(f"请求拦截: {flow.request.url}")

def response(flow: http.HTTPFlow) -> None:
    # 这里可以拦截和修改响应
    print(f"响应拦截: {flow.response.status_code}")