import logging
import subprocess
import time

import requests

containers = [('fast_api', 8081), ('flask', 8082), ('fiber', 8083), ('gin', 8084), ('akka', 8085)]
get_endpoints = ['simple_read']

if __name__ == '__main__':

    flag = True
    while flag:
        flag = False
        for freamework, port in containers:
            r = requests.get(f' http://{freamework}:{port}/{get_endpoints[0]}')
            if r.status_code != 200:
                flag = True
                logging.info('Services not yet ready')
                time.sleep(1)

    for endpoint in get_endpoints:
        subprocess.run([f'echo "{endpoint}" >> /app/results/results.txt'], shell=True)
        for freamework, port in containers:
            subprocess.run([f'echo "{freamework}" >> /app/results/results.txt'], shell=True)
            subprocess.run([f'wrk -t4 -c50 -d10s http://{freamework}:{port}/{endpoint} >> /app/results/results.txt'],
                           shell=True)
            subprocess.run([f'echo "\n" >> /app/results/results.txt'], shell=True)
        subprocess.run([f'echo "\n" >> /app/results/results.txt'], shell=True)
