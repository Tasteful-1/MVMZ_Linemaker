#########################################################################################
# RPG MAKER MV & MZ Line Maker
# 작성 : tasteful
# json 파일을 깔끔하게 정리해줍니다.
# 이 코드는 타인의 사용을 고려하지 않았습니다.
# 수정 및 개선, 재배포는 자유롭게 하셔도 좋습니다.
#
# V1 : 최초작성 : 24-08-05
# V1 : 특정 문자열을 치환하는 방식으로 라인을 정리합니다.
#    : 동작이 불안정하며 불완전하여 3회에 걸쳐 기능이 반복됩니다.
# V2 : 업데이트 : 24-10-04
# V2 : 여타 추출툴로 수정이 가해진 파일에 대해서도 한번에 정리될 수 있도록 개선하였습니다.
#    : 이제 한번의 수정만으로 누락없는 정리가 가능해졌으며 소요시간이 대폭 단축되었습니다.
#    : 보다 온전한 수정을 위해 base_modifications 를 별도로 분리하였습니다.
#    : 정규식의 추가를 통해 특정 라인에 대한 수정을 제외시키려 하였으나
#    : 굳이 기능을 넣어도 쓸 일이 없겠다는 생각에 중단하였습니다.
#    : MK1 : plugins.js에 대하여 오직 name만을 기준으로 정리합니다.
#    : MK2 : Plugins.js에 대하여 parameters를 기준으로 추가정리합니다.
#V2.1: 업데이트 : 24-10-05
#    : Plugins.js에 대한 추가정리 로직을 변경하였습니다.
#########################################################################################

import os

def modify_file(file_path, modifications, max_passes=10):
    # 파일을 한 번에 읽기
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 문자열 수정
        modified_content = content
        for _ in range(max_passes):
            previous_content = modified_content
            for old_str, new_str in modifications:
                modified_content = modified_content.replace(old_str, new_str)

			# 이전 내용과 현재 내용이 동일하면 중단
            if previous_content == modified_content:
                break

        # 수정된 내용을 한 번에 파일에 다시 쓰기
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        print(f"Modified file: {file_path}")

    except Exception as e:
        print(f"Failed to process file {file_path}: {e}")

# 현재 스크립트의 디렉토리 경로 얻기
current_dir = os.path.dirname(os.path.abspath(__file__))

base_modifications = [
    ('\n', ''),
    ('\t', ''),
    ('" ', '"'),
    (': ', ':'),
]

base_modifications2 = [
    ('\n', ''),
    ('\t', ''),
    ('" ', '"'),
]

# 첫 번째 폴더에 대한 수정
data_folder_path = os.path.join(current_dir, 'data')
data_modifications = [
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
    ('}\n]\n}', '}]}'),
    ('null\n]\n}', 'null]}'),
    ('"events":[\n]\n}', '"events":[]')
]

# 두 번째 폴더에 대한 수정
js_folder_path = os.path.join(current_dir, 'js', 'plugins.js')
js_modifications = [
    ('var $plugins =[{"name"','// Generated by RPG Maker.\n// Do not edit this file directly.\nvar $plugins =\n[\n{"name"'),
    ('// Generated by RPG Maker.// Do not edit this file directly.// Generated by RPG Maker.\n// Do not edit this file directly.','// Generated by RPG Maker.\n// Do not edit this file directly.'),
    ('},{"name', '},\n\n{"name'),
    ('","parameters":', '",\n"parameters":\n'),
    ('","', '",\n"'),
]

# 폴더 내 파일 수정 실행
for folder_path, _, filenames in os.walk(data_folder_path):
    for filename in filenames:
        file_path = os.path.join(folder_path, filename)
        modify_file(file_path, base_modifications+data_modifications)

if os.path.isfile(js_folder_path):
    # 단일 파일일 경우, 바로 수정 함수 호출
    modify_file(js_folder_path, base_modifications2)
    modify_file(js_folder_path, js_modifications)
