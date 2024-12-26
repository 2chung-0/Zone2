import os

def rename_jpg_files():
    # 현재 디렉토리의 모든 파일 가져오기
    files = os.listdir('.')
    
    # JPG 파일만 필터링 (대소문자 모두 고려)
    jpg_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg'))]
    
    # 파일 이름 변경
    for index, file in enumerate(jpg_files, 1):
        new_name = f'zone3_childhood_{index}.jpg'
        
        try:
            os.rename(file, new_name)
            print(f'변경 완료: {file} -> {new_name}')
        except OSError as e:
            print(f'에러 발생 ({file}): {e}')

if __name__ == '__main__':
    # 실행 전 확인 메시지
    print('현재 폴더의 모든 JPG 파일의 이름을 변경합니다.')
    response = input('계속하시겠습니까? (y/n): ')
    
    if response.lower() == 'y':
        rename_jpg_files()
        print('모든 파일 이름 변경이 완료되었습니다.')
    else:
        print('작업이 취소되었습니다.')