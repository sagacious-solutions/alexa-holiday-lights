from typing import Callable
import logging
from multiprocessing import Process

from flask import Flask
from flask import Response as FlaskResponse
from flask_ask_sdk.skill_adapter import SkillAdapter


from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from light_animations import xmasTree
from colors import LedColor

import config

sb = SkillBuilder()


def set_leds_violet():
    xmasTree.setSolid(LedColor.brightViolet)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class LightLoop:
    def __init__(self):
        self.process = Process(target=set_leds_violet)
        self.process.start()

    def set_looping_pattern(self, callback: Callable, kwargs={}):
        def loop_wrapper():
            while True:
                callback(**kwargs)
        self.process.terminate()
        self.process = Process(target=loop_wrapper)
        self.process.start()
    
    def set_static_lights(self, callback: Callable, kwargs={}):
        self.process.terminate()
        self.process = Process(target=callback, kwargs=kwargs)
        self.process.start()


light_loop = LightLoop()


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    speech_text = "Choose a lighting option."

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Holiday Lights", speech_text)).set_should_end_session(
        False).response


@sb.request_handler(can_handle_func=is_intent_name("setRainbowChaseIntent"))
def set_rainbow_chase_handler(handler_input):
    """Handler for setRainbowChaseIntent Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Settings lights to Rainbow Chase"
    light_loop.set_looping_pattern(xmasTree.rainbowCycle)
    return handler_input.response_builder.speak(speech_text).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("turnOffIntent"))
def turn_off_lights_intent(handler_input):
    """Handler to turn off the lights."""
    # type: (HandlerInput) -> Response
    speech_text = "Turning off the lights."
    light_loop.set_static_lights(xmasTree.setSolid, {LedColor.black})
    return handler_input.response_builder.speak(speech_text).set_should_end_session(
        True).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "You can set the light string with me."

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "oh, okay. Bye then!"

    return handler_input.response_builder.speak(speech_text).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """
    This handler will not be triggered except in supported locales,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = ("Sorry, thats not a thing.")
    reprompt = "Choose a light pattern. Trying saying Start Rainbow chase."
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "Something happened that I couldn't deal with."
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


app = Flask(__name__)
# Register your intent handlers to the skill_builder object

skill_adapter = SkillAdapter(
    skill=sb.create(), skill_id=config.secrets["ALEXA_SKILL_ID"],
    app=app)


@app.route("/", methods=['GET', 'POST'])
def invoke_skill():
    return skill_adapter.dispatch_request()


@app.route("/test/", methods=['GET', 'POST'])
def test_turn_yellow():
    light_loop.process.terminate()
    light_loop.process = Process(target=xmasTree.setSolid, args=[LedColor.yellow])
    light_loop.process.start()
    return FlaskResponse("Test Received!!", status=202)



if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", ssl_context=(config.https_cert, config.https_key))