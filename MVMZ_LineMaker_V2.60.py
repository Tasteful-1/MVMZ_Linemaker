#########################################################################################
# RPG MAKER MV & MZ Line Maker V2.60
# 작성 : tasteful
# json 파일을 깔끔하게 정리해줍니다.
# 이 코드는 타인의 사용을 고려하지 않았습니다.
# 수정 및 개선, 재배포는 자유롭게 하셔도 좋습니다.
#
#V1.00: 최초작성 : 24-08-05
#     : 특정 문자열을 치환하는 방식으로 라인을 정리합니다.
#     : 동작이 불안정하며 불완전하여 3회에 걸쳐 기능이 반복됩니다.
#V2.00: 업데이트 : 24-10-04
#     : 여타 추출툴로 수정이 가해진 파일에 대해서도 한번에 정리될 수 있도록 개선하였습니다.
#     : 이제 한번의 수정만으로 누락없는 정리가 가능해졌으며 소요시간이 대폭 단축되었습니다.
#     : 보다 온전한 수정을 위해 base_modifications 를 별도로 분리하였습니다.
#     : MK1 : plugins.js에 대하여 오직 name만을 기준으로 정리합니다.
#     : MK2 : Plugins.js에 대하여 parameters를 기준으로 추가정리합니다.
#V2.10: 업데이트 : 24-10-05
#	  : Plugins.js에 대한 추가정리 로직을 변경하였습니다.
#V2.20: 업데이트 : 24-10-07
#     : Data//.json에 대한 수식을 강화하였습니다.
#     : 작업종료 및 오류발생 팝업 메세지를 추가하였습니다.
#V2.30: 업데이트 : 24-10-10
#	  : 수식을 소폭 강화하였습니다.
#V2.40: 업데이트 : 24-10-12
#     : Plugins.js에 대한 수식을 소폭 강화하였습니다.
#     : data 폴더가 없을 경우 플러그인까지 적용이 안되는 오류를 수정하였습니다.
#V2.41: 업데이트 : 24-10-18
#     : namepop 플러그인과 관련된 이슈를 임시조치하였습니다.
#V2.42: 업데이트 : 24-10-27
#     : namepop 플러그인과 관련된 이슈를 완전해결하였습니다.
#V2.43: 업데이트 : 24-10-30
#     : memo 관련 플러그인들과 관련된 이슈를 임시조치하였습니다.
#V2.44: 업데이트 : 24-11-04
#     : null과 관련된 이슈를 해결하였습니다.
#     : memo 관련 이슈를 해결하였습니다.
#V2.45: 업데이트 : 24-11-06
#     : code 403에 대한 null에 한하여 줄바꿈을 제외하였습니다.
#     : 줄정리의 대상을 확장자가 json인 파일로 제한하였습니다.
#V2.50: 업데이트 : 24-11-10
#     : 더 구체적인 수정 대상 텍스트의 선별을 위해 정규식을 추가하였습니다.
#     : 더 이상 < > 속에 포함된 텍스트는 변형시키지 않습니다.
#V2.51: 업데이트 : 24-11-12
#     : 정규식을 하나 추가하였으며, 그를 위해 정규식 활용 방식을 변경하였습니다.
#     : 더 이상 "note":"" 속에 포함된 텍스트를 변형시키지 않습니다.
#V2.52: 업데이트 : 24-11-13
#     : 정규식을 복수 추가하였습니다.
#     : 가능한 파일명이나 데이터 값에 해당하는 텍스트를 변형시키지 않도록 조정하였습니다.
#V2.53: 업데이트 : 24-11-21
#     : 플러그인 구조변경을 경미하게 개선하였습니다.
#V2.54: 업데이트 : 24-12-04
#     : 플러그인 구조변경을 경미하게 개선하였습니다.
#V2.60: 업데이트 : 24-12-06
#     : 예외 정규식을 추가하였습니다.
#########################################################################################

import os
import re
import tkinter as tk
from tkinter import messagebox

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
        show_popup("오류 발생", error_message)

# 현재 스크립트의 디렉토리 경로 얻기
current_dir = os.path.dirname(os.path.abspath(__file__))

# 데이터 폴더 및 js/plugins.js 파일 경로 설정
data_folder_path = os.path.join(current_dir, 'data')
js_folder_path = os.path.join(current_dir, 'js', 'plugins.js')

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

# 제외할 패턴 예시
exclusions1 = [
    r'<(?![^>]*/>)[a-zA-Z][^>]*>',
    r'\[\"[^\"]*\"\]',
    r',\"[^\"]*\",',
    r'"note":\s*"([^"]*?)"',
    r'"name":\s*"([^"]*?)"',
    r'"characterName":\s*"([^"]*?)"',
    r'"battleback1Name":\s*"([^"]*?)"',
    r'"battleback2Name":\s*"([^"]*?)"',
    r'"description":\s*"([^"]*?)"',
    r':\d+,"indent":\d+,"parameters":\[[^\]]*\]',
]  # 여기에서 제외할 패턴을 정규식으로 추가

# 제외할 패턴 예시
exclusions2 = [r'<[^>]*>']  # 여기에서 제외할 패턴을 정규식으로 추가

# 데이터 폴더가 존재하는지 확인
if not os.path.isdir(data_folder_path):
    show_popup("디렉토리 찾기 오류", "data 폴더를 찾을 수 없습니다.")
else:
    for folder_path, _, filenames in os.walk(data_folder_path):
        for filename in filenames:
            if filename.endswith('.json'):
                file_path = os.path.join(folder_path, filename)
                modify_file(file_path, data_modifications1 + data_modifications2 + data_modifications3 + data_modifications4, exclusions=exclusions1)

# js/plugins.js 파일이 존재하는지 확인
if not os.path.isfile(js_folder_path):
    show_popup("파일 찾기 오류", "js/plugins.js 파일을 찾을 수 없습니다.")
else:
    modify_file(js_folder_path, js_modifications1 + js_modifications2, exclusions=exclusions2)

# tkinter 루프 실행
root = tk.Tk()
root.withdraw()  # 기본 윈도우 숨기기
show_popup("완료", "작업이 종료되었습니다.")
