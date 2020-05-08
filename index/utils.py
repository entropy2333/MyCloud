import os
import qrcode
import base64

def judge_filepath(file_type):
    img_list = ['bmp', 'jpg', 'png', 'tif', 'gif', 'pcx', 'tga', 'exif', 'fpx', 'svg', 'psd', 'cdr', 'pcd', 'dxf',
                'ufo', 'eps', 'ai', 'raw', 'WMF', 'webp']
    doc_list = ['txt', 'doc', 'xls', 'ppt', 'docx', 'xlsx', 'pptx', 'lrc', 'wps', 'zip', 'rar', '7z', 'torrent', 'pdf']
    video_list = ['cd', 'ogg', 'mp3', 'asf', 'wma', 'wav', 'mp3pro', 'rm', 'mp4', 'real', 'ape', 'module', 'midi',
                  'vqf']
    procedure_list = ['exe', 'py', 'java', 'class', 'pyc', 'app', 'apk', 'bat']
    if file_type in img_list:
        file_path = 'img'
    elif file_type in doc_list:
        file_path = 'doc'
    elif file_type in video_list:
        file_path = 'video'
    elif file_type in procedure_list:
        file_path = 'procedure'
    else:
        file_path = 'others'
    return file_path


def format_size(old_size):
    if old_size <= 1024:
        return str(old_size) + 'B'
    elif 1024 < old_size <= 1024 * 1024:
        new_size = round(old_size / 1024, 2)
        return str(new_size) + 'KB'
    elif 1024 * 1024 < old_size <= 1024 * 1024 * 1024:
        new_size = round(old_size / (1024 * 1024), 2)
        return str(new_size) + 'MB'
    elif old_size > 1024 * 1024 * 1024:
        new_size = round(old_size / (1024 * 1024 * 1024), 2)
        return str(new_size) + 'GB'

def gen_qrcode(file_path, qr_dir='./'):
    share_url = base64.b64encode(file_path.encode())
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(share_url)
    qr.make(fit=True)

    img = qr.make_image()
    # save_path = '1.png'
    save_path = qr_dir + share_url.decode().replace('/','-') + '.png'
    img.save(save_path)
    with open(save_path,"rb") as f:
        img_str = base64.b64encode(f.read())
    os.remove(save_path)
    return share_url.decode(), img_str.decode()
