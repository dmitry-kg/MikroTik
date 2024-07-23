from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import ros_api

class RouterOSInfluxDBData:
    def __init__(self, router_host, router_user, router_password, influx_url, influx_token, influx_org, influx_bucket):
        self.router = ros_api.Api(router_host, user=router_user, password=router_password, port=8728)
        self.influx_client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
        self.influx_write_api = self.influx_client.write_api(write_options=SYNCHRONOUS)
        self.influx_bucket = influx_bucket

    def get_connection_data(self, dst_addresses, min_orig_rate):
        data = {}
        for dst_address in dst_addresses:
            data[dst_address] = {"src-address": [], "orig-repl-rate": []}

        r = self.router.talk(f'/ip/firewall/connection/print\nwhere\norig-rate>{min_orig_rate}')
        for entry in r:
            if "src-address" in entry:
                src_address = entry["src-address"].split(":")[0]
                dst_address = entry["dst-address"].split(":")[0]
                if dst_address in dst_addresses:
                    orig_repl_rate = int(entry["orig-rate"]) + int(entry["repl-rate"])
                    if src_address in data[dst_address]["src-address"]:
                        index = data[dst_address]["src-address"].index(src_address)
                        data[dst_address]["orig-repl-rate"][index] += orig_repl_rate
                    else:
                        data[dst_address]["src-address"].append(src_address)
                        data[dst_address]["orig-repl-rate"].append(orig_repl_rate)

        return data

    def send_data_to_influxdb(self, data):
        influx_data = []
        for dst_address, graph_data in data.items():
            src_addresses = graph_data["src-address"]
            orig_repl_rates = graph_data["orig-repl-rate"]
            for i in range(len(src_addresses)):
                if orig_repl_rates[i] > 0:
                    data_point = Point("connection_data") \
                        .tag("dst-address", dst_address) \
                        .tag("src-address", src_addresses[i]) \
                        .field("orig-repl-rate", orig_repl_rates[i])
                    influx_data.append(data_point)

        self.influx_write_api.write(bucket=self.influx_bucket, record=influx_data)

    def close(self):
        self.influx_client.close()

# Пример использования:
routeros_influx = RouterOSInfluxDBData(
    router_host='192.168.30.1',
    router_user='apiuser',
    router_password='gyPdEQZuCDr0XZUBJGg7W32',
    influx_url='http://192.168.30.148:8086',
    influx_token='tkRxMDTM5Y9I-M-PLaQIEWJLLpWWVFN_OklU_v3bIVCRP8PJVYXMHXReeDHaTRz3J-wEoS01eD2eiiD-kMkNbQ==',
    influx_org='DataCenter',
    influx_bucket='MikroTik'
)

desired_dst_addresses = ["217.29.18.146", "217.29.18.147", "217.29.18.148", "217.29.18.149","217.29.30.234", "217.29.30.235",
                         "217.29.30.236","217.29.30.237", "217.29.30.238",
                         "217.29.20.250", "217.29.20.251", "217.29.20.252", "217.29.20.253","217.29.20.254",
                         "217.29.30.42", "217.29.30.43","217.29.30.44", "217.29.30.45","217.29.30.46",
                         "217.29.30.90","217.29.30.91","217.29.30.92","217.29.30.93","217.29.30.94",
                         "217.29.18.146", "217.29.18.147", "217.29.18.148", "217.29.18.149", "217.29.18.150",
                         "217.29.18.194", "217.29.18.195", "217.29.18.196", "217.29.18.197", "217.29.18.198",
                         "217.29.19.90", "217.29.19.91", "217.29.19.92", "217.29.19.93", "217.29.19.94",
                         "217.29.20.194", "217.29.20.195", "217.29.20.196", "217.29.20.197", "217.29.20.198",
                         "217.29.22.106", "217.29.22.107", "217.29.22.108", "217.29.22.109", "217.29.22.110",
                         "217.29.26.58", "217.29.26.59", "217.29.26.60", "217.29.26.61", "217.29.26.62",
                         "217.29.26.210", "217.29.26.211", "217.29.26.212", "217.29.26.213", "217.29.26.214",
                         "217.29.26.215", "217.29.26.216", "217.29.26.217", "217.29.26.218", "217.29.26.219",
                         "217.29.26.220", "217.29.26.221", "217.29.26.222",
                         "77.235.22.50", "77.235.22.51", "77.235.22.52","77.235.22.53", "77.235.22.54",
                         "77.235.22.55", "77.235.22.56", "77.235.22.57", "77.235.22.58","77.235.22.59",
                         "77.235.22.60", "77.235.22.61","77.235.22.62",
                         "77.235.20.178", "77.235.20.179", "77.235.20.180","77.235.20.181","77.235.20.182","77.235.20.183","77.235.20.184",
                         "77.235.20.185","77.235.20.186","77.235.20.187","77.235.20.188","77.235.20.189", "77.235.20.190",
                         "77.235.20.170","77.235.20.171","77.235.20.172","77.235.20.173","77.235.20.174",
                         "77.235.20.42","77.235.20.43","77.235.20.44","77.235.20.45","77.235.20.46",
                        "212.112.116.233", "212.112.107.213", "212.112.116.231","212.112.116.236", "31.186.53.155", "31.186.53.149", "212.112.105.196",
                        "212.112.105.90", "212.112.105.91"
                         ]  # Добавьте другие адреса по желанию
min_orig_rate = 102400  # Минимальная скорость для фильтрации

data = routeros_influx.get_connection_data(desired_dst_addresses, min_orig_rate)
routeros_influx.send_data_to_influxdb(data)
routeros_influx.close()

