#!/usr/bin/env python3
from flask import Flask
from ask_sdk_core.skill_builder import SkillBuilder
from flask_ask_sdk.skill_adapter import SkillAdapter
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from arduinobot_msgs.action import ArduinobotTask
# integrates with the rclpy library
import rclpy
from rclpy.node import Node
import threading
from rclpy.action import ActionClient

# Allows the client to run in a separate thread
threading.Thread(target=lambda: rclpy.init()).start()

#Creates an action client, the interface by which it interacts
action_client = ActionClient(Node('alexa_interface'), ArduinobotTask, "task_server")

app = Flask(__name__)

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hi, how can we help?"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Online", speech_text)).set_should_end_session(
            False)

        goal = ArduinobotTask.Goal()
        goal.task_number = 0
        action_client.send_goal_async(goal)

        return handler_input.response_builder.response

# Handles the pick up pen command
class PickIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("PickIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Ok, I'm moving"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Pick", speech_text)).set_should_end_session(
            True)

        goal = ArduinobotTask.Goal()
        goal.task_number = 1
        action_client.send_goal_async(goal)

        return handler_input.response_builder.response

# Handles the sleep commands
class SleepIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("SleepIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Ok, see you later."

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Sleep", speech_text)).set_should_end_session(
            True)

        goal = ArduinobotTask.Goal()
        goal.task_number = 2
        action_client.send_goal_async(goal)

        return handler_input.response_builder.response

# Handles the wake command
class WakeIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("WakeIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Hi, I am ready"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Wake", speech_text)).set_should_end_session(
            True)
            
        goal = ArduinobotTask.Goal()
        goal.task_number = 0
        action_client.send_goal_async(goal)

        return handler_input.response_builder.response

# Handles a request not recognized by the robot
class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response

        speech = "Hmm, I don't know that. Can you please say it again?"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

# Registers the skills for the robot
skill_builder = SkillBuilder()
skill_builder.add_request_handler(LaunchRequestHandler())
skill_builder.add_request_handler(PickIntentHandler())
skill_builder.add_request_handler(SleepIntentHandler())
skill_builder.add_request_handler(WakeIntentHandler())
skill_builder.add_exception_handler(AllExceptionHandler())


skill_adapter = SkillAdapter(
    skill=skill_builder.create(), skill_id="amzn1.ask.skill.65af8809-5aaa-4c12-8f93-eafa3d3017c0", app=app)

@app.route("/")
def invoke_skill():
    return skill_adapter.dispatch_request()

skill_adapter.register(app=app, route="/")

if __name__ == '__main__':
    app.run()