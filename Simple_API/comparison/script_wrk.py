import subprocess
import time

time.sleep(30)

containers = [('fast_api', 8081), ('flask', 8082), ('fiber', 8083), ('gin', 8084)]
endpoints = ['simple_read']

for endpoint in endpoints:
    subprocess.run([f'echo "{endpoint}" >> /app/results/results.txt'], shell=True)
    for freamework, port in containers:
        subprocess.run([f'echo "{freamework}" >> /app/results/results.txt'], shell=True)
        subprocess.run([f'wrk -t4 -c50 -d10s http://{freamework}:{port}/{endpoint} >> /app/results/results.txt'],
                       shell=True)
        subprocess.run([f'echo "\n" >> /app/results/results.txt'], shell=True)
    subprocess.run([f'echo "\n" >> /app/results/results.txt'], shell=True)
