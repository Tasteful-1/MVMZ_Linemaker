#########################################################################################
# RPG MAKER MV & MZ Line Maker_Private_resource
# 작성 : tasteful
# json 파일을 깔끔하게 정리해줍니다.
# 이 코드는 타인의 사용을 고려하지 않았습니다.
# 수정 및 개선, 재배포는 자유롭게 하셔도 좋습니다.
#
# URL : https://github.com/Tasteful-1/MVMZ_Linemaker
#########################################################################################

import os
import re
import sys
import requests
import tkinter as tk
from tkinter import messagebox
import traceback

# 현재 프로그램 버전
CURRENT_VERSION = "2.6.6"

# 현재 스크립트의 디렉토리 경로 얻기
current_dir = os.path.dirname(os.path.abspath(__file__))

# 데이터 폴더 및 js/plugins.js 파일 경로 설정
data_folder_path = os.path.join(current_dir, '..//..//Ex_Main//data')
system_file_path = os.path.join(current_dir, '..//..//Ex_Main//data', 'system.json')
js_folder_path = os.path.join(current_dir, '..//..//Ex_Main//js', 'plugins.js')

# 서버에서 업데이트 정보 확인
def check_for_update():
	update_info_url = "https://raw.githubusercontent.com/Tasteful-1/MVMZ_Linemaker/refs/heads/main/update_info.json"
	try:
		response = requests.get(update_info_url)
		response.raise_for_status()
		update_info = response.json()

		latest_version = update_info["latest_version"]
		download_url = update_info["download_url"]
		changelog = update_info.get("changelog", "변경 사항 없음.")

		if latest_version > CURRENT_VERSION:
			# 업데이트 알림 팝업 표시
			message = (
				f"업데이트가 존재합니다!\n\n"
				f"현재 버전: {CURRENT_VERSION}\n"
				f"최신 버전: {latest_version}\n\n"
				f"변경 사항:\n{changelog}\n\n"
				"업데이트를 다운로드하시겠습니까?"
			)
			choice = tk.messagebox.askyesno("업데이트 확인", message)  # 예/아니오 팝업
			if choice:
				download_update(download_url)  # 예를 선택한 경우 업데이트 다운로드
			else:
				print("업데이트를 건너뜁니다.")
	except Exception as e:
		tk.messagebox.showerror("업데이트 오류", f"업데이트 확인 중 오류 발생: {e}")

# 업데이트 다운로드 및 실행
def download_update(download_url):
	try:
		# 저장 디렉토리 설정
		save_dir = current_dir
		os.makedirs(save_dir, exist_ok=True)  # 디렉토리가 없으면 생성

		# 파일 이름과 경로 설정
		file_name = download_url.split("/")[-1]
		file_path = os.path.join(save_dir, file_name)
		print(f"{file_name} 다운로드 중...")
		response = requests.get(download_url, stream=True)
		with open(file_name, "wb") as file:
			for chunk in response.iter_content(chunk_size=8192):
				file.write(chunk)
		print(f"다운로드 완료: {file_name}")
		print(f"갱신된 파일로 재실행 해주십시오")
		sys.exit()  # 업데이트 후 프로그램 종료
	except Exception as e:
		print(f"업데이트 다운로드 중 오류 발생: {e}")

if __name__ == "__main__":
	check_for_update()

def show_popup(title, message):
	# 팝업 메시지 표시
	messagebox.showinfo(title, message)

def modify_file(file_path, modifications, exclusions=None, max_passes=10):
	if exclusions is None:
		exclusions = []

	try:
		with open(file_path, 'r', encoding='utf-8') as file:
			content = file.read()

		modified_content = content
		for _ in range(max_passes):
			previous_content = modified_content

			# 제외 패턴을 찾아 제외 부분은 그대로 유지하고 나머지 부분만 수정
			excluded_sections = []
			last_end = 0
			for match in re.finditer(f"({'|'.join(exclusions)})", modified_content):
				start, end = match.span()
				# 제외 패턴 앞부분은 수정 대상으로 저장
				excluded_sections.append((modified_content[last_end:start], False))
				# 제외 패턴 부분은 그대로 저장
				excluded_sections.append((modified_content[start:end], True))
				last_end = end
			# 마지막 부분 추가
			excluded_sections.append((modified_content[last_end:], False))

			# 수정 대상 부분만 수정 적용
			modified_content = ""
			for text, is_excluded in excluded_sections:
				if not is_excluded:
					for old_str, new_str in modifications:
						text = text.replace(old_str, new_str)
				modified_content += text

			if previous_content == modified_content:
				break

		with open(file_path, 'w', encoding='utf-8') as file:
			file.write(modified_content)
		print(f"Modified file: {file_path}")

	except Exception as e:
		error_message = f"오류 발생 {file_path}: {e}"
		print(error_message)
		traceback.print_exc()
		print("오류 발생", error_message)

#선처리1
data_modifications1 = [
	('namepop  ', 'namepop_ζε'),
	('    ', ''),
	('   ', ''),
	('  ', ''),
	('\n', ''),
	('{ "','{"'),
	(', "',',"'),
	(' ]}',']}'),
	(', {',',{'),
	(' \\\\C[','\\\\C['),
	('namepop_ζε','namepop  '),
]

