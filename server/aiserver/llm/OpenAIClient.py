from openai import OpenAI
from decouple import config
import json


api_key = config("OPENAI_API_KEY")


class OpenAIClient:

    def __init__(self):
        self.client = OpenAI(api_key=api_key)

    def get_quiz(self, message, schema):
        """
        GPT API 를 통해 퀴즈 생성. 퀴즈 옵션에 따른 프롬프트 적용 필요.
        JSON 형태로 응답 받음. 퀴즈 옵션에 따른 후처리 필요.
        :param message: GPT API 호출 프롬프트
        :param schema: 반환 받을 JSON schema
        :return: JSON 포맷의 퀴즈
        """
        try:
            print("Receiving response from GPT...")
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=message,
                tools=schema,
                top_p=0.95
            )

            tool_calls = response.choices[0].message.tool_calls
            quiz = []
            for i in range(len(tool_calls)):
                t = json.loads(tool_calls[i].function.arguments)
                quiz.append(t)
                print(t)
                print("QUIZ GENERATE!! >> No. ", i)
            print("퀴즈 생성 완료")
            return quiz
        except Exception as e:
            print(e)
            return e

    def get_summary(self, message, schema):
        """
        GPT API 를 통해 요약본 생성. Markdown으로 작성된 요약본 생성
        :return: 마크다운 포맷의 요약본 포함 JSON
        """
        print("Receiving response from GPT...")
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=message,
                tools=schema,
                tool_choice={"type": "function", "function": {"name": "get_summary"}}
            )
            tool_calls = response.choices[0].message.tool_calls
            raw_summary = json.loads(tool_calls[0].function.arguments)["summary"]

            print("요약 생성 완료")
            return raw_summary

        except Exception as e:
            print(str(e))
            return e

    def get_kc(self, message, schema):
        print("Receiving response from GPT...")
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=message,
                tools=schema,
            )

            tool_calls = response.choices[0].message.tool_calls

            print("KC 분류 완료")
            return tool_calls

        except Exception as e:
            print(str(e))
            return e
