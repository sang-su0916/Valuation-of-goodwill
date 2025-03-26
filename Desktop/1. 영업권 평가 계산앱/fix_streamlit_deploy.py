import os
import shutil

# 필요한 파일들을 루트 디렉토리로 복사
files_to_move = ['app.py', 'requirements.txt', 'runtime.txt', 'packages.txt', '.env']

for file in files_to_move:
    # Desktop/1. 영업권 평가 계산앱 경로에 파일이 있는지 확인
    nested_path = os.path.join("Desktop", "1. 영업권 평가 계산앱", file)
    if os.path.exists(nested_path) and not os.path.exists(file):
        print(f"Moving {nested_path} to {file}")
        shutil.copy2(nested_path, file)
    elif os.path.exists(file):
        print(f"File already exists: {file}")
    else:
        print(f"File not found: {nested_path}")

print("Done. Files are now in the correct location for Streamlit deployment.") 