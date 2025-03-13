from datetime import datetime
import google.generativeai as ggenai
from pprint import pprint
from google.ai.generativelanguage_v1beta.types import content
import asyncio

import json
import os
from . import main_functions
from django.conf import settings

class DRAssistantAI:
    def __init__(self):
        
        with open(self.get_file_path("main_functions.json"), 'r') as file:
            functions_dict = json.load(file)

        with open(self.get_file_path("static_data.json"), 'r') as file:
            static_data_dict = json.load(file)

        self.functions_declar_json = functions_dict['main_functions']
        self.static_data_json = static_data_dict['static_data']

        self.model_id="gemini-2.0-flash"
        self.reply_model, self.chat_session = self.setup_reply_model()
        ggenai.configure(api_key=settings.GOOGLE_API_KEY)

        self.saved_memories = {}
        self.temp_memory = ""
        self.error_messages = []
        self.function_called = []

        today_date = self.get_today_date()
        self.saved_memories["today date in dd-mm-yyyy format"] = today_date

    def get_file_path(self, filename):
        file_path = os.path.join(settings.BASE_DIR, 'data_retriever_ai', 'json_file', filename)
        return file_path

    def get_today_date(self):
        today = datetime.today()
        date_string = today.strftime("%d-%m-%Y")
        return date_string

    def get_all_variables_paragraph(self):
        filter_properties = self.functions_declar_json['get_bookings_count']['object']['properties']
        variable_paragraph = ""

        for func_name in self.functions_declar_json:
            filter_properties = self.functions_declar_json[func_name]['object']['properties']

            if variable_paragraph != "":
                    variable_paragraph += "\n"
            variable_paragraph += f"{func_name} filter variables:"

            for key, value in filter_properties.items():
                variable_paragraph += f"\n{key}({value['type']}): {value['description']}"

        return variable_paragraph

    def get_saved_memories_paragraph(self):
        saved_memories_paragraph = ""
        for saved_data_key, saved_data_value in self.saved_memories.items():
            if saved_memories_paragraph != "":
                saved_memories_paragraph += "\n"

            saved_memories_paragraph += f"{saved_data_key}: {saved_data_value}"

        return saved_memories_paragraph
    
    def get_function_called_paragraph(self):
        function_called_paragraph = ""
        for function_called in self.function_called:
            if function_called_paragraph != "":
                function_called_paragraph += "\n"

            function_called_paragraph += f"{function_called}"

        return function_called_paragraph
    
    def get_error_messages_paragraph(self):
        error_messages_paragraph = ""
        for error_message in self.error_messages:
            if error_messages_paragraph != "":
                error_messages_paragraph += "\n"

            error_messages_paragraph += f"{error_message}"

        return error_messages_paragraph

    def add_to_temp_memory(self, text):
        if self.temp_memory != "":
            self.temp_memory += "\n"
        self.temp_memory += str(text)
    
    async def extract_static_data(self, question):
        static_data_paragraph = self.get_static_data_paragraph()

        system_instruction=f"You are an AI that lists all data mentioned in the user's question.\nYou have to find data only under these titles:\nLocations, Client Statuses\n\nIn the database, we have\n{static_data_paragraph}\n\nNow chop down the question and list all the found data with keywords in the question. You need to include all the related data for each datum.  If the question mentions data that goes under the titles but not found in the database, you include an error message for each not found data."

        # Create the model
        generation_config = {
        "temperature": 1,
        "top_p": 0,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type = content.Type.OBJECT,
            enum = [],
            required = ["data_in_natural_language"],
            properties = {
            "data_in_natural_language": content.Schema(
                type = content.Type.OBJECT,
                enum = [],
                required = ["found_data", "error_messages"],
                properties = {
                "found_data": content.Schema(
                    type = content.Type.ARRAY,
                    items = content.Schema(
                    type = content.Type.STRING,
                    ),
                ),
                "error_messages": content.Schema(
                    type = content.Type.ARRAY,
                    items = content.Schema(
                    type = content.Type.STRING,
                    ),
                ),
                },
            ),
            },
        ),
        "response_mime_type": "application/json",
        }

        model = ggenai.GenerativeModel(
        model_name=self.model_id,
        generation_config=generation_config,
        system_instruction=system_instruction
        )

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(question)

        given_static_data = json.loads(response.text)['data_in_natural_language']
        found_data = given_static_data['found_data']
        error_messages = given_static_data['error_messages']

        for error_message in error_messages:
            self.error_messages.append(error_message)

        for found_datum in found_data:
            self.add_to_temp_memory(found_datum)

    async def extract_date_data(self, question):
        # Create the model
        generation_config = {
        "temperature": 1,
        "top_p": 0,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type = content.Type.OBJECT,
            enum = [],
            required = ["date_data"],
            properties = {
            "date_data": content.Schema(
                type = content.Type.ARRAY,
                items = content.Schema(
                type = content.Type.OBJECT,
                enum = [],
                required = ["date_data_title", "date_data_value"],
                properties = {
                    "date_data_title": content.Schema(
                    type = content.Type.STRING,
                    ),
                    "date_data_value": content.Schema(
                    type = content.Type.STRING,
                    ),
                },
                ),
            ),
            },
        ),
        "response_mime_type": "application/json",
        }

        model = ggenai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config,
            system_instruction=f"You are a date processor AI that extract all related date data based on the keywords of the user's question.\nIf the question includes date range like ( this|that|next|previous|coming|last, day|week|month|year ), you have to return both start date and end date.\n\nToday date in dd-mm-yyyy: {self.get_today_date()}\n\nProcess based on the given today date. If the question doesn't include keywords related with date, return empty list\nAlways give date value ONLY in this format: dd-mm-yyyy\nAlways give response like this: <date data title>: <date data value>\nPlease describe the date data title fully, for example: 'Start Date of the previous month'",
            )
        
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(question)
        date_data = json.loads(response.text)['date_data']

        def check_errors(date_data):
            errors = ""
            for date in date_data:
                result = main_functions.date_to_code(date['date_data_value'])
                if type(result) == str:
                    errors += f"{date['date_data_title']}: {date['date_data_value']} ({result})\n"

            if errors != "":
                errors += "Please process the data value again and return the response with all date data!"
            return errors

        errors = check_errors(date_data)
        while errors != "":
            response = chat_session.send_message(errors)
            date_data = json.loads(response.text)['date_data']
            errors = check_errors(date_data)

        for date in date_data:
            self.add_to_temp_memory(f"{date['date_data_title']}: {date['date_data_value']}")

    def prepare_necessary_filters(self, question):
        filter_variables_paragraph = self.get_all_variables_paragraph()

        system_instruction=f"You are an AI from booking management system.\nYou task is to list the necessary filter variable names from given filter varibles along with its value.\nAll the required values will be given below.\nYou must follow the data type of filter variables for their value.\nFor date data, you MUST use the exact date given below.\n\nQuestion: {question}\n\nFilter Variables:\n\n{filter_variables_paragraph}\n\nGiven Values:\n{self.temp_memory}"

        # Create the model
        generation_config = {
        "temperature": 1,
        "top_p": 0,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_schema": content.Schema(
            type = content.Type.OBJECT,
            enum = [],
            required = ["required_filter_variables", "not_relevant_question"],
            properties = {
            "required_filter_variables": content.Schema(
                type = content.Type.ARRAY,
                items = content.Schema(
                type = content.Type.OBJECT,
                enum = [],
                required = ["filter_variable_name", "value"],
                properties = {
                    "filter_variable_name": content.Schema(
                    type = content.Type.STRING,
                    ),
                    "value": content.Schema(
                    type = content.Type.STRING,
                    ),
                },
                ),
            ),
            "not_relevant_question": content.Schema(
                type = content.Type.BOOLEAN,
            ),
            },
        ),
        "response_mime_type": "application/json",
        }

        model = ggenai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=generation_config,
            system_instruction=system_instruction
            )
        
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(question)

        response_json = json.loads(response.text)

        return response_json
    
    def get_static_data_paragraph(self):
        static_data_paragraph = ""
        for static_function_name in self.static_data_json:

            if static_data_paragraph != "":
                static_data_paragraph += "\n"

            static_data_paragraph += f"{static_function_name}:\n"
            for data in self.static_data_json[static_function_name]['data']:
                static_data_paragraph += f"{data}\n"

        return static_data_paragraph
    
    def update_reply_model_sys_instr(self, additional_sys_instr=""):
        system_instruction = f"Your name is 'Iggy', an assistant AI in booking management system that replies to the user formally.\nThe result might have been saved in the saved memories.\nIf you don't find the appropriate result for the user's question in the saved memories, you MUST call 'process_answer' function to get the result.\nSo you check the saved memories to reply to the user.\nSometime, there might be errors when finding the result of what user asked, include those errors when replying to the user.\n\nSaved Memories:\n{self.get_saved_memories_paragraph()}\n\nFunction Called Result:\n{self.get_function_called_paragraph()}\n\nError Messages:\n{self.get_error_messages_paragraph()}\n\nTemporary Memories:\n{self.temp_memory}\n\n{additional_sys_instr}"

        for part in self.reply_model._system_instruction.parts:
            self.reply_model._system_instruction.parts.remove(part)

        part.text = system_instruction
        self.reply_model._system_instruction.parts.append(part)
    
    def setup_reply_model(self):
        # Create the model
        generation_config = {
        "temperature": 1,
        "top_p": 0,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
        }

        model = ggenai.GenerativeModel(
        model_name="gemini-2.0-flash",
        generation_config=generation_config,
        system_instruction="A",
        tools = [
            ggenai.protos.Tool(
            function_declarations = [
                ggenai.protos.FunctionDeclaration(
                name = "process_answer",
                description = "process answers based on the user's question.",
                ),
            ],
            ),
        ],
        tool_config={'function_calling_config':'AUTO'},
        )

        chat_session = model.start_chat(history=[])

        return model, chat_session

    def find_answer(self, question):
        async def run_at_the_same_time():
            task1 = asyncio.create_task(self.extract_date_data(question))
            task2 = asyncio.create_task(self.extract_static_data(question))
            # Await each task individually; they run concurrently.
            await task1
            await task2

        asyncio.run(run_at_the_same_time())

        filters_to_apply = self.prepare_necessary_filters(question)

        if filters_to_apply['not_relevant_question'] == False:
            number_of_bookings = main_functions.get_bookings_count(
                function_declar_json=self.functions_declar_json['get_bookings_count'],
                necessary_parameters=filters_to_apply['required_filter_variables']
            )

            filter_text = ""
            for var in filters_to_apply['required_filter_variables']:
                filter_text += f"{var['filter_variable_name']}={var['value']}, "

            self.function_called.append(f"get_bookings_count({filter_text}): {number_of_bookings}")
    
    def send_message(self, question):
        self.update_reply_model_sys_instr()
        response = self.chat_session.send_message(question)

        if response.candidates[0].content.parts[0].function_call:
            self.find_answer(question)
            self.update_reply_model_sys_instr()

            response = self.chat_session.send_message(f"__SYSTEM__\nThe results for question '{question}' have been processed.\nYou can find in function called or errors.\nIf you don't find the appropriate result now, you MUST just return the normal reply to user.\nBut if you find answers, you MUST return the normal reply to user.")

            self.saved_memories[question] = response.text

        #print(response.text)

        print("saved memories",self.saved_memories)
        print("temp memory",self.temp_memory)
        print("function called",self.function_called)
        print("error messages",self.error_messages)

        self.temp_memory = ""
        self.function_called = []
        self.error_messages = []

        print(self.chat_session)

        return response.text