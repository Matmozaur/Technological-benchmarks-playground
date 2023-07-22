import logging
import time
import requests

import matplotlib.pyplot as plt

log = logging.getLogger()
log.setLevel(logging.INFO)


def wait_for_services(containers, get_endpoint):
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
                time.sleep(5)


def plot_results(results):
    for endpoint in ['simple_read', 'simple_write']:
        for metric, r in zip(['Latency',
                              # 'Req/Sec'
                              ], [True, False]):
            y = [(k, float(v[endpoint][metric]['avg'].replace('ms', ''))) for k, v in results.items()]
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
            plt.savefig(f'/app/results/{endpoint}_{metric}.png')
