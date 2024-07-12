from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS
import ros_api

# Подключение к RouterOS API
router = ros_api.Api('192.168.30.1', user='apiuser', password='gyPdEQZuCDr0XZUBJGg7W32', port=8728)

# Выполнение запроса к API
r = router.talk('/ip/firewall/connection/print\nwhere\norig-rate>0')
#print(r)
# Подготовка данных для InfluxDB
#AKNET
desired_src_addresses = ["212.112.116.233", "212.112.107.213", "212.112.116.231","212.112.116.236", "31.186.53.155", "31.186.53.149"]
src_ip_orig_rate_sum = {}
src_ip_repl_rate_sum = {}
dst_ip_orig_rate_sum = {}
dst_ip_repl_rate_sum = {}
src_ip_rates = {}
dst_ip_rates = {}

##SAIMA-128107
desired_src_addresses_saima = ["217.29.30.234", "217.29.30.235", "217.29.30.236","217.29.30.237", "217.29.30.238",
                               "217.29.20.250", "217.29.20.251", "217.29.20.252", "217.29.20.253","217.29.20.254",
                               "217.29.30.42", "217.29.30.43","217.29.30.44", "217.29.30.45","217.29.30.46",
                               "217.29.30.90","217.29.30.91","217.29.30.92","217.29.30.93","217.29.30.94",
                               "217.29.26.210", "217.29.26.211", "217.29.26.212", "217.29.26.213",
                               "217.29.26.214", "217.29.26.215", "217.29.26.216", "217.29.26.217",
                               "217.29.26.218", "217.29.26.219", "217.29.26.220", "217.29.26.221",
                               "217.29.26.222" ]
src_ip_orig_rate_sum_saima = {}
src_ip_repl_rate_sum_saima = {}
dst_ip_orig_rate_sum_saima = {}
dst_ip_repl_rate_sum_saima = {}
src_ip_rates_saima = {}
dst_ip_rates_saima = {}


##SAIMA-119201
desired_src_addresses_saima_119201 = ["217.29.18.146", "217.29.18.147", "217.29.18.148","217.29.18.149", "217.29.18.150",
                               "217.29.18.194", "217.29.18.195", "217.29.18.196", "217.29.18.197","217.29.18.198",
                               "217.29.19.90", "217.29.19.91","217.29.19.92", "217.29.19.93","217.29.19.94",
                               "217.29.20.194","217.29.20.195","217.29.20.196","217.29.20.197","217.29.20.198",
                               "217.29.22.106","217.29.22.107","217.29.22.108","217.29.22.109","217.29.22.110",
                               "217.29.26.58","217.29.26.59","217.29.26.60","217.29.26.61","217.29.26.62"]
src_ip_orig_rate_sum_saima_119201 = {}
src_ip_repl_rate_sum_saima_119201 = {}
dst_ip_orig_rate_sum_saima_119201 = {}
dst_ip_repl_rate_sum_saima_119201 = {}
src_ip_rates_saima_119201 = {}
dst_ip_rates_saima_119201 = {}


#MEGALINE
desired_src_addresses_megaline = ["77.235.22.50", "77.235.22.51", "77.235.22.52","77.235.22.53", "77.235.22.54",
                               "77.235.22.55", "77.235.22.56", "77.235.22.57", "77.235.22.58","77.235.22.59",
                               "77.235.22.60", "77.235.22.61","77.235.22.62",
                               "77.235.20.178", "77.235.20.179", "77.235.20.180","77.235.20.181","77.235.20.182","77.235.20.183","77.235.20.184",
                               "77.235.20.185","77.235.20.186","77.235.20.187","77.235.20.188","77.235.20.189", "77.235.20.190",
                               "77.235.20.170","77.235.20.171","77.235.20.172","77.235.20.173","77.235.20.174",
                               "77.235.20.42","77.235.20.43","77.235.20.44","77.235.20.45","77.235.20.46"

                                ]
src_ip_orig_rate_sum_megaline = {}
src_ip_repl_rate_sum_megaline = {}
dst_ip_orig_rate_sum_megaline = {}
dst_ip_repl_rate_sum_megaline = {}
src_ip_rates_megaline = {}
dst_ip_rates_megaline = {}

###SRC-AKNET
for entry in r:
    src_ip = entry["src-address"].split(":")[0]  # Получение IP-адреса без порта
    orig_rate = int(entry["orig-rate"])
    repl_rate = int(entry["repl-rate"])

    if src_ip in desired_src_addresses:  # Фильтрация по IP-адресам
        if src_ip not in src_ip_rates:
            src_ip_rates[src_ip] = 0

        src_ip_rates[src_ip] += orig_rate + repl_rate


