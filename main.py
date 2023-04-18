# ecoding:utf-8
from PIL import Image
import piexif
from tkinter import filedialog


def main():
    filepath = filedialog.askopenfilenames(defaultextension=".jpg", filetypes=[("图片文件", ".jpg .png")], initialdir="desktop")
    print(filepath)
    gps_str = input('请输入经纬度：')
    arr = gps_str.split(',')
    lng = float(arr[1])
    lat = float(arr[0])
    print(lng)
    print(lat)

    # 将经纬度与相对航高转为exif可用的经纬度与行高
    # exif需要的航高输入为(20000,2)格式，表示高度为20000/100米
    # exif需要的经度与维度为((12, 1), (20,1), (41000, 1000))格式表示12度20分41秒
    lng_exif = format_latlng(lng)
    lat_exif = format_latlng(lat)
    _dict = {"lng": lng_exif, "lat": lat_exif, "lng_ref": 'E', "lat_ref": 'N'}

    for image_path in filepath:
        # image_path = browse(True)[1]
        print("写入文件：", image_path)
        # 修改图片的exif
        read_modify_exif(image_path, _dict)


def format_latlng(latlng):
    """经纬度十进制转为分秒"""
    degree = int(latlng)
    res_degree = latlng - degree
    minute = int(res_degree * 60)
    res_minute = res_degree * 60 - minute
    seconds = round(res_minute * 60.0, 3)

    return (degree, 1), (minute, 1), (int(seconds * 1000), 1000)


def read_modify_exif(image_path, _dict):
    """ 读取并且修改exif文件"""
    img = Image.open(image_path)  # 读图
    if img.info.get('exif'):
        exif_dict = piexif.load(img.info['exif'])  # 提取exif信息
    else:
        exif_dict = {'GPS': {}}
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitude] = _dict['lng']  # 修改经度
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitude] = _dict['lat']  # 修改纬度
    exif_dict['GPS'][piexif.GPSIFD.GPSLongitudeRef] = _dict['lng_ref']  # odm需要读取，一般为’W'
    exif_dict['GPS'][piexif.GPSIFD.GPSLatitudeRef] = _dict['lat_ref']  # 一般为‘N'

    exif_bytes = piexif.dump(exif_dict)
    print('lng:{} lat:{}'.format(exif_dict['GPS'][piexif.GPSIFD.GPSLongitude],
                                 exif_dict['GPS'][piexif.GPSIFD.GPSLatitude]))
    piexif.insert(exif_bytes, image_path)


if __name__ == "__main__":
    main()
