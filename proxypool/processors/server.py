'''
Author: Abel
Date: 2022-04-01 09:51:33
LastEditTime: 2022-04-07 17:01:53
LastEditors: Abel
Description: ...
FilePath: /proxy_pool/ProxyPool/proxypool/processors/server.py
'''
from flask import Flask, g
from proxypool.storages.redis import RedisClient
from proxypool.setting import API_HOST, API_PORT, API_THREADED, IS_DEV, REDIS_KEY


__all__ = ['app']

app = Flask(__name__)
if IS_DEV:
    app.debug = True


def get_conn():
    """
    get redis client object
    :return:
    """
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index():
    """
    get home page, you can define your own templates
    :return:
    """
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    get a random proxy
    :return: get a random proxy
    """
    conn = get_conn()
    return conn.random().string()


@app.route('/all')
def get_proxy_all():
    """
    get a random proxy
    :return: get a random proxy
    """
    conn = get_conn()
    proxies = conn.all()
    proxies_string = ''
    if proxies:
        for proxy in proxies:
            proxies_string += str(proxy) + '\n'

    return proxies_string

@app.route('/get')
def get_proxy_all_with_score():
    """
    get a random proxy
    :return: get a random proxy
    """
    conn = get_conn()
    proxies = conn.all()
    proxies_string = ''
    if proxies:
        for proxy in proxies:
            proxies_string += f"{str(proxy)}|{conn.db.zscore(REDIS_KEY, proxy.string())} + '\n\r'"
    return proxies_string


@app.route('/count')
def get_count():
    """
    get the count of proxies
    :return: count, int
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=API_THREADED)