###SRC-MEGALINE
for entry_megaline in r:
    src_ip = entry_megaline["src-address"].split(":")[0]  # Получение IP-адреса без порта
    orig_rate = int(entry_megaline["orig-rate"])
    repl_rate = int(entry_megaline["repl-rate"])

    if src_ip in desired_src_addresses_megaline:  # Фильтрация по IP-адресам
        if src_ip not in src_ip_rates_megaline:
            src_ip_rates_megaline[src_ip] = 0

        src_ip_rates_megaline[src_ip] += orig_rate + repl_rate

###SRC-SAIMA-119201
for entry_saima_119201 in r:
    src_ip = entry_saima_119201["src-address"].split(":")[0]  # Получение IP-адреса без порта
    orig_rate = int(entry_saima_119201["orig-rate"])
    repl_rate = int(entry_saima_119201["repl-rate"])

    if src_ip in desired_src_addresses_saima_119201:  # Фильтрация по IP-адресам
        if src_ip not in src_ip_rates_saima_119201:
            src_ip_rates_saima_119201[src_ip] = 0

        src_ip_rates_saima_119201[src_ip] += orig_rate + repl_rate

###SRC-SAIMA
for entry_saima in r:
    src_ip = entry_saima["src-address"].split(":")[0]  # Получение IP-адреса без порта
    orig_rate = int(entry_saima["orig-rate"])
    repl_rate = int(entry_saima["repl-rate"])

    if src_ip in desired_src_addresses_saima:  # Фильтрация по IP-адресам
        if src_ip not in src_ip_rates_saima:
            src_ip_rates_saima[src_ip] = 0

        src_ip_rates_saima[src_ip] += orig_rate + repl_rate


###DST-AKNET
for entry in r:
    dst_ip = entry["dst-address"].split(":")[0]  # Получение IP-адреса без порта
    orig_rate = int(entry["orig-rate"])
    repl_rate = int(entry["repl-rate"])

    if dst_ip in desired_src_addresses:  # Фильтрация по IP-адресам
        if dst_ip not in dst_ip_rates:
            dst_ip_rates[dst_ip] = 0

        dst_ip_rates[dst_ip] += orig_rate + repl_rate

###DST-SAIMA
for entry_saima in r:
    dst_ip = entry_saima["dst-address"].split(":")[0]  # Получение IP-адреса без порта
    orig_rate = int(entry_saima["orig-rate"])
    repl_rate = int(entry_saima["repl-rate"])

    if dst_ip in desired_src_addresses_saima:  # Фильтрация по IP-адресам
        if dst_ip not in dst_ip_rates_saima:
            dst_ip_rates_saima[dst_ip] = 0

        dst_ip_rates_saima[dst_ip] += orig_rate + repl_rate

###DST-SAIMA-119201
for entry_saima_119201 in r:
    dst_ip = entry_saima_119201["dst-address"].split(":")[0]  # Получение IP-адреса без порта
    orig_rate = int(entry_saima_119201["orig-rate"])
    repl_rate = int(entry_saima_119201["repl-rate"])

    if dst_ip in desired_src_addresses_saima_119201:  # Фильтрация по IP-адресам
        if dst_ip not in dst_ip_rates_saima_119201:
            dst_ip_rates_saima_119201[dst_ip] = 0

        dst_ip_rates_saima_119201[dst_ip] += orig_rate + repl_rate

###DST-MEGALINE
for entry_megaline in r:
    dst_ip = entry_megaline["dst-address"].split(":")[0]  # Получение IP-адреса без порта
    orig_rate = int(entry_megaline["orig-rate"])
    repl_rate = int(entry_megaline["repl-rate"])

    if dst_ip in desired_src_addresses_megaline:  # Фильтрация по IP-адресам
        if dst_ip not in dst_ip_rates_megaline:
            dst_ip_rates_megaline[dst_ip] = 0

        dst_ip_rates_megaline[dst_ip] += orig_rate + repl_rate

##SRC_SUMMARY_AKNET
for entry in r:
    src_ip = entry["src-address"].split(":")[0]  # Получение IP-адреса без порта

    if src_ip in desired_src_addresses:  # Фильтрация по IP-адресам
        orig_rate = int(entry["orig-rate"])

        if src_ip in src_ip_orig_rate_sum:
            src_ip_orig_rate_sum[src_ip] += orig_rate
        else:
            src_ip_orig_rate_sum[src_ip] = orig_rate
        repl_rate = int(entry["repl-rate"])
        if src_ip in src_ip_repl_rate_sum:
            src_ip_repl_rate_sum[src_ip] += repl_rate
        else:
            src_ip_repl_rate_sum[src_ip] = repl_rate

