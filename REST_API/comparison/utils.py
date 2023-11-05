import logging
import os
import time
import requests

import pandas as pd
import matplotlib.pyplot as plt

GET_ENDPOINTS = os.getenv('GET_ENDPOINTS').split(';')
POST_ENDPOINTS = os.getenv('POST_ENDPOINTS').split(';')

log = logging.getLogger()
log.setLevel(logging.INFO)


def wait_for_services(containers, get_endpoint, wait_time):
    flag = True
    while flag:
        flag = False
        for freamework, port in containers:
            try:
                r = requests.get(f' http://{freamework}:{port}/{get_endpoint}')
                logging.info(f'address: http://{freamework}:{port}/{get_endpoint}')
                if r.status_code != 200:
                    raise Exception
            except Exception as e:
                flag = True
                logging.debug(e)
                logging.info(f'Service {freamework} not yet ready')
                time.sleep(wait_time)


def fix_number(number):
    if 'k' in number:
        return float(number.replace('k', '')) * 1000
    if 'm' in number:
        return float(number.replace('m', '')) * 1000000
    return number


def plot_results(results):
    for endpoint in GET_ENDPOINTS+POST_ENDPOINTS:
        for metric, r in zip(['Latency', 'Req/Sec'], [True, False]):
            if metric == 'Latency':
                y = [(k, pd.to_timedelta((v[endpoint][metric]['avg'])).total_seconds()*1000)
                     for k, v in results.items()]
            else:
                y = [(k, float(fix_number(v[endpoint][metric]['avg']))) for k, v in results.items()]
            y = sorted(y, key=lambda x: x[1], reverse=r)
            plt.figure(figsize=(20, 8))
            plot = plt.bar([x[0] for x in y], [x[1] for x in y])
            for value in plot:
                height = value.get_height()
                plt.text(value.get_x() + value.get_width() / 2.,
                         1.002 * height, '%f' % height, ha='center', va='bottom')
            plt.title(f"{endpoint} {metric}")
            plt.xlabel("Freamework")
            plt.ylabel("Latency (ms)")
            plt.savefig(f'/app/results/{endpoint}_{metric.replace("/", "")}.png')
