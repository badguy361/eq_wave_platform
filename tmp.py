from obspy import read

# 讀取 SAC 文件
sac_file = read("./TSMIP_Dataset/20220918/TW.A002.10.HLE.D.2022.261.000000.SAC")[0]

# 查看頭文件信息
print(sac_file.stats.sac)