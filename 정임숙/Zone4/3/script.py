import os
import shutil
from pathlib import Path
from PIL import Image

# 현재 스크립트가 있는 폴더를 대상으로 처리
current_folder = Path(__file__).parent

# 지원하는 이미지 확장자
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif'}

# 이미지 파일만 필터링 (script.py와 door.jpg 제외)
image_files = []
for f in current_folder.iterdir():
    if f.suffix.lower() in IMAGE_EXTENSIONS and f.name != 'door.jpg' and f.name != 'script.py':
        image_files.append(f)

if not image_files:
    print("No image files found in current folder")
    exit()

# 이미지 파일들을 수정 시간순으로 정렬
image_files.sort(key=lambda x: x.stat().st_mtime)

# 이미지를 jpg로 변환하여 저장하는 함수
def save_as_jpg(input_path, output_path):
    with Image.open(input_path) as img:
        # RGBA 이미지인 경우 RGB로 변환
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[3])
            img = background
        # 다른 모드의 이미지는 RGB로 변환
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        img.save(output_path, 'JPEG', quality=95)

# 첫 번째 이미지를 door.jpg로 변환하여 저장
door_file = current_folder / "door.jpg"
try:
    save_as_jpg(image_files[0], door_file)
    print(f"Created door texture: door.jpg")
except Exception as e:
    print(f"Error creating door texture: {e}")
    exit()

# 처리된 원본 파일들을 저장할 목록
processed_files = set()

# 나머지 이미지들의 이름을 1.jpg, 2.jpg 등으로 변경
for i, old_file in enumerate(image_files, 1):
    new_name = f"{i}.jpg"
    new_file = current_folder / new_name
    
    try:
        save_as_jpg(old_file, new_file)
        print(f"Created {new_name}")
        processed_files.add(old_file)
    except Exception as e:
        print(f"Error processing {old_file.name}: {e}")

# 처리가 완료된 원본 파일 삭제
print("\nCleaning up original files...")
for file in processed_files:
    try:
        file.unlink()
        print(f"Deleted original file: {file.name}")
    except Exception as e:
        print(f"Error deleting {file.name}: {e}")