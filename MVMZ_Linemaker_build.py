import os
import re
import sys
import json
import traceback

class MVMZLineMaker:

#========초기화========#

    def __init__(self):
        self.CURRENT_VERSION = "3.0.3"
        #self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.current_dir = os.path.dirname(sys.executable)
        self.data_folder_path = os.path.join(self.current_dir, 'data')
        self.system_file_path = os.path.join(self.current_dir, 'data', 'system.json')
        self.js_folder_path = os.path.join(self.current_dir, 'js', 'plugins.js')

        # 진행 상황 관리를 위한 카운터 추가
        self.total_files = 0
        self.processed_files = 0

        # 처리 대상 파일 패턴 정의
        self.file_patterns = [
            re.compile(r'Actors(_\d+)?\.json$'),
            re.compile(r'Armors(_\d+)?\.json$'),
            re.compile(r'Classes(_\d+)?\.json$'),
            re.compile(r'CommonEvents(_\d+)?\.json$'),
            re.compile(r'Enemies(_\d+)?\.json$'),
            re.compile(r'Items(_\d+)?\.json$'),
            re.compile(r'MapInfos(_\d+)?\.json$'),
            re.compile(r'Skills(_\d+)?\.json$'),
            re.compile(r'States(_\d+)?\.json$'),
            re.compile(r'System(_\d+)?\.json$'),
            re.compile(r'Troops(_\d+)?\.json$'),
            re.compile(r'Weapons(_\d+)?\.json$'),
        ]

        # Map 파일 패턴 (Map001.json, Map313_2.json 등)
        self.map_pattern = re.compile(r'Map\d{3}(_\d+)?\.json$')

        print(f"MVMZLineMaker 시작 (버전: {self.CURRENT_VERSION})")

        print("=" * 50)

        if os.path.isdir(self.data_folder_path):
            print(f"데이터 폴더 확인 완료")
        else:
            print(f"데이터 폴더를 찾을 수 없음")
        if os.path.isfile(self.system_file_path):
            print(f"시스템 파일 확인 완료")
        else:
            print(f"시스템 파일을 찾을 수 없음")
        if os.path.isfile(self.js_folder_path):
            print(f"플러그인    확인 완료")
        else:
            print(f"플러그인 파일을 찾을 수 없음")

        print("=" * 50)

        #print(f"데이터 폴더 경로: {self.data_folder_path}")
        #print(f"시스템 파일 경로: {self.system_file_path}")
        #print(f"플러그인 파일 경로: {self.js_folder_path}")

