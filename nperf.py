import os
import time
from pathlib import Path

import speedtest
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from ping3 import ping as runPingTest


load_dotenv()
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


nperf_interval = os.getenv('nperf_interval')
latency_servers = os.getenv('latency_servers')
influx_url = os.getenv('influx_url')
influx_token = os.getenv('influx_token')
influx_bucket = os.getenv('influx_bucket')
influx_org = os.getenv('influx_org')


client = InfluxDBClient(url=influx_url, token=influx_token)


def run_speedtest():
    try:
        servers = []
        threads = None

        s = speedtest.Speedtest()
        s.get_servers(servers)
        s.get_best_server()
        s.download(threads=threads)
        s.upload(threads=threads)

        data = s.results.dict()

        download_speed = round(data['download'] * 0.000001, 2)
        upload_speed = round(data['upload'] * 0.000001, 2)
        ping = data['ping']

        return {'Download': download_speed,
                'Upload': upload_speed,
                'Ping': ping}

    except Exception as e:
        print('❌ Error while performing speed test: ', e)
        pass


def run_latency_test():
    latency_data = {}

    try:
        servers = latency_servers.split()

        try:
            for server in servers:
                pingResult = runPingTest(server)

                if isinstance(pingResult, float):
                    latency_data[server] = round(pingResult * 1000, 2)
                else:
                    pass

            return latency_data

        except Exception as e:
            print('❌ Error while performing latency test: ', e)
            pass

    except KeyError:
        print("No custom servers for latency tests defined.")
        pass


def store_data(filter, dict):
    try:
        for items in dict:
            key = items
            value = dict[items]

            string = (filter + ' ' + str(key) + '=' + str(value))

            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(influx_bucket, influx_org, string)

            print('✅ ' + filter + ' data uploaded to influxdb.')

    except Exception as e:
        print('❌ Could not store data to influxdb: ', e)
        pass


def nperf():
    interval = int(nperf_interval)

    if isinstance(interval, int) and interval >= 30:

        while True:

            print('----------------')
            print("⚡ nperf started")

            store_data('Speed', run_speedtest())
            store_data('Latency', run_latency_test())

            print('----------------')
            print('')

            time.sleep(interval)

    else:
        print("Please define a interval value >= 30!")


nperf()
