# Apache JMeter load test

`api-smoke.jmx` is a portable JMeter test plan for the local FastAPI target. It includes a thread group, HTTP defaults, a health request, response assertion and summary report listener.

Run after starting the app:

```bash
uvicorn load_testing.app:app --host 127.0.0.1 --port 8000
jmeter -n -t jmeter/api-smoke.jmx -Jhost=127.0.0.1 -Jport=8000 -Jthreads=10 -Jrampup=5 -Jloops=5 -l jmeter/results.jtl -e -o jmeter/report
```

This is a small smoke profile, not a capacity benchmark. Increase threads, ramp-up and duration only against an environment where load testing is authorized.
