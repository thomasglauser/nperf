```
                          ____
   ____  ____  ___  _____/ __/
  / __ \/ __ \/ _ \/ ___/ /_
 / / / / /_/ /  __/ /  / __/
/_/ /_/ .___/\___/_/  /_/
     /_/
```

## Simple Network Performance Monitoring

[![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/thomasglauser00/nperf)](https://hub.docker.com/r/thomasglauser00/nperf)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

## Features

-   Monitoring of Download/Upload speeds (Via speedtest.net)
-   Monitoring of server latency
-   Everything is containerized
-   Simple configuration with docker-compose

## Demo

![Dashboard](https://github.com/AUThomasCH/nperf/raw/main/docs/images/dashboard.PNG)

## Deployment with Docker Compose

To deploy this project run

```bash
git clone https://github.com/AUThomasCH/nperf.git

cd nperf
```

Create a `.env` file in the projects directory.

Add the following configuration:

```
[NPERF]

# This defines the sleep time in seconds, before a new test is executed
nperf_interval = 300

# This addresses defines the servers which will be pinged, seperated with spaces!
# If a server isn't reacable, no value will be stored in the database!
latency_servers = 1.1.1.1 google.com github.com

[INFLUX_DB]
# This is the address of the influxdb
influx_url = "http://influxdb:8086"

# This is the authentication token. If you need to change or set it initially, just rerun 'docker-compose up' after it.
influx_token = _zqUe1mEHxmrcrJj9Ii8WZG0ZJU8yOUJ8nGHnhsrYwh2MfOU5AitI8LNktLTRQc-zKQzpKc_76-t9F5r4samaA==

influx_bucket = nperf
influx_org = nperf

```

Now start the project with docker-compose

```
docker-compose up
```

If everything runs, access the InfluxDB web interface at http://localhost:8086

You will need to do some initial configuration and generate a token for authentication.

After you generated a token, copy and paste it in the .env file and rerun `docker-compose up`.
nperf can now authenticate itself with the token.

Done!

## Contributing

Contributions are always welcome! Just open a Pull Request.

## License

[GNU General Public License v3.0](https://github.com/AUThomasCH/nperf/blob/main/LICENSE)