#선처리2
data_modifications2 = [
	('\n', ''),
	('\t', ''),
	('" ', '"'),
	(' : ', '￥★￥'),
	(': ',':'),
]

#메인
data_modifications3 = [
	('"[null,', '"[널,'),
	('null]"]},', '널]"]},'),
	('},{"id', '},\n{"id'),
	('},{"code', '},\n{"code'),
	(',"list": [{"code"', ',"list": [\n{"code"'),
	(',"list":[{"code"', ',"list":[\n{"code"'),
	(',{"list":[{"code"', ',{"list":[\n{"code"'),
	('{"autoplayBgm"', '{\n"autoplayBgm"'),
	(',"data":[', ',\n"data":['),
	('],"events":[', '],\n"events":['),
	('"events":[null,', '"events":[\nnull,'),
	('null,{"id"', 'null,\n{"id"'),
	('},null', '},\nnull'),
	('null]', 'null\n]'),
	('[null,{"id":1', '[\nnull,\n{"id":1'),
	('[null,', '[\nnull,'),
	('[null\n]', '[\nnull\n]'),
]

#후처리
data_modifications4 = [
	('}\n]\n}', '}]}'),
	('null\n]\n}', 'null]}'),
	('"events":[\n]\n}', '"events":[]'),
 	('"[널,', '"[null,'),
 	('널]"]},', 'null]"]},'),
	('￥★￥', ' : '),
	('[6,null\n]', '[6,null]'),
]

js_modifications1 = [
	('    ', ''),
	('   ', ''),
	('  ', ''),
	('\n', ''),
	('\t', ''),
	('" ', '"'),
	('{ "','{"'),
	(', "',',"'),
	(' ]}',']}'),
	(' {','{'),
	(' \\\\C[','\\\\C[')
]

js_modifications2 = [
	('var $plugins = [{"name"', '// Generated by RPG Maker.\n// Do not edit this file directly.\nvar $plugins =\n[\n{"name"'),
	('var $plugins =[{"name"', '// Generated by RPG Maker.\n// Do not edit this file directly.\nvar $plugins =\n[\n{"name"'),
	('// Generated by RPG Maker.// Do not edit this file directly.// Generated by RPG Maker.\n// Do not edit this file directly.', '// Generated by RPG Maker.\n// Do not edit this file directly.'),
	('},{"name', '},\n\n{"name'),
	('","parameters":', '",\n"parameters":\n'),
	('","', '",\n"'),
	('}}];', '}}\n];'),
	('": ', '":'),
]

system_modification = [
	(',"switches":[',',\n\n"switches":['),
	('],"terms":','],\n\n"terms":'),
	('},"variables":[','},\n\n"variables":['),
	('],"versionId"','],\n\n"versionId"'),
]

# 제외할 패턴 예시
exclusions1 = [
	r'<(?![^>]*/>)[a-zA-Z][^>]*>',
	r'\[\"[^\"]*\"\]',
	r',\"[^\"]*\",',
	r'"note":\s*"([^"]*?)"',
	r'"name":\s*"([^"]*?)"',
	r'"characterName":\s*"([^"]*?)"',
	r'"battlerName":\s*"([^"]*?)"',
	r'"battleback1Name":\s*"([^"]*?)"',
	r'"battleback2Name":\s*"([^"]*?)"',
	r'"description":\s*"([^"]*?)"',
	r':\d+,"indent":\d+,"parameters":\[((?:\[(?:"[^"]*"(?:\s*,\s*)*)*\]|"[^"]*"|\d+)(?:\s*,\s*)*)+\]',
]  # 여기에서 제외할 패턴을 정규식으로 추가

# 제외할 패턴 예시
exclusions2 = [r'<[^>]*?(?=>|"\]\})']  # 여기에서 제외할 패턴을 정규식으로 추가
exclusions3 = [r'ι']  # 여기에서 제외할 패턴을 정규식으로 추가

# 데이터 폴더가 존재하는지 확인
if not os.path.isdir(data_folder_path):
	print("디렉토리 찾기 오류", "data 폴더를 찾을 수 없습니다.")
else:
	for folder_path, _, filenames in os.walk(data_folder_path):
		for filename in filenames:
			if filename.endswith('.json'):
				file_path = os.path.join(folder_path, filename)
				modify_file(file_path, data_modifications1 + data_modifications2 + data_modifications3 + data_modifications4, exclusions=exclusions1)

# 시스템파일이 존재하는지 확인
if not os.path.isfile(system_file_path):
	print("디렉토리 찾기 오류", "system.json 을 찾을 수 없습니다.")
else:
	modify_file(system_file_path, system_modification, exclusions=exclusions2)

# js/plugins.js 파일이 존재하는지 확인
if not os.path.isfile(js_folder_path):
	print("파일 찾기 오류", "js/plugins.js 파일을 찾을 수 없습니다.")
else:
	modify_file(js_folder_path, js_modifications1 + js_modifications2, exclusions=exclusions3)

# tkinter 루프 실행
#root = tk.Tk()
#root.withdraw()  # 기본 윈도우 숨기기
#show_popup("완료", "작업이 종료되었습니다.")
