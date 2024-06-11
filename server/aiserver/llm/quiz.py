from .OpenAIClient import OpenAIClient
from .utils import *
import json
import time
from .ComponentController import ComponentController

openai_client = OpenAIClient()
kc_df = KCList().df
component_controller = ComponentController()


class QuizGenerator:
    def __init__(self):
        self.client = openai_client
        self.kc_df = kc_df
        self.controller = component_controller


    def txt_format_for_quiz(self, txt, page_kc_id, start_page, end_page):
        """
        pdf text를 퀴즈 생성기의 입력 포맷으로 변환하여 리턴

        :param txt: "<0>~~~<1>~~~" 포맷의 pdf text
        :param page_kc_id: KC 분류기 결과 - 페이지별 KC ID
        :return: 퀴즈 생성기 입력 포맷 문자열 (ex. <KC1>: ~~~ <KC2>:~~~)
        """
        j = {}
        pages = list(page_kc_id.keys())
        end_page += 1  
        selected_pages = pages[start_page:end_page]
        for page_number in selected_pages:
            kc_id = page_kc_id[page_number]
            if kc_id in j:
                j[kc_id] += " " + get_page_txt(txt, page_number)
            else:
                j[kc_id] = get_page_txt(txt, page_number)

        input_txt = ""
        kc_id_list = list(j.keys())

        for kc_id in kc_id_list:
            input_txt += f"<{kc_id}> {self.kc_df.loc[kc_id]['kc']}: "
            input_txt += j[kc_id] + "\n"
        print("input_txt", input_txt)

        return input_txt

    def get_quiz(self, params):

        print(type(params["pageKcId"]))
        page_kc_id = json.loads(params["pageKcId"])

        req = {"pdftxt": self.txt_format_for_quiz(params["pdfText"], page_kc_id, params["startPage"], params["endPage"]),
               "rank": str(params["rank"]),
               "problem_num": str(params["problemNum"]),
               "subject": params["subject"],
               "dkt": params.get('dkt')
               }

        problem_list = []
        retries = 3 # 퀴즈 생성 에러시 최대 재시도 횟수

        # 퀴즈 종류에 따라 퀴즈 생성
        if params["quizType"] == "MULTIPLE_CHOICE":
            print("Quiz type: MULTIPLE_CHOICE")
            for attempt in range(retries):
                try:
                    problem_list = self.get_choice_quiz(req)
                    break  # 함수가 성공적으로 실행되면 종료합니다.
                except Exception as e:
                    print(f"Error occurred: {e}")
                    if attempt < retries - 1:
                        print(f"Retrying... ({attempt + 1}/{retries})")
                    else:
                        print("All retries failed.")
                        raise  # 모든 재시도가 실패하면 예외를 다시 발생시킵니다.

        elif params["quizType"] == "OX":
            print("Quiz type: OX Quiz")
            for attempt in range(retries):
                try:
                    problem_list = self.get_ox_quiz(req)
                    break  # 함수가 성공적으로 실행되면 종료합니다.
                except Exception as e:
                    print(f"Error occurred: {e}")
                    if attempt < retries - 1:
                        print(f"Retrying... ({attempt + 1}/{retries})")
                    else:
                        print("All retries failed.")
                        raise  # 모든 재시도가 실패하면 예외를 다시 발생시킵니다.

        elif params["quizType"] == "BLANK":
            print("Quiz type: BLANK")
            for attempt in range(retries):
                try:
                    problem_list = self.get_blank_quiz(req)
                    break  # 함수가 성공적으로 실행되면 종료합니다.
                except Exception as e:
                    print(f"Error occurred: {e}")
                    if attempt < retries - 1:
                        print(f"Retrying... ({attempt + 1}/{retries})")
                    else:
                        print("All retries failed.")
                        raise  # 모든 재시도가 실패하면 예외를 다시 발생시킵니다.

        gen_quiz = {
            "quizId": params["quizId"],
            "quizType": params["quizType"],
            "problemList": problem_list,
        }

        # quiz id, type  추가 , jsonify
        return gen_quiz

    def get_choice_quiz(self, params):
        try:
            msg = self.controller.choice_quiz_create_msg(params)
            raw_quiz = self.client.get_quiz(msg, self.controller.get_schema_for_choice())

            choice_problem_list = []
            for i in range(len(raw_quiz)):
                prob = {
                    "problemNo": i + 1,
                    "kcId": raw_quiz[i]["kc_id"],
                    "question": raw_quiz[i]["question"],
                    "content": None,
                    "options": {
                        "option_a": raw_quiz[i]["options"]["option_a"],
                        "option_b": raw_quiz[i]["options"]["option_b"],
                        "option_c": raw_quiz[i]["options"]["option_c"],
                        "option_d": raw_quiz[i]["options"]["option_d"],
                    },
                    "answer": raw_quiz[i]["answer"],
                    "blanks": {
                        "blank_1": None,
                        "blank_2": None,
                        "blank_3": None,
                        "blank_4": None,
                    },
                    "explanation": raw_quiz[i]["explanation"],
                }
                choice_problem_list.append(prob)

            self.print_choice_prob(raw_quiz)
            return choice_problem_list

        except Exception as e:
            print(str(e))
            return str(e)

    def get_ox_quiz(self, params):
        msg = self.controller.ox_quiz_create_msg(params)
        raw_quiz = self.client.get_quiz(msg, self.controller.get_schema_for_ox())
        b = lambda x: "o" if x == True else "x"

        # postprocessing
        ox_problem_list = []
        for i in range(len(raw_quiz)):
            prob = {
                "problemNo": i + 1,
                "kcId": raw_quiz[i]["kc_id"],
                "question": raw_quiz[i]["question"],
                "content": None,
                "options": {
                    "option_a": None,
                    "option_b": None,
                    "option_c": None,
                    "option_d": None,
                },
                "answer": b(raw_quiz[i]["answer"]),
                "blanks": {
                    "blank_1": None,
                    "blank_2": None,
                    "blank_3": None,
                    "blank_4": None,
                },
                "explanation": raw_quiz[i]["explanation"],
            }
            ox_problem_list.append(prob)

        self.print_ox_prob(raw_quiz)
        return ox_problem_list


    def get_blank_quiz(self, params):
        msg = self.controller.blank_quiz_create_msg(params)
        raw_quiz = self.client.get_quiz(msg, self.controller.get_schema_for_blank())

        # postprocessing
        blank_problem_list = []
        for i in range(len(raw_quiz)):
            if raw_quiz[i]["is_markdown"] == True:
                content = "<markdown>" + raw_quiz[i]["content"]
                print(f"{i}번 문제는 코드 문제.")
            else:
                content = raw_quiz[i]["content"]

            prob = {
                "problemNo": i + 1,
                "kcId": raw_quiz[i]["kc_id"],
                "question": raw_quiz[i]["question"],
                "content": content,
                "options": {
                    "option_a": None,
                    "option_b": None,
                    "option_c": None,
                    "option_d": None,
                },
                "answer": None,
                "blanks": {
                    "blank_1": raw_quiz[i]["blanks"]["blank_1"],
                    "blank_2": raw_quiz[i]["blanks"]["blank_2"],
                    "blank_3": raw_quiz[i]["blanks"]["blank_3"],
                    "blank_4": raw_quiz[i]["blanks"]["blank_4"],
                },
                "explanation": raw_quiz[i]["explanation"],
            }
            blank_problem_list.append(prob)

        self.print_blank_prob(raw_quiz)
        return blank_problem_list

    def print_choice_prob(self, quiz):
        for i in range(len(quiz)):
            print("+----------------------------------------+")
            print("+               문제 ", str(i), "                 +")
            print("+----------------------------------------+")
            print("KC ID: ", quiz[i]['kc_id'])
            print("KC by GPT:  ", quiz[i]['kc'])
            print("True KC:  ", self.kc_df.loc[quiz[i]['kc_id']]['kc'])
            print()
            print(quiz[i]['question'])
            print()
            print("A. ", quiz[i]['options']['option_a'])
            print("B. ", quiz[i]['options']['option_b'])
            print("C. ", quiz[i]['options']['option_c'])
            print("D. ", quiz[i]['options']['option_d'])
            print()
            print("Answer:  ", quiz[i]['answer'])
            print("Explanation:  ", quiz[i]['explanation'])
            print()

    def print_ox_prob(self, quiz):
        for i in range(len(quiz)):
            print("+----------------------------------------+")
            print("|                문제 ", str(i), "                 |")
            print("+----------------------------------------+")
            print("KC ID: ", quiz[i]['kc_id'])
            print("KC by GPT:  ", quiz[i]['kc'])
            print("True KC:  ", self.kc_df.loc[quiz[i]['kc_id']]['kc'])
            print()
            print(quiz[i]['question'])
            print()
            if quiz[i]['answer']:
                print("    +=========+            +---------+")
                print("    | ✔️  O    |            |    X    |")
                print("    +=========+            +---------+")
            else:
                print("    +---------+            +=========+")
                print("    |    O    |            | ✔️  X    |")
                print("    +---------+            +=========+")
            print()
            print("Answer:  ", quiz[i]['answer'])
            print("Explanation:  ", quiz[i]['explanation'])
            print()

    import textwrap
    def print_blank_prob(self,  quiz):
        for i in range(len(quiz)):
            print("+----------------------------------------+")
            print("+               문제 ", str(i), "                  +")
            print("+----------------------------------------+")
            print("KC ID: ", quiz[i]['kc_id'])
            print("KC by GPT:  ", quiz[i]['kc'])
            print("True KC:  ", self.kc_df.loc[quiz[i]['kc_id']]['kc'])
            print("MD? ", quiz[i]['is_markdown'])
            print()
            print(quiz[i]['question'])
            print()
            print(quiz[i]['content'])
            print()

            for j in range(4):
                b = "blank_" + str(j + 1)
                if quiz[i]['blanks'][b] != None:
                    print("(", str(j + 1), "):    ", quiz[i]['blanks'][b])

            print("Explanation:  ",quiz[i]['explanation'])
            print()

    def retry_function(self, func, retries=3, delay=1):
        for attempt in range(retries):
            try:
                func()
                return  # 함수가 성공적으로 실행되면 종료합니다.
            except Exception as e:
                print(f"Error occurred: {e}")
                if attempt < retries - 1:
                    print(f"Retrying... ({attempt + 1}/{retries})")
                    time.sleep(delay)
                else:
                    print("All retries failed.")
                    raise  # 모든 재시도가 실패하면 예외를 다시 발생시킵니다.