import shutil
print("gdal_translate path:", shutil.which("gdal_translate"))

import os
import subprocess

# 原始图像路径
input_file = "14_53_2_2_2m_v4.1_dem.tif"

# 原图右下角坐标
or_x = 1300100.0
or_y = -2650100.000

# 像素大小
pixel_size = 2.0
tile_size = 2048  # 每块2048像素

# 裁剪块的数量
rows = 6
cols = 6

# 原图起始坐标（左上角）
# origin_x = 1249900.0
# origin_y = -2599900.0
origin_x = or_x - cols * tile_size * pixel_size
origin_y = or_y + rows * tile_size * pixel_size

print(f'裁剪起点(x{origin_x}, y{origin_y})')

os.makedirs("tiles", exist_ok=True)

for row in range(rows):
    for col in range(cols):
        x_off = col * tile_size
        y_off = row * tile_size

        # # 最后一个 tile 可能不足 tile_size，需修正
        # w = min(tile_size, image_width - x_off)
        # h = min(tile_size, image_height - y_off)

        # 计算地理范围
        ulx = origin_x + x_off * pixel_size
        uly = origin_y - y_off * pixel_size  # y 是负的
        lrx = ulx + tile_size * pixel_size
        lry = uly - tile_size * pixel_size

        output_file = f"tiles/tile_r{row:02d}_c{col:02d}.tif"

        cmd = [
            "gdal_translate",
            "-projwin", str(ulx), str(uly), str(lrx), str(lry),
            "-of", "GTiff",
            "-co", "COMPRESS=LZW",
            input_file,
            output_file
        ]

        print(f"Exporting tile ({row}, {col}) -> {output_file}")
        subprocess.run(cmd)
