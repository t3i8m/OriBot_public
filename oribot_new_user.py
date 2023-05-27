from oribot_user_db import appending_new_user, users_db_json
import time

# {'content_type': 'text', 'id': 5, 'message_id': 5, 'from_user': {'id': 785767433, 'is_bot': False, 
# 'first_name': 'Timur', 'username': 't3i8m', 'last_name': None, 'language_code': 'en', 'can_join_groups': None, 
# 'can_read_all_group_messages': None, 'supports_inline_queries': None, 'is_premium': None, 'added_to_attachment_menu': None}, 
# 'date': 1667677429, 'chat': {'id': 785767433, 'type': 'private', 'title': None, 'username': 't3i8m', 'first_name': 'Timur', 
# 'last_name': None, 'photo': None, 'bio': None, 'join_to_send_messages': None, 'join_by_request': None, 
# 'has_private_forwards': None, 'has_restricted_voice_and_video_messages': None, 'description': None, 'invite_link': None, 
# 'pinned_message': None, 'permissions': None, 'slow_mode_delay': None, 'message_auto_delete_time': None, 
# 'has_protected_content': None, 'sticker_set_name': None, 'can_set_sticker_set': None, 'linked_chat_id': None, 'location': None}, 'sender_chat': None, 'forward_from': None, 'forward_from_chat': None, 'forward_from_message_id': None, 'forward_signature': None, 'forward_sender_name': None, 'forward_date': None, 'is_automatic_forward': None, 'reply_to_message': None, 'via_bot': None, 'edit_date': None, 'has_protected_content': None, 'media_group_id': None, 'author_signature': 
# None, 'text': '/start', 'entities': [<telebot.types.MessageEntity object at 0x0000018B1973E310>], 'caption_entities': None, 
# 'audio': None, 'document': None, 'photo': None, 'sticker': None, 'video': None, 'video_note': None, 'voice': None, 
# 'caption': None, 'contact': None, 'location': None, 'venue': None, 'animation': None, 'dice': None, 'new_chat_member': None, 
# 'new_chat_members': None, 'left_chat_member': None, 'new_chat_title': None, 'new_chat_photo': None, 'delete_chat_photo': None, 
# 'group_chat_created': None, 'supergroup_chat_created': None, 'channel_chat_created': None, 'migrate_to_chat_id': None, 
# 'migrate_from_chat_id': None, 'pinned_message': None, 'invoice': None, 'successful_payment': None, 'connected_website': None, 
# 'reply_markup': None, 'json': {'message_id': 5, 'from': {'id': 785767433, 'is_bot': False, 'first_name': 'Timur', 
# 'username': 't3i8m', 'language_code': 'en'}, 'chat': {'id': 785767433, 'first_name': 'Timur', 'username': 't3i8m', 
# 'type': 'private'}, 'date': 1667677429, 'text': '/start', 'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]}}


class User:
    def __init__(self,user_first_name, user_name, chat_id, local_time, premium = False):
        self.user_first_name = user_first_name
        self.user_name = user_name
        self.chat_id = chat_id
        self.premium = premium
        self.time_of_registration = local_time
        self.lang = "Unknown"
        self.change_lang = True
        self.location = "Unknown"
        self.lat = 0
        self.long = 0
        self.manual_region=False
        self.schedule_forecast_new_event_location=False
        self.schedule_forecast_new_event_time = False
        # self.counter_for_scheduled_jobs = 0
        self.schedule_forecast_new_event_region=False
        self.schedule_region_flag=False
        self.schedule_active_event = False
        self.schedule_active_event_change_location = False
        self.schedule_remove_event = False
        self.schedule_event_remove_number = 1
        self.planner_every_day_txt_flag=False 
        self.planner_every_day_active_event=False
        self.planner_every_day_event_change_txt=False
        self.planner_every_day_event_get_time=False
        self.planner_scheduler_engine = None
        self.planner_thread_engine=None
        self.weather_schedule_engine=None
        self.weather_thread_engine=None
        # self.weather_remove_event_active=False
        self.planner_every_day_remove_event=False
        self.planner_every_day_event_remove_specific_event=1
        self.planner_specific_event_active = False
        self.planner_specific_event_txt_flag=False
        self.planner_specific_event_change_txt=False
        self.planner_specific_event_get_date=False
        self.planner_specific_event_get_time=False
        self.planner_specific_event_schedule_engine=None
        self.planner_specific_event_thread_engine=None
        self.planner_specific_event_remove_event=False
        self.planner_specific_event_remove_specific_event=1
        self.planner_specific_event_remove_active = False
        self.planner_every_day_event_remove_active = False
        self.schedule_remove_event_active=False
        self.date_activated_account = None
        self.time_flag_premium_function = None
        self.premium_expiring_date = None
        self.premium_schedule_engine=None
        self.premium_thread_engine=None
        self.activated_bot=True
        self.promo_code_activasion=True
        self.get_promo_code=False
        self.promo_code_expiring_date=None
        self.promo_code_date_activated_account=None
        self.promo_code_schedule_engine=None
        self.promo_code_thread_engine=None
        self.admin_chat_premium=False
        return


    # printing information about user
    def info(self):
        # print(f"Name:{self.user_first_name}\nUserName: {self.user_name}\nChatId: {self.chat_id}\nPremiumStatus: {self.premium}\nTimeOfRegistartion: {self.time_of_registration}\nLanguage: {self.lang}\nChange language: {self.change_lang}")
        return f"Name:{self.user_first_name}\nUserName: {self.user_name}\nChatId: {self.chat_id}\nPremiumStatus: {self.premium}\nTimeOfRegistartion: {self.time_of_registration}\nLanguage: {self.lang}\nChange language: {self.change_lang}"

def initialization_new_user(message)->(User):
    local_time = time.localtime()
    user = User(message.chat.first_name,message.chat.username, message.chat.id, transform_local_time(local_time))
    appending_new_user(user,users_db_json)
    return user

def transform_local_time(local_time):
    final_time = [local_time.tm_mday, local_time.tm_mon, local_time.tm_year]
    for index, n in enumerate(final_time):
        if index in [0,1] and n<10:
            final_time[index]="0"+str(n)
        else:
            final_time[index]=str(n)
    return ".".join(final_time)
