from obspy import read
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
import random

# InfluxDB 連接設置
bucket = "earthquake"
org = "earthquake_platform"
token = "7wrbNp7it-HGbKjc-xwPEyzG8RLrJbIGfvbWBIaGB3qmVImCl8uCXFdxMwN0IxUnOOgGnxKvYyj3jki1XWLGHg=="
url = "http://10.97.135.7:8086"

# 創建 InfluxDB 客戶端
client = InfluxDBClient(url=url, token=token, org=org, timeout=30_000)

# 創建寫入 API
write_api = client.write_api(write_options=SYNCHRONOUS)

# 生成假數據並寫入 InfluxDB
for i in range(5):  # 生成100條數據
    print(i)
    point = Point("earthquake") \
        .tag("sensor", "sensor1") \
        .field("value", random.uniform(20.0, 30.0)) \
        .time(int(time.time() * 1000000000) + i * 1000000000, WritePrecision.NS)

    # 寫入數據點到 InfluxDB
    write_api.write(bucket=bucket, org=org, record=point)

print("Fake data has been written to InfluxDB.")

# 關閉客戶端
client.close()