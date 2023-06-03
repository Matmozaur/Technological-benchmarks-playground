import requests
import grequests
import time
import logging
import json

if __name__ == "__main__":
    time.sleep(5)

    results = dict()

    for freamework, port in [('flask', 8081), ('fast_api', 8080), ('fiber', 8082)]:
        results[freamework] = dict()
        for endpoint in ['simple_read', 'simple_write']:
            results[freamework][endpoint] = dict()
            results[freamework][endpoint]['sequentional'] = dict()
            for number in [10, 50, 100, 500]:
                start = time.time()
                match endpoint:
                    case 'simple_write':
                        for i in range(number):
                            r = requests.post(f'http://{freamework}:{port}/{endpoint}', json={'name': 'x'})
                    case 'simple_read':
                        for i in range(number):
                            r = requests.get(f'http://{freamework}:{port}/{endpoint}')
                t = time.time() - start
                results[freamework][endpoint]['sequentional'][number] = t
                logging.info(f'Sequentional {freamework}: {endpoint}: {number}: {t}s')

    for freamework, port in [('flask', 8081), ('fast_api', 8080), ('fiber', 8082)]:
        for endpoint in ['simple_read', 'simple_write']:
            results[freamework][endpoint]['concurrent'] = dict()
            for number in [10, 50, 100, 500]:
                start = time.time()
                match endpoint:
                    case 'simple_write': r = (grequests.post(f'http://{freamework}:{port}/{endpoint}', json={'name': 'x'}) for _ in range(number))
                    case 'simple_read': r = (grequests.get(f'http://{freamework}:{port}/{endpoint}') for _ in range(number))
                r = grequests.map(r)
                t = time.time() - start
                results[freamework][endpoint]['concurrent'][number] = t
                logging.info(f'Concurrent {freamework}: {endpoint}: {number}: {t}')
    
    with open('/app/results/results.json', 'w') as f:
        json.dump(results, f)