#========초기화========#
#
#========파일처리========#

    def is_target_file(self, filename):
        """처리 대상 파일인지 확인"""
        # Map 패턴 검사
        if self.map_pattern.match(filename):
            return True

        # 기타 파일 패턴 검사
        for pattern in self.file_patterns:
            if pattern.match(filename):
                return True

        return False

    def process_files(self):

        self.total_files = 0
        self.processed_files = 0
        error_files = 0
        failed_files = []

        try:
            # 데이터 폴더 내 대상 파일 필터링
            if not os.path.isdir(self.data_folder_path):
                print(f"데이터 폴더를 찾을 수 없음: {self.data_folder_path}")
                return False

            json_files = [f for f in os.listdir(self.data_folder_path)
                        if f.endswith('.json') and self.is_target_file(f)]

            # plugins.js 포함하여 총 파일 수 계산
            self.total_files = len(json_files) + (1 if os.path.isfile(self.js_folder_path) else 0)

            if self.total_files == 0:
                print("처리할 파일이 없습니다.")
                return False

            # 데이터 폴더의 JSON 파일 처리
            for filename in json_files:
                try:
                    file_path = os.path.join(self.data_folder_path, filename)
                    self.modify_json_file(file_path)
                    self._increment_progress()
                    #print(f"파일 처리 완료: {filename}")
                except Exception as e:
                    error_files += 1
                    failed_files.append(f"{filename}: {str(e)}")

            # plugins.js 처리
            if os.path.isfile(self.js_folder_path):
                try:
                    self.modify_js_file(self.js_folder_path)
                    self._increment_progress()
                    print("플러그인 처리 완료")
                except Exception as e:
                    error_files += 1
                    failed_files.append(f"plugins.js: {str(e)}")
                    print(f"플러그인 파일 처리 실패: {str(e)}")

            # 성공 여부 판단
            success = (self.processed_files == self.total_files)

            print("=" * 50)
            print(f"처리 완료 - 총 파일: {self.total_files}, "
                            f"성공: {self.processed_files}, 실패: {error_files}")
            print("=" * 50)
            # 실패한 파일이 있으면 목록 출력
            if error_files > 0:
                print("\n실패한 파일 목록:")
                for fail_info in failed_files:
                    print(f"- {fail_info}")

            return success

        except Exception as e:
            print(f"Line Maker 처리 중 오류 발생: {str(e)}")
            return False

    def modify_json_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                content = file.read()

            # 새로운 포맷 함수 적용
            modified_content = self.format_json_content(content)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)

        except Exception as e:
            raise

    def format_json_content(self, content):
        try:
            # JSON 파싱
            data = json.loads(content)
            formatted_content = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

            # 포맷팅 규칙 정의
            format_rules = [
                # 기본 구조 처리
                (r'null,\{"id"', r'null,\n{"id"'),

                # 공통 패턴 처리
                (r'("switchId":\d+,"trigger":\d+)\},(\{"id":)', r'\1},\n\2'),
                (r'("type":\d+,"variance":\d+)\},(\{"id":)', r'\1},\n\2'),
                (r'\],"learnings":', r'],\n"learnings":'),
                (r'\],"hitType":', r'],\n"hitType":'),
                (r'\],"iconIndex":', r'],\n"iconIndex":'),
                (r'\],"gold":', r'],\n"gold":'),

                # 개체별 처리
                # Actors
                (r'"note":"([^"]*)","profile":"([^"]*)"},{"id":', r'"note":"\1","profile":"\2"},\n{"id":'),
                # Classes
                (r'(\d+\]\]\}),\{"id"', r'\1,\n{"id"'),
                # Items
                (r'("successRate":\d+,"tpGain":\d+)\},(\{"id":)', r'\1},\n\2'),
                (r'("type":\d+,"variance":\d+)\}\},(\{"id":)', r'\1}},\n\2'),
                (r'("type":"","variance":"")\}\},(\{"id":)', r'\1}},\n\2'),
                # Skills
                (r'("tpCost":\d+,"tpGain":\d+,"messageType":\d+)\},(\{"id":)', r'\1},\n\2'),
                (r'("tpCost":\d+,"tpGain":\d+)\},(\{"id":)', r'\1},\n\2'),
                #"type":1,"variance":0},"message1":""},
                # Armor
                (r'("price":\d+)\},(\{"id":)', r'\1},\n\2'),
                # Weapons
                (r'("price":\d+,"wtypeId":\d+)\},(\{"id":)', r'\1},\n\2'),
                # Enemies
                (r'("params":\[\d+(?:,\d+)*\])\},(\{"id":)', r'\1},\n\2'),
                # Troops
                (r'("span":\d+)\}\]\},(\{"id":)', r'\1}]},\n\2'),
                # States
                (r'("messageType":\d+)\},(\{"id":)', r'\1},\n\2'),
                (r'("traits":\[[^\]\[{}]*(?:\{[^{}]*\}[^\]\[{}]*)*\](?:,"[^"]*":[^{}\[\]]*)*)\},(\{"id":)', r'\1},\n\2'),
                (r'("value":-?\d*\.?\d*)\}\]\},(\{"id":)', r'\1}]},\n\2'),
                # MapInfos
                (r'("scrollX":-?\d*\.?\d*,"scrollY":-?\d*\.?\d*,"quick":(true|false))\},(\{"id":)', r'\1},\n\3'),
                (r'("scrollX":-?\d*\.?\d*,"scrollY":-?\d*\.?\d*)\},(\{"id":)', r'\1},\n\2'),
                (r'("scrollX":-?\d*\.?\d*,"scrollY":-?\d*\.?\d*)\},(null)', r'\1},\n\2'),
                # Maps 처리
                (r'("tilesetId":\d+,"width":\d+,)("data":)', r'\1\n\2'),
                (r'("x":\d+,"y":\d+)\},(\{"id":)', r'\1},\n\2'),

                # list 배열 시작 부분
                (r'("list":\[)(?!\n)', r'\1\n'),

                # code 205 특별 처리
                (r'([^\n])(\{"code":205,)', r'\1\n\2'),
            ]

            # 모든 규칙 적용
            result = formatted_content
            for pattern, replacement in format_rules:
                result = re.sub(pattern, replacement, result)

            # code 객체 처리 - 복잡한 패턴은 별도 함수로
            result = self._process_code_objects(result)

            # 중복 줄바꿈 정리
            result = re.sub(r'\n\s*\n', '\n', result)

            # System 처리
            system_rules = [
                (r'("startX":\d+,"startY":\d+,)("switches":)', r'\1\n\n\2'),
                (r'("\],)("terms":)', r'\1\n\n\2'),
                (r'\},("variables":)', r'},\n\n\1'),
                (r'("\],)("versionId":)', r'\1\n\n\2'),
            ]

            # System 규칙 적용
            for pattern, replacement in system_rules:
                result = re.sub(pattern, replacement, result)

            return result

        except Exception as e:
            raise

    def _process_code_objects(self, text):
        """code 객체 관련 포맷팅을 처리하는 함수"""
        def replace_code_objects(match):
            full_match = match.group(0)

            # moveRoute나 list 배열 내부 제외
            if '"moveRoute":{"list":[' in full_match:
                return full_match

            # code 객체 줄바꿈 처리
            parts = full_match.split('{"code":')
            processed = []
            for i, part in enumerate(parts):
                if i == 0:
                    processed.append(part.rstrip())
                else:
                    processed.append('\n{"code":' + part)

            return ''.join(processed)

        # 연속된 code 객체들을 찾아서 처리
        pattern = r'((?:{"code":.*?}(?:,\s*)?)+)'
        return re.sub(pattern, replace_code_objects, text)

    def modify_js_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as file:
                content = file.read()

            # 간단 포맷팅 예외 처리
            def apply_visumz_formatting(content):
                """VisuMZ 플러그인 포맷팅 처리"""
                print("간단한 포맷팅 적용")
                patterns_and_replacements = [
                    ('","', '",\n"'),
                    ('},{', '},\n{'),
                    ('},\n{"name', '\n},\n\n{"name'),
                    (',"description"', ',\n"description"'),
                    ('"parameters":{', '"parameters":{\n'),
                    ('\n\n', '\n')
                ]
                modified_content = content
                for pattern, replacement in patterns_and_replacements:
                    modified_content = re.sub(pattern, replacement, modified_content)

                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(modified_content)

                print("간단 포맷팅 완료")

            # if "VisuMZ" in content:
            #     apply_visumz_formatting(content)
            #     return

            # 더 견고한 plugins 배열 추출 방법
            def extract_plugins_array(content):
                """plugins 배열을 안전하게 추출"""
                pattern = r'(?://[^\n]*\n)*\s*var\s+\$plugins\s*=\s*'
                match = re.search(pattern, content)
                if not match:
                    return None, None, None

                start_pos = match.end()

                # 배열 시작 찾기
                bracket_start = content.find('[', start_pos)
                if bracket_start == -1:
                    return None, None, None

                # 균형 잡힌 괄호로 배열 끝 찾기
                bracket_count = 0
                i = bracket_start
                while i < len(content):
                    if content[i] == '[':
                        bracket_count += 1
                    elif content[i] == ']':
                        bracket_count -= 1
                        if bracket_count == 0:
                            break
                    i += 1

                if bracket_count != 0:
                    return None, None, None

                # 세미콜론까지 포함
                end_pos = content.find(';', i)
                if end_pos == -1:
                    end_pos = i + 1
                else:
                    end_pos += 1

                plugins_str = content[bracket_start:i+1]
                full_start = match.start()

                return plugins_str, full_start, end_pos

            plugins_str, start_pos, end_pos = extract_plugins_array(content)
            if not plugins_str:
                print("plugins 배열을 찾을 수 없습니다. 간단 포맷팅을 적용합니다.")
                apply_visumz_formatting(content)
                return

            # JSON 파싱 시도
            try:
                plugins = json.loads(plugins_str)
            except json.JSONDecodeError as e:
                print(f"JSON 파싱 실패: {e}")
                print("복잡한 구조로 인해 간단 포맷팅을 적용합니다.")
                apply_visumz_formatting(content)
                return

            def format_parameters(params):
                """parameters 객체를 보기 좋게 포맷팅하면서 이스케이프 문자 유지"""
                if not params:  # 빈 객체인 경우
                    return "{}"

                lines = []
                items = list(params.items())
                for i, (key, value) in enumerate(items):
                    # 백슬래시 키 처리 - \AT[n] 패턴 감지 및 처리
                    if key.startswith('\\AT[') and key.endswith(']'):
                        escaped_key = f'"\\\\{key[1:]}"'  # 백슬래시 추가 이스케이프
                    else:
                        escaped_key = json.dumps(key, ensure_ascii=False)

                    if isinstance(value, str):
                        try:
                            # JSON 문자열인지 확인
                            json.loads(value)
                            # JSON 문자열이면 원본 형태 그대로 유지
                            escaped_value = json.dumps(value, ensure_ascii=False)
                            lines.append(f'{escaped_key}:{escaped_value}')
                        except json.JSONDecodeError:
                            # 일반 문자열이면 그냥 처리
                            lines.append(f'{escaped_key}:{json.dumps(value, ensure_ascii=False)}')
                    else:
                        # 일반 값은 JSON 덤프
                        lines.append(f'{escaped_key}:{json.dumps(value, ensure_ascii=False, separators=(",", ":"))}')

                return "{\n" + ",\n".join(lines) + "\n}"

            def format_plugin(plugin):
                """플러그인 객체를 포맷팅"""
                formatted_plugin = {}
                for key, value in plugin.items():
                    if key == 'description':
                        formatted_plugin[key] = ' '.join(line.strip() for line in value.splitlines() if line.strip())
                    else:
                        formatted_plugin[key] = value

                lines = []
                for i, (key, value) in enumerate(formatted_plugin.items()):
                    if key == 'parameters':
                        # parameters는 특별한 포맷팅 적용
                        line = f'"parameters":{format_parameters(value)}'
                    else:
                        line = f'"{key}":{json.dumps(value, ensure_ascii=False)}'

                    if i < len(formatted_plugin) - 1:
                        line += ','
                    lines.append(line)

                return "{" + "\n".join(lines) + "\n}"

            formatted_plugins = []
            for i, plugin in enumerate(plugins):
                plugin_str = format_plugin(plugin)
                if i < len(plugins) - 1:
                    plugin_str += ','
                formatted_plugins.append(plugin_str)

            plugins_formatted = "// Generated by RPG Maker.\n"
            plugins_formatted += "// Do not edit this file directly.\n"
            plugins_formatted += "var $plugins =\n[\n"
            plugins_formatted += "\n".join(formatted_plugins)
            plugins_formatted += "\n];"

            modified_content = content[:start_pos] + plugins_formatted + content[end_pos:]

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(modified_content)

        except Exception as e:
            print(f"파일 처리 중 오류 발생: {file_path}")
            print(traceback.format_exc())
            # 오류 발생 시 간단 처리 방식 적용
            apply_visumz_formatting(content)

#========파일처리========#
#
#========진행상황관리========#

    def _increment_progress(self):
        """진행률 증가 및 보고 - 10% 단위로만 표시"""
        self.processed_files += 1
        if self.total_files > 0:
            current_progress = (self.processed_files / self.total_files) * 100
            current_tenth = int(current_progress / 10)
            previous_tenth = int(((self.processed_files - 1) / self.total_files * 100) / 10)

            if current_tenth != previous_tenth:
                print(f"[줄정리]진행률: {current_tenth * 10}% ({self.processed_files}/{self.total_files})")

#========진행상황관리========#

    def main(self):
        """메인 함수"""
        self.process_files()
        input("\n엔터 키를 누르면 종료됩니다...")

if __name__ == "__main__":
    MVMZLineMaker.main(self=MVMZLineMaker())