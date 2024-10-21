
from openai import OpenAI
import time
import json

class AIAssistant:
    def __init__(self, api_key, assistant_id):
        self.client = OpenAI(api_key=api_key)
        self.asistant_id = assistant_id
        print("Constructed AI Assistant")

    def create_thread(self, messages):
        # print("Creating thread with messages:")
        # print(messages)
        thread = self.client.beta.threads.create(
            messages=[
                messages
            ]
        )
        print(f"Thread created: {thread.id}")
        return thread

    def create_message(self, role, content):
        print("Creating message")
        return {"role": role, "content": content}

    def run_thread(self, thread_id):
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=self.asistant_id)
        return run

    def get_latest_message(self, thread_id):
        message_response = self.client.beta.threads.messages.list(
            thread_id=thread_id)
        messages = message_response.data
        return messages[0]

    def generate_response(self, query, thread_id=None):
        # Check if the query is part of an existing thread
        if thread_id:
            # If it is, update the thread with new message
            message = self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=query
                )
        else:
            # If not, create a new message and thread
            message = self.create_message("user", query)
            thread = self.create_thread(message)
            thread_id = thread.id
        # Create new run
        run = self.run_thread(thread_id)
        while True:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run.id)
            if run.status == "completed":
                break
            print(f"Run status: {run.status}")
            time.sleep(0.5)
        # print(f"{variable_name} generated!")
        latest_message = self.get_latest_message(thread_id)
        return latest_message.content[0].text.value, thread_id

    
    
    # def generate_variable(self, variable_name, data):
    #     """Generates a variable using the AI Assistant.

    #     Args:
    #         variable_name (string): The variable name to be replaced in the .docx template.
    #         data (dict): A dictionary containing the data to be used as a propmt in the AI Assistant.

    #     Returns:
    #         dict: A dictionary containing the variable name and generated response as a key value pair, compatible with the dictionary format for report generator context.
    #     """
    #     message = self.create_message("user", json.dumps(data))
    #     thread = self.create_thread(message)
    #     run = self.run_thread(thread.id)
    #     while True:
    #         run = self.client.beta.threads.runs.retrieve(
    #             thread_id=thread.id, run_id=run.id)
    #         if run.status == "completed":
    #             break
    #         print(f"Run status: {run.status}")
    #         time.sleep(0.5)
    #     # print(f"{variable_name} generated!")
    #     latest_message = self.get_latest_message(thread.id)
    #     return {variable_name: latest_message.content[0].text.value}