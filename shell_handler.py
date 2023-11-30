import subprocess
from datetime import datetime

from model_handler import get_chat_completion
from prompt_loader import get_system_prompt

DEFAULT_TIMEOUT = 60


class RestrictedShellHandler:
    def __init__(self, model: str = "gpt-4", timeout: int = DEFAULT_TIMEOUT):
        self.session_history = []
        self.prompt_turns = [{"role": "system", "content": get_system_prompt()}]
        self.timeout = timeout
        self.is_live = True
        self.model = model

    def _log_history(self, msg: str):
        print(msg)
        self.session_history.append(msg)

    def parse_user_input_from_stdin(self) -> str:
        print(">")
        user_input = input()
        self._log_history(user_input)
        return user_input

    def print_assistant_response_to_stdout(self, response: str):
        msg = "assistant: " + response
        self._log_history(msg)

        msg = "(press enter to run command)>"
        self._log_history(msg)

    def start_subprocess_with_command(self, command: str):
        if self.is_live:
            self._log_history(f"user confirmed, executing command: {command}")

            if command != "":
                response = subprocess.run(
                    command, shell=True, timeout=self.timeout, capture_output=True
                )
            else:
                self._log_history("invalid command")
        else:
            response = None
            print(f"Shell is not live, not executing command: {command}")

        return response

    def is_user_confirmation(self, user_input: str) -> bool:
        # check whether user confirmed with enter
        confirmed = user_input == ""
        self._log_history("user: " + user_input)
        return confirmed

    def is_user_abort(self, user_input: str) -> bool:
        # check whether user aborted with ctrl+c
        aborted = user_input == "\x03" or user_input.lower() == "abort"
        self._log_history("user: " + user_input)
        return aborted

    def abort_shell(self):
        self.is_live = False
        self._log_history("Aborting shell")
        # TODO: stop currently running subprocess

        self._save_session_history_to_file()

    def _save_session_history_to_file(self):
        # get current time in format: 23-11-30_19-58
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%y_%H-%M")

        with open(dt_string + "_session_history.txt", "w") as f:
            for entry in self.session_history:
                f.write(entry + "\n")

    def _parse_command_from_history(self) -> str:
        # parse command from history
        command = ""
        # get last entry in history that is not a system prompt and contains <bash> tags
        for entry in reversed(self.session_history):
            if "<bash>" in entry and "system" not in entry:
                command = entry.split("<bash>")[1].split("</bash>")[0].strip()
                break

        return command

    def _call_model(self, user_input: str) -> str:
        if self.is_live:
            print("assistant: ...")
            self.prompt_turns.append({"role": "user", "content": user_input})
            chat_completion = get_chat_completion(self.model, self.prompt_turns)
            return chat_completion["message"]["content"]

    def print_subprocess_response(self, response):
        if response is not None:
            if response.stderr:
                self._log_history(response.stderr.decode("utf-8"))
            else:
                self._log_history(response.stdout.decode("utf-8"))

    def run(self):

        self._log_history("system: {}".format(self.prompt_turns[0]["content"]))

        while self.is_live:
            user_input = self.parse_user_input_from_stdin()

            if self.is_user_abort(user_input):
                self.abort_shell()
                break

            elif self.is_user_confirmation(user_input):
                # parse command from history
                command = self._parse_command_from_history()

                # execute command
                response = self.start_subprocess_with_command(command)
                if response is not None:
                    self.print_subprocess_response(response)
            else:
                # call model
                response = self._call_model(user_input)
                self.print_assistant_response_to_stdout(response)
