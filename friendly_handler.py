from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    InlineQueryHandler,
    BaseFilter)
from typing import Union, List, Pattern, Callable, Optional

from telegram.utils.helpers import DefaultValue, DEFAULT_FALSE


class FriendlyHandler:
    """
        to create a more user-friendly way to use handlers instead of a long list of dispatchers
        OPTIONS:
            + COMMAND HANDLER
            + MESSAGE HANDLER
            + CALLBACK QUERY HANDLER
            + INLINE QUERY HANDLER
    """
    def __init__(self, updater: Updater):
        self.dis = updater.dispatcher

    def command_handler(
            self,
            commands: Union[str, List[str]],
            filters: BaseFilter = None,
            allow_edited: bool = None,
            pass_args: bool = False,
            pass_update_queue: bool = False,
            pass_job_queue: bool = False,
            pass_user_data: bool = False,
            pass_chat_data: bool = False,
            run_async: Union[bool, DefaultValue] = DEFAULT_FALSE):
        def wrapper(func):
            self.dis.add_handler(CommandHandler(
                commands,
                func,
                filters,
                allow_edited,
                pass_args,
                pass_update_queue,
                pass_job_queue,
                pass_user_data,
                pass_chat_data,
                run_async, ))

        return wrapper

    def message_handler(
            self,
            filters: BaseFilter,
            pass_update_queue: bool = False,
            pass_job_queue: bool = False,
            pass_user_data: bool = False,
            pass_chat_data: bool = False,
            message_updates: bool = None,
            channel_post_updates: bool = None,
            edited_updates: bool = None,
            run_async: Union[bool, DefaultValue] = DEFAULT_FALSE, ):
        def wrapper(func):
            self.dis.add_handler(MessageHandler(
                filters,
                func,
                pass_update_queue,
                pass_job_queue,
                pass_user_data,
                pass_chat_data,
                message_updates,
                channel_post_updates,
                edited_updates,
                run_async
            ))

        return wrapper

    def callback_query_handler(
            self,
            ass_update_queue: bool = False,
            pass_job_queue: bool = False,
            pattern: Union[str, Pattern, type, Callable[[object], Optional[bool]]] = None,
            pass_groups: bool = False,
            pass_groupdict: bool = False,
            pass_user_data: bool = False,
            pass_chat_data: bool = False,
            run_async: Union[bool, DefaultValue] = DEFAULT_FALSE, ):
        def wrapper(func):
            self.dis.add_handler(CallbackQueryHandler(
                func,
                ass_update_queue,
                pass_job_queue,
                pattern,
                pass_groups,
                pass_groupdict,
                pass_user_data,
                pass_chat_data,
                run_async
            ))

        return wrapper

    def inline_query_handler(
            self,
            pass_update_queue: bool = False,
            pass_job_queue: bool = False,
            pattern: Union[str, Pattern] = None,
            pass_groups: bool = False,
            pass_groupdict: bool = False,
            pass_user_data: bool = False,
            pass_chat_data: bool = False,
            run_async: Union[bool, DefaultValue] = DEFAULT_FALSE,
            chat_types: List[str] = None, ):
        def wrapper(func):
            self.dis.add_handler(InlineQueryHandler(
                func,
                pass_update_queue,
                pass_job_queue,
                pattern,
                pass_groups,
                pass_groupdict,
                pass_user_data,
                pass_chat_data,
                run_async,
                chat_types, ))

        return wrapper


class ConvHandler:
    """
        DO NOT USE CONV-HANDLER, IT'S ON THE CONSTRUCTION
    """
    __conv_entry_point: str = None
    __conv_states: dict = None

    def __init__(self, updater: Updater):
        self.dis = updater.dispatcher

    def start(self, commands: List[str] = None, filters: BaseFilter = None):
        def wrapper(func):
            if commands:
                self.__conv_entry_point = CommandHandler(commands, func)

            elif filters:
                self.__conv_entry_point = MessageHandler(filters, func)

            else:
                raise ValueError

        return wrapper
