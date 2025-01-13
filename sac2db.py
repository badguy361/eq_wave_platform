from obspy import read
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import numpy as np
from dotenv import load_dotenv
import os
from datetime import timedelta
from tqdm import tqdm
from datetime import datetime

load_dotenv()
# InfluxDB 連線設定
bucket = os.getenv("influxdb_bucket")
org = os.getenv("influxdb_org")  # 替換成你的組織名稱
token = os.getenv("influxdb_token")  # 替換成你的 token
url = os.getenv("influxdb_endpoint")  # 替換成你的 InfluxDB 位址

# 建立 InfluxDB 客戶端
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# 讀取 SAC 文件
sac_file = read("../TSMIP_Dataset/20220918/TW.A002.10.HLE.D.20220918080200.SAC")[0]
starttime_utc = sac_file.stats.starttime.datetime

station_data = {
    'station': sac_file.stats.station,
    'channel': sac_file.stats.channel,
    'network': sac_file.stats.network,
    'location': sac_file.stats.location,
    'sampling_rate': sac_file.stats.sampling_rate,
    'starttime': starttime_utc,
}

# 設定要寫入的時間範圍（秒數）
start_time_seconds = 24280  # 起始秒數 06:44:40
end_time_seconds = 24500    # 結束秒數 06:50:00

sampling_rate = station_data['sampling_rate']
total_duration_seconds = end_time_seconds - start_time_seconds  # 總持續時間

start_index = int(start_time_seconds * sampling_rate)
end_index = int(end_time_seconds * sampling_rate)

# 確保索引不超出數據範圍
start_index = max(0, start_index)
end_index = min(len(sac_file.data), end_index)

# 打印索引範圍與總樣本數
print(f"開始寫入索引: {start_index}, 結束索引: {end_index}")
print(f"總樣本數: {end_index - start_index}")

# 將波形資料寫入 InfluxDB
for i, amplitude in enumerate(sac_file.data[start_index:end_index]):
    # 計算時間偏移量，保留小數秒
    current_time_offset_seconds = start_time_seconds + (i / sampling_rate)
    time_offset = timedelta(seconds=current_time_offset_seconds)
    timestamp = station_data['starttime'] + time_offset
    print(timestamp)
    # 創建數據點
    point = Point("seismic_data") \
        .tag("station", station_data['station']) \
        .tag("channel", station_data['channel']) \
        .tag("network", station_data['network']) \
        .field("amplitude", float(amplitude)) \
        .time(timestamp, WritePrecision.NS)
    
    # 寫入數據點
    write_api.write(bucket=bucket, org=org, record=point)

client.close()
print("資料已成功寫入 InfluxDB")
##################delete######################
# delete_api = client.delete_api()

# # 定义时间范围
# # 为了删除所有数据，可以使用从 Unix 时间开始到当前时间
# start = "1970-01-01T00:00:00Z"
# stop = datetime.utcnow().isoformat() + "Z"

# # 定义删除的 predicate（条件）
# # 这里我们删除 _measurement 为 "seismic_data" 的所有数据
# predicate = '_measurement="seismic_data"'

# try:
#     # 执行删除操作
#     delete_api.delete(
#         start=start,
#         stop=stop,
#         predicate=predicate,
#         bucket=bucket,
#         org=org
#     )
#     print("Measurement 'seismic_data' 的所有数据已被删除。")
# except Exception as e:
#     print(f"删除数据时出错: {e}")

# client.close()
