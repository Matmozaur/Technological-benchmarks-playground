import datetime
import json
import logging
import os
import subprocess

from utils import wait_for_services, plot_results

log = logging.getLogger()
log.setLevel(logging.INFO)

CONTAINERS = [('fast-api', 8081), ('flask', 8082), ('fiber', 8083), ('gin', 8084), ('akka', 8085),
              # ('dotnet', 8086)
              ]

GET_ENDPOINTS = os.getenv('GET_ENDPOINTS').split(';')
POST_ENDPOINTS = os.getenv('POST_ENDPOINTS').split(';')

WRK_TIME = os.getenv('WRK_TIME')
WRK_CONNECTIONS = os.getenv('WRK_CONNECTIONS')
WRK_THREADS = os.getenv('WRK_THREADS')

WAIT_TIME = os.getenv('WAIT_TIME', 10)

if __name__ == '__main__':

    wait_for_services(CONTAINERS, GET_ENDPOINTS[0], WAIT_TIME)

    results = dict()

    subprocess.run([f'echo "{datetime.datetime.now()}" >> /app/results/results_logs.txt'], shell=True)
    for freamework, port in CONTAINERS:
        subprocess.run([f'echo "{freamework}" >> /app/results/results_logs.txt'], shell=True)
        results[freamework] = dict()
        for endpoint in GET_ENDPOINTS:
            subprocess.run([f'echo "{endpoint}" >> /app/results/results_logs.txt'], shell=True)
            res = subprocess.run([f'wrk -t{WRK_THREADS} -c{WRK_CONNECTIONS} -d{WRK_TIME} '
                                  f'http://{freamework}:{port}/{endpoint} | tee -a /app/results/results_logs.txt'],
                                 capture_output=True, text=True, shell=True).stdout.split("\n")[3:5]
            results[freamework][endpoint] = {v[0]: {'avg': v[1], 'std': v[2], 'max': v[3]} for v in map(str.split, res)}
            subprocess.run([f'echo "\n" >> /app/results/results_logs.txt'], shell=True)

        for endpoint in POST_ENDPOINTS:
            subprocess.run([f'echo "{endpoint}" >> /app/results/results_logs.txt'], shell=True)
            res = subprocess.run([f'wrk -t{WRK_THREADS} -c{WRK_CONNECTIONS} -d{WRK_TIME}  -s ./app/{endpoint}.lua '
                                  f'http://{freamework}:{port}/{endpoint} | tee -a /app/results'
                                  f'/results_logs.txt'],
                                 capture_output=True, text=True, shell=True).stdout.split("\n")[3:5]
            results[freamework][endpoint] = {v[0]: {'avg': v[1], 'std': v[2], 'max': v[3]} for v in map(str.split, res)}
            subprocess.run([f'echo "\n" >> /app/results/results_logs.txt'], shell=True)
        subprocess.run([f'echo "\n" >> /app/results/results_logs.txt'], shell=True)
    subprocess.run([f'echo "\n" >> /app/results/results_logs.txt'], shell=True)

    with open("/app/results/results.json", "w") as outfile:
        json.dump(results, outfile, indent=4)

    plot_results(results)

    logging.info('END TEST')
