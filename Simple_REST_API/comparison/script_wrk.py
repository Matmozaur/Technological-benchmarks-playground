import logging
import os
import subprocess
import time
import requests

log = logging.getLogger()
log.setLevel(logging.INFO)

containers = [('fast-api', 8081), ('flask', 8082), ('fiber', 8083), ('gin', 8084), ('akka', 8085), ('dotnet', 8086)]
get_endpoints = ['simple_read']
post_endpoints = ['simple_write']

WRK_TIME = os.getenv('WRK_TIME')
WRK_CONNECTIONS = os.getenv('WRK_CONNECTIONS')
WRK_THREADS = os.getenv('WRK_THREADS')


if __name__ == '__main__':

    flag = True
    while flag:
        flag = False
        for freamework, port in containers:
            try:
                r = requests.get(f' http://{freamework}:{port}/{get_endpoints[0]}')
                logging.info(f'address: http://{freamework}:{port}/{get_endpoints[0]}')
                if r.status_code != 200:
                    raise Exception
            except Exception as e:
                flag = True
                logging.debug(e)
                logging.info(f'Service {freamework} not yet ready')
                time.sleep(5)

    for freamework, port in containers:
        subprocess.run([f'echo "{freamework}" >> /app/results/results.txt'], shell=True)
        for endpoint in get_endpoints:
            subprocess.run([f'echo "{endpoint}" >> /app/results/results.txt'], shell=True)
            subprocess.run([f'wrk -t{WRK_THREADS} -c{WRK_CONNECTIONS} -d{WRK_TIME} '
                            f'http://{freamework}:{port}/{endpoint} >> /app/results/results.txt'],
                           shell=True)
            subprocess.run([f'echo "\n" >> /app/results/results.txt'], shell=True)

        for endpoint in post_endpoints:
            subprocess.run([f'echo "{endpoint}" >> /app/results/results.txt'], shell=True)
            subprocess.run([f'wrk -t{WRK_THREADS} -c{WRK_CONNECTIONS} -d{WRK_TIME}  -s ./app/post.lua '
                            f'http://{freamework}:{port}/{endpoint} >> /app/results'
                            f'/results.txt'],
                           shell=True)
            subprocess.run([f'echo "\n" >> /app/results/results.txt'], shell=True)
        subprocess.run([f'echo "\n" >> /app/results/results.txt'], shell=True)

    logging.info('END TEST')