##DST_SUMMARY_AKNET
for entry in r:
    src_ip = entry["dst-address"].split(":")[0]  # Получение IP-адреса без порта

    if src_ip in desired_src_addresses:  # Фильтрация по IP-адресам
        orig_rate = int(entry["orig-rate"])

        if src_ip in dst_ip_orig_rate_sum:
            dst_ip_orig_rate_sum[src_ip] += orig_rate
        else:
            dst_ip_orig_rate_sum[src_ip] = orig_rate
        repl_rate = int(entry["repl-rate"])
        if src_ip in dst_ip_repl_rate_sum:
            dst_ip_repl_rate_sum[src_ip] += repl_rate
        else:
            dst_ip_repl_rate_sum[src_ip] = repl_rate


influx_data = []


##COunt COnnections

# Переменная для подсчета количества ID
id_count = 0

# Перебор элементов в списке response
for entry in r:
    if '.id' in entry:
        id_count += 1

data_point = Point("firewall_connection_count") \
    .field("id_count", id_count)
influx_data.append(data_point)



###SRC_AKNET
for src_ip, total_rate in src_ip_rates.items():
    data_point = Point("fw_connections_summary") \
        .tag("src_address", src_ip) \
        .field("src_total_rate", total_rate)
    influx_data.append(data_point)

###DST_AKNET
for dst_ip, total_rate in dst_ip_rates.items():
    data_point = Point("fw_connections_summary") \
        .tag("dst_address", dst_ip) \
        .field("dst_total_rate", total_rate)
    influx_data.append(data_point)


###SRC_SAIMA
for src_ip, total_rate in src_ip_rates_saima.items():
    data_point = Point("fw_connections_summary_saima") \
        .tag("src_address", src_ip) \
        .field("src_total_rate", total_rate)
    influx_data.append(data_point)
###DST_SAIMA
for dst_ip, total_rate in dst_ip_rates_saima.items():
    data_point = Point("fw_connections_summary_saima") \
        .tag("dst_address", dst_ip) \
        .field("dst_total_rate", total_rate)
    influx_data.append(data_point)


###SRC_SAIMA-119201
for src_ip, total_rate in src_ip_rates_saima_119201.items():
    data_point = Point("fw_connections_summary_saima_119201") \
        .tag("src_address", src_ip) \
        .field("src_total_rate", total_rate)
    influx_data.append(data_point)
###DST_SAIMA-119201
for dst_ip, total_rate in dst_ip_rates_saima_119201.items():
    data_point = Point("fw_connections_summary_saima_119201") \
        .tag("dst_address", dst_ip) \
        .field("dst_total_rate", total_rate)
    influx_data.append(data_point)

###SRC_MEGALINE
for src_ip, total_rate in src_ip_rates_megaline.items():
    data_point = Point("fw_connections_summary_megaline") \
        .tag("src_address", src_ip) \
        .field("src_total_rate", total_rate)
    influx_data.append(data_point)
###DST_MEGALINE
for dst_ip, total_rate in dst_ip_rates_megaline.items():
    data_point = Point("fw_connections_summary_megaline") \
        .tag("dst_address", dst_ip) \
        .field("dst_total_rate", total_rate)
    influx_data.append(data_point)

#############################################
for src_ip, src_total_orig_rate in src_ip_orig_rate_sum.items():
    data_point = Point("src_orig_rate_fw_connections_summary") \
        .tag("src_address", src_ip) \
        .field("total_orig_rate", src_total_orig_rate)


    influx_data.append(data_point)

for src_ip, src_total_repl_rate in src_ip_repl_rate_sum.items():
    data_point = Point("src_repl_rate_fw_connections_summary") \
        .tag("src_address", src_ip) \
        .field("total_repl_rate", src_total_repl_rate)


    influx_data.append(data_point)

for src_ip, dst_total_orig_rate in dst_ip_orig_rate_sum.items():
    data_point = Point("dst_orig_rate_fw_connections_summary") \
        .tag("dst_address", src_ip) \
        .field("total_orig_rate", dst_total_orig_rate)

    influx_data.append(data_point)

for src_ip, dst_total_repl_rate in dst_ip_repl_rate_sum.items():
    data_point = Point("dst_repl_rate_fw_connections_summary") \
        .tag("dst_address", src_ip) \
        .field("total_repl_rate", dst_total_repl_rate)

    influx_data.append(data_point)
#         total_orig_rate += int(entry["orig-rate"])
# print("Total orig_rate:", total_orig_rate)
# Подключение к InfluxDB v2 и отправка данных
url = "http://192.168.30.148:8086"
token = "tkRxMDTM5Y9I-M-PLaQIEWJLLpWWVFN_OklU_v3bIVCRP8PJVYXMHXReeDHaTRz3J-wEoS01eD2eiiD-kMkNbQ=="
org = "DataCenter"
bucket = "MikroTik"
# print(src_ip_orig_rate_sum)
# print(src_ip_repl_rate_sum)
# print(src_ip_rates)
#
# print(src_ip_rates_saima)
# print(dst_ip_rates_saima)

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)
write_api.write(bucket=bucket, record=influx_data)

# Закройте соединение с InfluxDB
client.close()
