import requests
import grequests
import time
import logging
import json

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)

    time.sleep(5)

    results = dict()
    containers = [('fast_api', 8081), ('flask', 8082), ('fiber', 8083), ('gin', 8084)]
    endpoints = ['simple_read', 'simple_write']
    numbers = [10, 100, 1000, 10000]

    for number in numbers:
        results[number] = dict()
        for endpoint in endpoints:
            results[number][endpoint] = dict()
            results[number][endpoint]['sequentional'] = dict()
            for freamework, port in containers:
                requests.get(f'http://{freamework}:{port}/{endpoint}')
                time.sleep(0.5)
                match endpoint:
                    case 'simple_write':
                        start = time.time()
                        for i in range(number):
                            r = requests.post(f'http://{freamework}:{port}/{endpoint}', json={'name': 'x'})
                    case 'simple_read':
                        start = time.time()
                        for i in range(number):
                            r = requests.get(f'http://{freamework}:{port}/{endpoint}')
                t = time.time() - start
                results[number][endpoint]['sequentional'][freamework] = t
                logging.info(f'Sequentional {freamework}: {endpoint}: {number}: {t}s')
                time.sleep(1)

    for number in numbers:
        for endpoint in endpoints:
            results[number][endpoint]['concurrent'] = dict()
            for freamework, port in containers:
                requests.get(f'http://{freamework}:{port}/{endpoint}')
                time.sleep(0.5)
                match endpoint:
                    case 'simple_write':
                        start = time.time()
                        r = (grequests.post(f'http://{freamework}:{port}/{endpoint}', json={'name': 'x'}) for _ in range(number))
                    case 'simple_read':
                        start = time.time()
                        r = (grequests.get(f'httpl://{freamework}:{port}/{endpoint}') for _ in range(number))
                r = grequests.map(r)
                t = time.time() - start
                results[number][endpoint]['concurrent'][freamework] = t
                logging.info(f'Concurrent {freamework}: {endpoint}: {number}: {t}')
                time.sleep(1)
    
    with open('/app/results/results.json', 'w') as f:
        json.dump(results, f, indent=2)
