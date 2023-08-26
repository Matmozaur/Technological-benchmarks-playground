# Technological-benchmarks-playground
Project dedicated to compare against each other various technologies that we may be using for a given task.

Specific directories in the project corresponds to the technologies we want to benchmark. 

### REST_API
In this subdirectory we want to compare latency and throughput of different REST APIs,
using wrk benchmarking technology. We may benchmark simple read/write operation, as well
as complex functionalities.

To use it one must create directories with each freamework/technology to be compared,
provide relevant data to orchestration definition (docker-compose) and set environment
config (.env file), most important:
- CPUS - percent of the cpu allocated to each container
- MEM_LIMIT - ram limit
- GET_ENDPOINTS - list of get endpoint names, separated by ;
- POST_ENDPOINTS - list of post endpoint names, separated by ;
- WRK_TIME - wrk script execution time
- WRK_CONNECTIONS - wrk connections to the container
- WRK_THREADS - number of used threads

### GQL_API


### ORM_DB

