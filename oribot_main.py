# 05.11.2022
import os
import time
import random
import telebot
import schedule
import threading
# import importlib.util
from time import sleep
# from pprint import pprint
from telebot import types
from datetime import datetime, timedelta
from telebot.types import LabeledPrice
from oribot_user_db import update_user
# from oribot_check_status import check_status
from oribot_ai_model import generated_answer
from oribot_all_messages_dict import all_messages
from oribot_new_user import initialization_new_user
from oribot_auth_data import token, payment_token, promo_codes_list
from oribot_weather_manager import from_coordinates_to_location, from_location_to_coordinates, weather_main
from oribot_translator import translate_current_text, all_languages_lst, emoji_code_dict, emoji_digits_time, emoji_description_commands

# username = @oriibbot

# Description:

# OriBot is a bot assistant. It offers several features, including:
# 📝 to-do planning
# ⛅️ sending weather by location
# 💬 chat with artificial intelligence
#  Press /start and go 🚀

# functions:
# /help - to see main functions
# /change_lang - to change language
# /promo_code - to use a promo code
# /buy_premium - to upgrade account to premium
# /weather - weather function
# /planner - planner function
# /all_lang - all available languages
# /region - to enter the location manually 
# /schedule_forecast - to schedule a weather forecast
# /new_forecast_event - to set new a forecast event
# /remove_forecast_event - to remove a forecast event
# /all_forecast_events - to see all forecast events
# /every_day_event - to schedule every day event
# /new_every_day_event - to set a new every day event
# /remove_every_day_event - to remove an every day event
# /all_every_day_events - to see all every day events
# /specific_event - to schedule a specific event
# /new_specific_event - to set a new specific event
# /remove_specific_event - to remove an every day event
# /all_specific_events - to see all every day events

# class Reboot_bot(Exception):
#     def __init__(self, message, obj):
#         self.message = message
#         self.obj=obj

users_dict = {} 
# users_dict = {
    # "id(string)":[
    # User <class>, 0 
    # weather <dict>, 1
    # planner <dict>  2
    # premium settings <dict> 3
    # promo code processing <dict> 4
    # ]
# } 

all_gifs_url_holder = {
    "We_are_working_on_it":['https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNGViN2ZhNDA1NDFmZDc1OTQzZDViODliMDVjM2E4N2JmYTVmMTIzOCZjdD1n/JIX9t2j0ZTN9S/giphy.gif', "https://media.giphy.com/media/l0K4hO8mVvq8Oygjm/giphy.gif", "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjA5ZTE5ZWQxMTk1M2Q2MzZiMDkxODlhNDUwYmMzMmY3YjA2ZGViZCZlcD12MV9pbnRlcm5hbF9naWZzX2dpZklkJmN0PWc/fQZX2aoRC1Tqw/giphy.gif", "https://media.giphy.com/media/nCVVpakhBTwBi/giphy.gif", "https://media.giphy.com/media/UYmY3vRnWpHHO/giphy.gif", "https://media.giphy.com/media/48zjXYRwBg5IQ/giphy.gif", "https://media.giphy.com/media/48zjXYRwBg5IQ/giphy.gif", "https://media.giphy.com/media/xUOwGfFOBuv547b06Q/giphy.gif","https://media.giphy.com/media/IzyI9jLVqDvB6/giphy.gif", "https://media.giphy.com/media/Sm9AfJRiZofjlrkAAl/giphy.gif", "https://media.giphy.com/media/T8Dhl1KPyzRqU/giphy.gif"],
    "Congrats":["https://media.giphy.com/media/chzz1FQgqhytWRWbp3/giphy.gif","https://media.giphy.com/media/duNowzaVje6Di3hnOu/giphy-downsized-large.gif", "https://media.giphy.com/media/duNowzaVje6Di3hnOu/giphy-downsized-large.gif", "https://media.giphy.com/media/cde4kPN98emjzL8QKH/giphy.gif","https://media.giphy.com/media/3o752eDHQgwl8zS3Oo/giphy.gif", "https://media.giphy.com/media/4oMoIbIQrvCjm/giphy.gif","https://media.giphy.com/media/S8Bkx6nxeiRSOWsjLO/giphy.gif", "https://media.giphy.com/media/s2qXK8wAvkHTO/giphy.gif","https://media.giphy.com/media/6nuiJjOOQBBn2/giphy.gif","https://media.giphy.com/media/6nuiJjOOQBBn2/giphy.gif"],
    "Smth_went_wrong":["https://media.giphy.com/media/XyLKdaVbQ3xg6o0sKy/giphy.gif", "https://media.giphy.com/media/HO05rCg5yuaOrpk14J/giphy.gif", "https://media.giphy.com/media/HO05rCg5yuaOrpk14J/giphy.gif", "https://media.giphy.com/media/PjruB3DPAZ8JutBZ8J/giphy.gif", "https://media.giphy.com/media/l46CwEYnbFtFfjZNS/giphy.gif", "https://media.giphy.com/media/nRNF5nlDgr8bK/giphy.gif", "https://media.giphy.com/media/jaf4JwRREzsuGMkkDk/giphy.gif", "https://media.giphy.com/media/jaf4JwRREzsuGMkkDk/giphy.gif", "https://media.giphy.com/media/WUrgA8xOSUJj6JZoJC/giphy.gif", "https://media.giphy.com/media/Crdyd3KhccSNa/giphy.gif", "https://media.giphy.com/media/4F0f7oz0wU4BfuaAQe/giphy.gif"],
}
price = [(LabeledPrice(label="Subscription on 1 month", amount=1*100))]



def telegram_bot():
    # users_dict_upd={}
    # global users_dict
    # if users_dict_upd!={}:
    #     users_dict=users_dict_upd

    # print("telegram_bot")

    bot = telebot.TeleBot(token)

    def detect_lang_func(message:dict, chat_id=""):
        # # try:
        #     if users_dict[str(message.chat.id)][0].activated_bot:
            try:
                if type(message)==dict or type(message)==telebot.types.Message:
                    if emoji_code_dict[message.text] in [n.upper() for n in all_languages_lst]:
                        users_dict[str(message.chat.id)][0].lang = emoji_code_dict[message.text].lower()
                        return True
                    else:
                        if users_dict[str(message.chat.id)][0].lang != "en":
                            bot.send_message(message.chat.id, all_messages["Error_lang_not_available"].format("❗️"))
                            bot.send_message(message.chat.id, all_messages["To_see_all_languages"].format("/all_lang"))
                        users_dict[str(message.chat.id)][0].lang = "en"
                        sleep(1)
                elif type(message)==str:
                    if message in all_languages_lst:
                        print(message)
                        if message=="uk":
                            users_dict[chat_id][0].lang = "en"
                        else:
                            users_dict[chat_id][0].lang = message
                        return True
                    else:
                        if users_dict[chat_id][0].lang != "en":
                            bot.send_message(chat_id, all_messages["Error_lang_not_available"].format("❗️"))
                            bot.send_message(chat_id, all_messages["To_see_all_languages"].format("/all_lang"))
                        users_dict[chat_id][0].lang = "en"
                        sleep(1)
            except Exception as ex:
                bot.send_message(message.chat.id, all_messages["Error_lang_emoji"].format("/change_lang", "❗️"))
                users_dict[str(message.chat.id)][0].lang = "en"
                users_dict[str(message.chat.id)][0].change_lang=False
                update_user(users_dict[str(message.chat.id)][0]) 
                sleep(1)
                message_about_plans(message)
            # else:
            #     bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        # except Exception as ex:
        #     print(ex)
        #     # bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
        #         # return False
            return 

    def sending_animation_bot_working(message, type_gif:str):
        try:
            try:
                if users_dict[str(message.chat.id)][0].activated_bot:
                    try:
                        bot.send_animation(message.chat.id, animation=all_gifs_url_holder[type_gif][random.randint(0,len(all_gifs_url_holder[type_gif])-1)])
                        sleep(1)
                        if type_gif=="We_are_working_on_it":
                            bot.send_message(message.chat.id,translate_current_text("We are working on it. Please stand by", lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang))
                        
                    except Exception as ex:
                        print(ex)
                        bot.send_message(message.chat.id,translate_current_text("We are working on it. Please stand by", lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang))
                else:
                    bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
            except KeyError:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
                
            except Exception:
                try:
                    if users_dict[message][0].activated_bot:
                        try:
                            bot.send_animation(message, animation=all_gifs_url_holder[type_gif][random.randint(0,len(all_gifs_url_holder[type_gif])-1)])
                            sleep(1)
                            if type_gif=="We_are_working_on_it":
                                bot.send_message(message,translate_current_text("We are working on it. Please stand by", lang_from="en", lang_to=users_dict[message][0].lang))
                            
                        except Exception as ex:
                            print(ex)
                            bot.send_message(message,translate_current_text("We are working on it. Please stand by", lang_from="en", lang_to=users_dict[message][0].lang))
                    else:
                            bot.send_message(message, all_messages["Use_command_start"].format("/start"))
                except KeyError:
                    bot.send_message(message, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) sending_animation_bot_working",ex)
        return


    def message_about_plans(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                keyboard = types.InlineKeyboardMarkup()
                if users_dict[str(message.chat.id)][0].premium==False:
                    promo_code = types.InlineKeyboardButton(text=translate_current_text("Promo code",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🏷", callback_data="promo_code")
                    keyboard.add(promo_code)
                basic_plan = types.InlineKeyboardButton(text=translate_current_text("About Basic 😄",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en"), callback_data="basic_plan")
                premium_plan = types.InlineKeyboardButton(text=translate_current_text("About Premium 😎",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en"), callback_data="premium_plan")
                keyboard.add(basic_plan,premium_plan)
                bot.send_message(message.chat.id, translate_current_text(all_messages["About_oribot"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("OriBot","🤗","€", "😉"), reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) message_about_plans",ex)
                # return False
        return
    

    def message_about_restrictions(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                keyboard_for_schedule_forecast_buy_premium = types.InlineKeyboardMarkup()
                button_buy_premium_schedule_forecast = types.InlineKeyboardButton(text=translate_current_text("Premium",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ⭐️", callback_data="buy_premium")
                keyboard_for_schedule_forecast_buy_premium.add(button_buy_premium_schedule_forecast)
                bot.send_message(message.chat.id, translate_current_text(all_messages["Location_basic_restriction"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("😀"), reply_markup=keyboard_for_schedule_forecast_buy_premium)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) message_about_restrictions",ex)
        return

    @bot.message_handler(commands=["promo_code"])
    def promo_code_processing(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if users_dict[str(message.chat.id)][0].premium==False:
                    if users_dict[str(message.chat.id)][0].promo_code_activasion:
                        users_dict[str(message.chat.id)][0].promo_code_activasion=False
                        users_dict[str(message.chat.id)][0].get_promo_code=True
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Promo_code_start"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👉"))
                    else:
                        keyboard_for_premium = types.InlineKeyboardMarkup()
                        button_buy_premium= types.InlineKeyboardButton(text=translate_current_text("Premium",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ⭐️", callback_data="buy_premium")
                        keyboard_for_premium.add(button_buy_premium) 
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Promo_code_limitation"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("/buy_premium", "👇"), reply_markup=keyboard_for_premium)
                else:
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Premium_account_already_activeted"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(users_dict[str(message.chat.id)][0].promo_code_expiring_date[0], "❗️"))
            else:
                    bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
        return

    def job_that_executes_once_promo_code_premium_control(current_event:dict, message):
        global users_dict
        if current_event["Expiring_time"]==datetime.now().strftime('%H:%M'):
            if datetime.strptime(current_event["Expiring_date"], "%d.%m.%Y")==(datetime.now().date()+timedelta(days=1)):
                bot.send_message(message.chat.id, translate_current_text(all_messages["Payment_expiring_reminder"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("❗️", "❗️"))
            elif ((datetime.strptime(users_dict[str(message.chat.id)][4]["Promo_code"][0]["Expiring_date"], "%d.%m.%Y").date()-datetime.now().date()).days)==0:
                users_dict[str(message.chat.id)][0].premium=False
                update_user(users_dict[str(message.chat.id)][0])
                users_dict[str(message.chat.id)][4]["Promo_code"]=[None]
                keyboard_for_premium = types.InlineKeyboardMarkup()
                button_buy_premium= types.InlineKeyboardButton(text=translate_current_text("Premium",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ⭐️", callback_data="buy_premium")
                keyboard_for_premium.add(button_buy_premium)
                bot.send_message(message.chat.id, translate_current_text(all_messages["Premium_expired"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("/buy_premium", "👇"), reply_markup=keyboard_for_premium)
                users_dict[str(message.chat.id)][0].promo_code_schedule_engine.clear()
                users_dict[str(message.chat.id)][0].promo_code_schedule_engine=None
                lambda users_dict:users_dict[str(message.chat.id)][0].promo_code_thread_engine.join()
                users_dict[str(message.chat.id)][0].promo_code_thread_engine=None
            else:
                return
        else:
            return
    
    def promo_code_premium_control(message):
        try:
            users_dict[str(message.chat.id)][0].promo_code_schedule_engine=schedule.Scheduler()
            users_dict[str(message.chat.id)][0].promo_code_schedule_engine.every().day.at(str(users_dict[str(message.chat.id)][4]["Promo_code"][0]["Expiring_time"])+":00").do(job_that_executes_once_promo_code_premium_control, users_dict[str(message.chat.id)][4]["Promo_code"][0], message)
            if users_dict[str(message.chat.id)][0].promo_code_thread_engine==None and users_dict[str(message.chat.id)][0].promo_code_schedule_engine!=None:
                def run_scheduler(scheduler):
                    while True:
                        scheduler.run_pending()
                        time.sleep(1)
                users_dict[str(message.chat.id)][0].promo_code_thread_engine = threading.Thread(target=run_scheduler, args=(users_dict[str(message.chat.id)][0].promo_code_schedule_engine,))
                users_dict[str(message.chat.id)][0].promo_code_thread_engine.start()
            return 
        except Exception as ex:
            print("promo_code_premium_control",ex)
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            return 

# help functions            
    @bot.message_handler(commands=["help"])
    def help_func(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                bot.send_message(message.chat.id, translate_current_text(all_messages["Help_func_text"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("OriBot","👇", "/weather", "/planner", "/change_lang", "/buy_premium", "❔", "OriBot", "@oribot_support_bot"))
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) buy_premium_main",ex)
        return

    # payment functions
    @bot.message_handler(commands=["buy_premium"])
    def buy_premium_main(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if users_dict[str(message.chat.id)][0].premium!=True:
                    # datetime.now()
                    current_time = datetime.now()
                    if users_dict[str(message.chat.id)][0].time_flag_premium_function==None or (current_time-users_dict[str(message.chat.id)][0].time_flag_premium_function).seconds>=600:
                        users_dict[str(message.chat.id)][0].time_flag_premium_function=datetime.now()
                        print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) has started buy_premium function")
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Premium_about_text"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("OriBot","€", "👇"))
                    
                        # invoice
                        bot.send_invoice(
                                chat_id=message.chat.id,  # Chat ID
                                title=translate_current_text("Premium Plan for OriBot", lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang)+" ⭐️",  # Название подписки
                                # description=translate_current_text("Bot Premium subscription activation {}", lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("⭐️"),  # Description of subscription
                                description=translate_current_text("As a Premium user, you will have all the features of {} unlocked:\n\n{}You can ask unlimited number of questions (for example: Who is Michael Jordan?)\n{}Daily planner with all functions\n{}Sending scheduled weather forecast\n\nTry all the functions yourself{}", lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("OriBot", "❔","📝", "🌤", "🚀"),  # Description of subscription

                                currency="eur",  # Payment currency
                                # photo_url=https://files.stripe.com/links/MDB8YWNjdF8xTXlmemFIWndFd2N3T1hufGZsX3Rlc3RfSlcyeTRBUlVqUm5tS2hkV3FFR1JRVFAw00tXEPiTwM
                                photo_url=  "https://lh3.googleusercontent.com/pw/AJFCJaUKUUDjCeLPXPfzwYmW4UQ9vYqLvf_Mjv3iPHTvMu57bv6leNVyrAKHJUN9vjO14IIjpdYxgs2RxYjX842GXm87N6cTOv1FV-_-lVFyMjjABYR4CBg4t6gKk-uugXTgRgxWG_78iQKRTEmnpG0mVF4=w720-h719-s-no?authuser=2",  # Product photo URL
                                provider_token=payment_token,  # Payment system token
                                start_parameter="one-month-subscription",  # Parameter for initialising the payment
                                photo_width=512,  # Product photo width
                                photo_height=512,  # Product photo height
                                is_flexible=False,  # Payment flexibility flag
                                need_shipping_address=False,
                                invoice_payload="one-month-subscription",  # Useful load of the account
                                prices=price,  # Subscription price
                            )
                    else:
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Premium_time_limit"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🕟"))
                else:
                    try:
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Premium_account_already_activeted"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(users_dict[str(message.chat.id)][0].premium_expiring_date[0], "❗️"))
                    except Exception as ex:
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Premium_account_already_activeted"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(users_dict[str(message.chat.id)][0].promo_code_expiring_date[0], "❗️"))
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) buy_premium_main",ex)
        return

    @bot.pre_checkout_query_handler(lambda query:True)
    def pre_check_out_query(pre_checkout_query):
        bot.answer_pre_checkout_query(pre_checkout_query.id,ok=True)

    @bot.message_handler(content_types=['successful_payment'])
    def process_payment_successful(message):
        try:
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id})",message.successful_payment)
            users_dict[str(message.chat.id)][0].premium=True
            users_dict[str(message.chat.id)][0].premium_expiring_date = [(datetime.now()+timedelta(days=30)).strftime('%d.%m.%Y'), (datetime.now()+timedelta(days=30)).strftime('%H:%M')]
            users_dict[str(message.chat.id)][0].date_activated_account = [datetime.now().strftime('%d.%m.%Y'), datetime.now().strftime('%H:%M')]
            users_dict[str(message.chat.id)][3]["Premium"][0] = {
                "Activation_date":users_dict[str(message.chat.id)][0].date_activated_account,
                "Expiring_date":users_dict[str(message.chat.id)][0].premium_expiring_date[0],
                "Expiring_time":users_dict[str(message.chat.id)][0].premium_expiring_date[1],
                "Active":True,
            }
            update_user(users_dict[str(message.chat.id)][0])
            premium_control(message)
            # keyboard_for_premium_commands = types.InlineKeyboardMarkup()
            # list_of_commands_premium = types.InlineKeyboardButton(text=translate_current_text("Commands",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ✍️", callback_data="available_commands")
            # keyboard_for_premium_commands.add(list_of_commands_premium) 
            keyboard_for_premium_available_commands = types.InlineKeyboardMarkup()
            button_premium_weather = types.InlineKeyboardButton(text=translate_current_text("Weather",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ⛅️", callback_data="available_commands_premium_weather")
            button_premium_planner = types.InlineKeyboardButton(text=translate_current_text("Planner",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 📔", callback_data="available_commands_planner")
            # button_premium_news = types.InlineKeyboardButton(text=translate_current_text("News",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" 🗞", callback_data="available_commands_premium_news")
            keyboard_for_premium_available_commands.add(button_premium_weather)
            keyboard_for_premium_available_commands.add(button_premium_planner)
            # keyboard_for_premium_available_commands.add(button_premium_news)
            # testing_command(message)
            sleep(1)
            bot.send_message(message.chat.id, translate_current_text(all_messages["Payment_was_successful"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🥳"))
            sleep(1)
            sending_animation_bot_working(message, type_gif="Congrats")
            bot.send_message(message.chat.id, translate_current_text(all_messages["Premium_thanks_from_oribot_team"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("OriBot","💙"))
            sleep(1)
            bot.send_message(message.chat.id, translate_current_text(all_messages["Available_commands_premium"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🔓","👇","/weather","/planner","❔", users_dict[str(message.chat.id)][0].premium_expiring_date[0]), reply_markup=keyboard_for_premium_available_commands, parse_mode='HTML')
            # bot.send_message(message.chat.id, translate_current_text(all_messages["Payment_thanks_message"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("OriBot","💙", "OriBot","👇", "❔","📝", "🌤", "🚀"), reply_markup=keyboard_for_premium_commands)
            return
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) process_payment_successful",ex)
        return

    @bot.message_handler(content_types=['unsuccessful_payment'])
    def process_payment_unsuccessful(message):
        try:
            users_dict[str(message.chat.id)][0].time_flag_premium_function=None
            keyboard_for_premium = types.InlineKeyboardMarkup()
            button_buy_premium= types.InlineKeyboardButton(text=translate_current_text("Premium",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ⭐️", callback_data="buy_premium")
            keyboard_for_premium.add(button_buy_premium) 
            print(f"Unsuccessful payment {users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id})")
            sending_animation_bot_working(message, type_gif="Smth_went_wrong")
            sleep(1)
            bot.send_message(message.chat.id, translate_current_text(all_messages["Payment_was_unsuccessful"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("☹️", "@oribot_support_bot"), reply_markup=keyboard_for_premium)
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) process_payment_unsuccessful",ex)
        return
    
    def job_that_executes_once_premium_control(current_event:dict, message):
        global users_dict
        if current_event["Expiring_time"]==datetime.now().strftime('%H:%M'):
            if datetime.strptime(current_event["Expiring_date"], "%d.%m.%Y")==(datetime.now().date()+timedelta(days=1)):
                bot.send_message(message.chat.id, translate_current_text(all_messages["Payment_expiring_reminder"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("❗️", "❗️"))
            elif ((datetime.strptime(users_dict[str(message.chat.id)][3]["Premium"][0]["Expiring_date"], "%d.%m.%Y").date()-datetime.now().date()).days)==0:
                users_dict[str(message.chat.id)][0].premium=False
                update_user(users_dict[str(message.chat.id)][0])
                users_dict[str(message.chat.id)][3]["Premium"]=[None]
                users_dict[str(message.chat.id)][0].time_flag_premium_function=None
                keyboard_for_premium = types.InlineKeyboardMarkup()
                button_buy_premium= types.InlineKeyboardButton(text=translate_current_text("Premium",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ⭐️", callback_data="buy_premium")
                keyboard_for_premium.add(button_buy_premium)
                bot.send_message(message.chat.id, translate_current_text(all_messages["Premium_expired"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("/buy_premium", "👇"), reply_markup=keyboard_for_premium)
                users_dict[str(message.chat.id)][0].premium_schedule_engine.clear()
                users_dict[str(message.chat.id)][0].premium_schedule_engine=None
                lambda users_dict:users_dict[str(message.chat.id)][0].premium_thread_engine.join()
                users_dict[str(message.chat.id)][0].premium_thread_engine=None
            else:
                return
        else:
            return
    
    def job_that_executes_once_premium_control_upd(current_event:dict, message):
        global users_dict
        if current_event["Expiring_time"]==datetime.now().strftime('%H:%M'):
            if datetime.strptime(current_event["Expiring_date"], "%d.%m.%Y")==(datetime.now().date()+timedelta(days=1)):
                bot.send_message(message, translate_current_text(all_messages["Payment_expiring_reminder"], lang_from="en", lang_to=users_dict[message][0].lang).format("❗️", "❗️"))
            elif ((datetime.strptime(users_dict[message][3]["Premium"][0]["Expiring_date"], "%d.%m.%Y").date()-datetime.now().date()).days)==0:
                users_dict[message][0].premium=False
                update_user(users_dict[message][0])
                users_dict[message][3]["Premium"]=[None]
                users_dict[message][0].time_flag_premium_function=None
                keyboard_for_premium = types.InlineKeyboardMarkup()
                button_buy_premium= types.InlineKeyboardButton(text=translate_current_text("Premium",lang_to=users_dict[message][0].lang, lang_from="en")+" ⭐️", callback_data="buy_premium")
                keyboard_for_premium.add(button_buy_premium)
                bot.send_message(message, translate_current_text(all_messages["Premium_expired"], lang_from="en", lang_to=users_dict[message][0].lang).format("/buy_premium", "👇"), reply_markup=keyboard_for_premium)
                users_dict[message][0].premium_schedule_engine.clear()
                users_dict[message][0].premium_schedule_engine=None
                lambda users_dict:users_dict[message][0].premium_thread_engine.join()
                users_dict[message][0].premium_thread_engine=None
            else:
                return
        else:
            return

    def premium_control(message):
        try:
            try:
                users_dict[str(message.chat.id)][0].premium_schedule_engine=schedule.Scheduler()
                users_dict[str(message.chat.id)][0].premium_schedule_engine.every().day.at(str(users_dict[str(message.chat.id)][3]["Premium"][0]["Expiring_time"])+":00").do(job_that_executes_once_premium_control, users_dict[str(message.chat.id)][3]["Premium"][0], message)
                if users_dict[str(message.chat.id)][0].premium_thread_engine==None and users_dict[str(message.chat.id)][0].premium_schedule_engine!=None:
                    def run_scheduler(scheduler):
                        while True:
                            scheduler.run_pending()
                            time.sleep(1)
                    users_dict[str(message.chat.id)][0].premium_thread_engine = threading.Thread(target=run_scheduler, args=(users_dict[str(message.chat.id)][0].premium_schedule_engine,))
                    users_dict[str(message.chat.id)][0].premium_thread_engine.start()
                return 
            except Exception as ex:
                users_dict[message][0].premium_schedule_engine=schedule.Scheduler()
                users_dict[message][0].premium_schedule_engine.every().day.at(str(users_dict[message][3]["Premium"][0]["Expiring_time"])+":00").do(job_that_executes_once_premium_control_upd, users_dict[message][3]["Premium"][0], message)
                if users_dict[message][0].premium_thread_engine==None and users_dict[message][0].premium_schedule_engine!=None:
                    def run_scheduler(scheduler):
                        while True:
                            scheduler.run_pending()
                            time.sleep(1)
                    users_dict[message][0].premium_thread_engine = threading.Thread(target=run_scheduler, args=(users_dict[message][0].premium_schedule_engine,))
                    users_dict[message][0].premium_thread_engine.start()
                return 
        except Exception as ex:
            print("premium_control",ex)
            return

    # setting functions
    @bot.message_handler(commands=["start"])
    def start_message(message):
        if str(message.chat.id) not in users_dict.keys():
            # bot.send_message(message.chat.id, all_messages["Restrictions_at_the_moment"].format("❗️", "❗️"))
            # sleep(2)
            users_dict[str(message.chat.id)] = []
            users_dict[str(message.chat.id)].append(initialization_new_user(message))
            users_dict[str(message.chat.id)].append({"All_weather_events":[]})
            users_dict[str(message.chat.id)].append({"All_every_day_events":[],"All_specific_events":[]})
            users_dict[str(message.chat.id)].append({"Premium":[None]})
            users_dict[str(message.chat.id)].append({"Promo_code":[None]})
            if int(users_dict[str(message.chat.id)][0].chat_id)==785767433:
                users_dict[str(message.chat.id)][0].premium=True
                users_dict[str(message.chat.id)][0].premium_expiring_date=["",""]

            keyboard_for_all_lang = types.InlineKeyboardMarkup()
            button_for_all_lang = types.InlineKeyboardButton(text="All languages"+" 🌐", callback_data="button_for_all_lang")
            keyboard_for_all_lang.add(button_for_all_lang) 

            bot.send_message(message.chat.id, (all_messages["Start_message"]).format(users_dict[str(message.chat.id)][0].user_first_name.title(), "👋","🚩"))
            bot.send_message(message.chat.id, (all_messages["Start_message_2nd_part"]).format("/all_lang", "👉"), reply_markup=keyboard_for_all_lang)
        else:
            try:
                text_message_translated = translate_current_text(all_messages["Already_used_/start"], lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en").format("/help")
                if text_message_translated!="'UNKNOWN' IS AN INVALID TARGET LANGUAGE . EXAMPLE: LANGPAIR=EN|IT USING 2 LETTER ISO OR RFC3066 LIKE ZH-CN. ALMOST ALL LANGUAGES SUPPORTED BUT SOME MAY HAVE NO CONTENT":
                    bot.send_message(message.chat.id, text_message_translated)
                else:
                    raise Exception
            except Exception as ex:
                print(ex)
                bot.send_message(message.chat.id, (all_messages["Already_used_/start"]).format("/help", "🙃"))
        return

    @bot.message_handler(commands=["change_lang"])
    def change_lang(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                try:
                    keyboard_for_all_lang = types.InlineKeyboardMarkup()
                    button_for_all_lang = types.InlineKeyboardButton(text="All languages"+" 🌐", callback_data="button_for_all_lang")
                    keyboard_for_all_lang.add(button_for_all_lang) 
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Change_lang"], lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en").format("🚩"))
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Start_message_2nd_part"], lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en").format("/all_lang", "👉"), reply_markup=keyboard_for_all_lang)
                except Exception as ex:
                    keyboard_for_all_lang = types.InlineKeyboardMarkup()
                    button_for_all_lang = types.InlineKeyboardButton(text="All languages"+" 🌐", callback_data="button_for_all_lang")
                    keyboard_for_all_lang.add(button_for_all_lang) 
                    bot.send_message(message.chat.id, all_messages["Change_lang"].format("🚩"))
                    bot.send_message(message.chat.id, all_messages["Start_message_2nd_part"].format("/all_lang", "👉"), reply_markup=keyboard_for_all_lang)
                else:
                    users_dict[str(message.chat.id)][0].change_lang = True
                    update_user(users_dict[str(message.chat.id)][0])
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) change_lang",ex)
        return
    
    @bot.message_handler(commands = ["all_lang"])
    def all_lang(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if users_dict[str(message.chat.id)][0].lang!="Unknown":
                    bot.send_message(message.chat.id, translate_current_text(all_messages["All_available_languages"], lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en").format("👇"))
                    # bot.send_message(message.chat.id, translate_current_text(all_messages["If_want_set_lang"], lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en").format("/change_lang", "🚩"))
                else:
                    bot.send_message(message.chat.id, all_messages["All_available_languages"].format("👇"))
                    # bot.send_message(message.chat.id, emoji_description_commands.format('am', 'az', 'be', 'bg', 'de', 'ee', 'es', 'fi', 'fr', 'uk', 'hr', 'hu', 'it', 'lt', 'lv', 'mt', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'sa', 'si', 'sk', 'th', 'tr', 'uz'))
                    # bot.send_message(message.chat.id, all_messages["If_want_set_lang"].format("/change_lang", "🚩"))
                bot.send_message(message.chat.id, emoji_description_commands.format('am', 'az', 'be', 'bg', 'de', 'ee', 'es', 'fi', 'fr', 'uk', 'hr', 'hu', 'it', 'lt', 'lv', 'mt', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'si', 'sk', 'th', 'tr', 'uz'))
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) all_lang",ex)
        return
    
    @bot.message_handler(commands = ['am', 'az', 'be', 'bg', 'de', 'ee', 'es', 'fi', 'fr', 'uk', 'hr', 'hu', 'it', 'lt', 'lv', 'mt', 'nl', 'no', 'pl', 'pt', 'ro', 'ru', 'si', 'sk', 'th', 'tr', 'uz'])
    def decode_language(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                status_detect, status_upd = detect_lang_func(message.text[1:], chat_id = str(message.chat.id)), update_user(users_dict[str(message.chat.id)][0])
                if status_detect == True and status_upd == True:
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Language_successful"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👍"))
                    bot.send_message(message.chat.id, translate_current_text(all_messages["If_want_set_lang"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("/change_lang", "🚩"))
                    users_dict[str(message.chat.id)][0].change_lang = False
                    message_about_plans(message)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) decode_language",ex)
        return
    
    # forecast functions
    @bot.message_handler(content_types=["location"])
    def weather_location_lat_long(message="",period=0):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if users_dict[str(message.chat.id)][0].schedule_forecast_new_event_location==False:
                    if message.location!=None or period!=0:
                        users_dict[str(message.chat.id)][0].lat = message.location.latitude
                        users_dict[str(message.chat.id)][0].long = message.location.longitude
                        users_dict[str(message.chat.id)][0].location = from_coordinates_to_location(long=users_dict[str(message.chat.id)][0].lat, lat=users_dict[str(message.chat.id)][0].long)
                        update_user(users_dict[str(message.chat.id)][0])
                    try:
                        if users_dict[str(message.chat.id)][0].location!=False:
                            if users_dict[str(message.chat.id)][0].premium:
                                    keyboard_for_location_days_premium = types.InlineKeyboardMarkup()
                                    button_one_day_location_premium = types.InlineKeyboardButton(text="1️⃣", callback_data="button_one_day_location_premium_1")
                                    button_three_days_location_premium = types.InlineKeyboardButton(text="3️⃣", callback_data="button_three_days_location_premium_3")
                                    button_seven_days_location_premium = types.InlineKeyboardButton(text="7️⃣", callback_data="button_seven_days_location_premium_7")
                                    button_ten_days_location_premium = types.InlineKeyboardButton(text="🔟", callback_data="button_ten_days_location_premium_10")
                                    keyboard_for_location_days_premium.add(button_one_day_location_premium,button_three_days_location_premium)
                                    keyboard_for_location_days_premium.add(button_seven_days_location_premium,button_ten_days_location_premium)
                                    bot.send_message(message.chat.id, translate_current_text(all_messages["Location_days_premium"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(users_dict[str(message.chat.id)][0].location,"📍","🗓"), reply_markup=keyboard_for_location_days_premium)
                            else:
                                    keyboard_for_location_days_basic = types.InlineKeyboardMarkup()
                                    button_one_day_location_basic = types.InlineKeyboardButton(text="1️⃣", callback_data="button_one_day_location_basic_1")
                                    button_three_days_location_basic = types.InlineKeyboardButton(text="3️⃣🔒", callback_data="button_three_days_location_basic_3")
                                    button_seven_days_location_basic = types.InlineKeyboardButton(text="7️⃣🔒", callback_data="button_seven_days_location_basic_7")
                                    button_ten_days_location_basic = types.InlineKeyboardButton(text="🔟🔒", callback_data="button_ten_days_location_basic_10")
                                    keyboard_for_location_days_basic.add(button_one_day_location_basic,button_three_days_location_basic)
                                    keyboard_for_location_days_basic.add(button_seven_days_location_basic,button_ten_days_location_basic)
                                    bot.send_message(message.chat.id, translate_current_text(all_messages["Location_days_premium"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(users_dict[str(message.chat.id)][0].location,"📍","🗓"), reply_markup=keyboard_for_location_days_basic)
                        else:
                                keyboard_region = types.InlineKeyboardMarkup()
                                button_weather_region = types.InlineKeyboardButton(text=translate_current_text("Region",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🗺", callback_data="button_weather_region")
                                keyboard_region.add(button_weather_region)
                                bot.send_message(message.chat.id, translate_current_text(all_messages["Location_incorrect"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🧐","/region"), reply_markup=keyboard_region)
                    except Exception as ex:
                        print("weather_location_lat_long()", ex)
                else:
                    if message.location!=None or period!=0:
                        if len(users_dict[str(message.chat.id)][1]["All_weather_events"])<10:
                            users_dict[str(message.chat.id)][1]["All_weather_events"].append(
                                    
                                    {
                                    "Lat":message.location.latitude,
                                    "Long":message.location.longitude,
                                    "Location":from_coordinates_to_location(long=message.location.latitude, lat=message.location.longitude),
                                    "Time":None,
                                    "Remove":False,
                                    "Scheduled":False,
                                    "Schedule_job":None,
                                    "Lang":users_dict[str(message.chat.id)][0].lang
                                    }
                                )
                            users_dict[str(message.chat.id)][0].schedule_forecast_new_event_location=False
                            users_dict[str(message.chat.id)][0].schedule_region_flag=False
                            users_dict[str(message.chat.id)][0].schedule_forecast_new_event_time=True
                            users_dict[str(message.chat.id)][0].schedule_forecast_new_event_region=False

                            bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_new_event_get_time"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("⌛️"))
                        else:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_new_event_reached_maximum_count"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🔟","/remove_forecast_event", "/all_forecast_events"))
                            users_dict[str(message.chat.id)][0].schedule_forecast_new_event_location=False
                    else:
                        keyboard_region = types.InlineKeyboardMarkup()
                        button_weather_region = types.InlineKeyboardButton(text=translate_current_text("Region",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🗺", callback_data="button_weather_region")
                        keyboard_region.add(button_weather_region)
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Location_incorrect"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🧐","/region"), reply_markup=keyboard_region)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) weather_location_lat_long",ex)
        return

    @bot.message_handler(commands=["region"])
    def region_oribot(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if users_dict[str(message.chat.id)][0].schedule_region_flag:
                    users_dict[str(message.chat.id)][0].schedule_forecast_new_event_region=True
                else:
                    users_dict[str(message.chat.id)][0].manual_region=True
                bot.send_message(message.chat.id, translate_current_text(all_messages["Region_start_message"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang)+" 🌐:")
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) region_oribot",ex)
        return

    @bot.message_handler(commands=["schedule_forecast"])
    def scheduling_forecast(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if users_dict[str(message.chat.id)][0].premium:
                    keyboard_for_schedule_forecast_functions= types.InlineKeyboardMarkup()
                    button_new_event_schedule_forecast = types.InlineKeyboardButton(text=translate_current_text("New event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🆕", callback_data="button_new_event_schedule_forecast")
                    button_remove_event_schedule_forecast = types.InlineKeyboardButton(text=translate_current_text("Remove event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🗑", callback_data="button_remove_event_schedule_forecast")
                    button_all_event_schedule_forecast = types.InlineKeyboardButton(text=translate_current_text("All events",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 📜", callback_data="button_print_all_events_schedule_forecast")
                    keyboard_for_schedule_forecast_functions.add(button_new_event_schedule_forecast)
                    keyboard_for_schedule_forecast_functions.add(button_remove_event_schedule_forecast)
                    keyboard_for_schedule_forecast_functions.add(button_all_event_schedule_forecast)
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_events_start_message"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("⏰",emoji_digits_time[len(users_dict[str(message.chat.id)][1]["All_weather_events"])],"/new_forecast_event", "🆕","/remove_forecast_event","🗑","/all_forecast_events","📜"),  reply_markup=keyboard_for_schedule_forecast_functions)
                else:
                    message_about_restrictions(message)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) scheduling_forecast",ex)
        return
    
    @bot.message_handler(commands=["remove_forecast_event"])
    def remove_event(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if users_dict[str(message.chat.id)][0].premium:
                    if len(users_dict[str(message.chat.id)][1]["All_weather_events"])>0:
                        users_dict[str(message.chat.id)][0].schedule_remove_event_active=True
                        users_dict[str(message.chat.id)][0].schedule_remove_event=True
                        message_holder = print_all_events(message)
                        users_dict[str(message.chat.id)][0].schedule_remove_event=False
                        keyboard_for_remove_buttons = types.InlineKeyboardMarkup()
                        if len(users_dict[str(message.chat.id)][1]["All_weather_events"])%2==0:
                            for button in range(1,len(users_dict[str(message.chat.id)][1]["All_weather_events"])+1,2):
                                sample_button_remove_n_event_first = types.InlineKeyboardButton(text=emoji_digits_time[button], callback_data=f"button_remove_event_number_{button}")
                                sample_button_remove_n_event_second = types.InlineKeyboardButton(text=emoji_digits_time[button+1], callback_data=f"button_remove_event_number_{button+1}")
                                keyboard_for_remove_buttons.add(sample_button_remove_n_event_first,sample_button_remove_n_event_second)
                        else:
                            for button in range(1,len(users_dict[str(message.chat.id)][1]["All_weather_events"])+1,2):
                                if button !=len(users_dict[str(message.chat.id)][1]["All_weather_events"]):
                                    sample_button_remove_n_event_first = types.InlineKeyboardButton(text=emoji_digits_time[button], callback_data=f"button_remove_event_number_{button}")
                                    sample_button_remove_n_event_second = types.InlineKeyboardButton(text=emoji_digits_time[button+1], callback_data=f"button_remove_event_number_{button+1}")
                                    keyboard_for_remove_buttons.add(sample_button_remove_n_event_first,sample_button_remove_n_event_second)
                                else:
                                    sample_button_remove_n_event_first = types.InlineKeyboardButton(text=emoji_digits_time[button], callback_data=f"button_remove_event_number_{button}")
                                    keyboard_for_remove_buttons.add(sample_button_remove_n_event_first)
                        bot.send_message(message.chat.id, message_holder, reply_markup=keyboard_for_remove_buttons)
                    else:
                        keyboard_for_schedule_forecast_functions= types.InlineKeyboardMarkup()
                        button_new_event_schedule_forecast = types.InlineKeyboardButton(text=translate_current_text("New event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🆕", callback_data="button_new_event_schedule_forecast")
                        keyboard_for_schedule_forecast_functions.add(button_new_event_schedule_forecast)
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_my_events_no_active_events"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("/new_forecast_event", "🆕"),  reply_markup=keyboard_for_schedule_forecast_functions)
                else:
                    message_about_restrictions(message)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) remove_event",ex)
        return
    
    
    @bot.message_handler(commands=["all_forecast_events"])
    def print_all_events(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if users_dict[str(message.chat.id)][0].premium:
                    if len(users_dict[str(message.chat.id)][1]["All_weather_events"])>0:
                        message_holder = str()
                        if users_dict[str(message.chat.id)][0].schedule_remove_event:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_remove_event_enter_digit"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(emoji_digits_time[len(users_dict[str(message.chat.id)][1]["All_weather_events"])], "🗑"))
                        else:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_my_events_list"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(emoji_digits_time[len(users_dict[str(message.chat.id)][1]["All_weather_events"])]))
                        for index, current_event in enumerate(users_dict[str(message.chat.id)][1]["All_weather_events"]):
                            # current_event = list(n.values())
                            current_event_msg = translate_current_text("\n{}\nLocation: {} {}\nTime: {} {}\n", lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(emoji_digits_time[index+1],current_event['Location'],"🏘", current_event['Time'], "⏳")
                            message_holder+=current_event_msg
                        if users_dict[str(message.chat.id)][0].schedule_remove_event:
                            return message_holder
                        else:
                            bot.send_message(message.chat.id, message_holder)
                    else:
                        keyboard_for_schedule_forecast_functions= types.InlineKeyboardMarkup()
                        button_new_event_schedule_forecast = types.InlineKeyboardButton(text=translate_current_text("New event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🆕", callback_data="button_new_event_schedule_forecast")
                        keyboard_for_schedule_forecast_functions.add(button_new_event_schedule_forecast)
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_my_events_no_active_events"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("/new_forecast_event", "🆕"),  reply_markup=keyboard_for_schedule_forecast_functions)
                else:
                    message_about_restrictions(message)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) print_all_events",ex)
        return
    
    @bot.message_handler(commands=["new_forecast_event"])
    def schedule_forecast_new_event(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if users_dict[str(message.chat.id)][0].premium:
                    # self.schedule_forecast_new_event_location
                    # location,region,handle_query,text
                    if len(users_dict[str(message.chat.id)][1]["All_weather_events"])<10:
                        if users_dict[str(message.chat.id)][0].schedule_active_event==False:
                            users_dict[str(message.chat.id)][0].schedule_forecast_new_event_location=True
                            users_dict[str(message.chat.id)][0].schedule_forecast_new_event_region=True
                            users_dict[str(message.chat.id)][0].schedule_region_flag=True
                            users_dict[str(message.chat.id)][0].schedule_active_event=True
                            keyboard_schedule_location_variants= types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
                            button_weather_location_schedule = types.KeyboardButton(text=translate_current_text("Send location",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 📍", request_location=True)
                            button_weather_region_schedule = types.KeyboardButton(text=translate_current_text("Region",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🗺")
                            keyboard_schedule_location_variants.add(button_weather_location_schedule)
                            keyboard_schedule_location_variants.add(button_weather_region_schedule)
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_new_event_start_message"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("⏲",emoji_digits_time[len(users_dict[str(message.chat.id)][1]["All_weather_events"])],emoji_digits_time[len(emoji_digits_time)-1], "🙃"), reply_markup=keyboard_schedule_location_variants)
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_new_event_method_location"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("📍","/region"))
                            pass
                        else:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_you_have_active_event"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🙃"))
                    else:
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_new_event_reached_maximum_count"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🔟","/remove_forecast_event", "/my_forecast_events"))
                else:
                    message_about_restrictions(message)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) schedule_forecast_new_event",ex)
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
        return

    def function_for_scheduling_weather_event_send_message(message,event):
        if users_dict[str(message.chat.id)][0].premium:
            bot.send_message(users_dict[str(message.chat.id)][0].chat_id,  translate_current_text(weather_main(event, method="manual"), lang_to = users_dict[str(message.chat.id)][0].lang, lang_from = "en"))
        else:
            return
        
        
    def scheduling_weather_event(message):
        try:
        # , method="scheduling"
            # global counter_schedule_location
            # global counter_for_scheduled_events
            event_removed=False
            for index,current_event in enumerate(users_dict[str(message.chat.id)][1]["All_weather_events"]):
                # users_dict[str(message.message.chat.id)][1]["All_weather_events"][len(users_dict[str(message.message.chat.id)][1]["All_weather_events"])-1]
                # event = list(current_event.values())
                # if method=="scheduling":
                if current_event["Scheduled"] == False and current_event["Time"]!=None:
                    if users_dict[str(message.chat.id)][0].weather_schedule_engine==None:
                        users_dict[str(message.chat.id)][0].weather_schedule_engine=schedule.Scheduler()

                    if weather_main(current_event, method="manual")!=False:
                        users_dict[str(message.chat.id)][0].weather_schedule_engine.every().day.at(str(current_event["Time"])+":00").do(function_for_scheduling_weather_event_send_message,message,current_event)
                        users_dict[str(message.chat.id)][1]["All_weather_events"][index]["Scheduled"]=True
                        users_dict[str(message.chat.id)][1]["All_weather_events"][index]["Schedule_job"]=users_dict[str(message.chat.id)][0].weather_schedule_engine.jobs[-1]
                    else:
                        del users_dict[str(message.chat.id)][1]["All_weather_events"][index]
                        raise Exception
                elif current_event["Time"]==None:
                    del users_dict[str(message.chat.id)][1]["All_weather_events"][index]
                    # raise Exception
                elif current_event["Remove"] == True:
                    event_removed = True
                    users_dict[str(message.chat.id)][0].schedule_remove_event_active=False
                    job = users_dict[str(message.chat.id)][0].weather_schedule_engine.jobs.pop(index)
                    users_dict[str(message.chat.id)][0].weather_schedule_engine.cancel_job(job)

                    # users_dict[str(message.chat.id)][0].weather_schedule_engine.clear(tag=str(users_dict[str(message.chat.id)][1]["All_weather_events"][index]))
                    del users_dict[str(message.chat.id)][1]["All_weather_events"][index]
                    if users_dict[str(message.chat.id)][1]["All_weather_events"]==[{}]:
                        users_dict[str(message.chat.id)][1]["All_weather_events"]=[]
                        # bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_remove_event_successfully"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👌"))
                        users_dict[str(message.chat.id)][0].weather_schedule_engine.clear()
                        users_dict[str(message.chat.id)][0].weather_schedule_engine=None
                        lambda users_dict:users_dict[str(message.chat.id)][0].weather_thread_engine.join()
                        users_dict[str(message.chat.id)][0].weather_thread_engine=None

            if users_dict[str(message.chat.id)][0].weather_thread_engine==None and users_dict[str(message.chat.id)][0].weather_schedule_engine!=None:
                def run_scheduler(scheduler):
                    while True:
                        scheduler.run_pending()
                        time.sleep(1)
                users_dict[str(message.chat.id)][0].weather_thread_engine = threading.Thread(target=run_scheduler, args=(users_dict[str(message.chat.id)][0].weather_schedule_engine,))
                users_dict[str(message.chat.id)][0].weather_thread_engine.start()
            # else:
            #     raise Exception

            if event_removed:
                bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_remove_event_successfully"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👌"))
            else:
                users_dict[str(message.chat.id)][0].schedule_active_event=False
                bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_new_event_congrats"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🎉", emoji_digits_time[len(users_dict[str(message.chat.id)][1]["All_weather_events"])], users_dict[str(message.chat.id)][1]["All_weather_events"][-1]["Location"],"🏘", users_dict[str(message.chat.id)][1]["All_weather_events"][-1]["Time"], "🗓"))

            sleep(1)
            scheduling_forecast(message)

            return True
        except Exception as ex:
            print("scheduling_weather_event",ex)
            raise Exception

    @bot.message_handler(commands=["weather"])
    def weather_main_function(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                bot.send_message(message.chat.id, translate_current_text("Only weather in Europe is possible at the moment", lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang)+" ❗️")
                sleep(1)
                if users_dict[str(message.chat.id)][0].premium:
                    keyboard_geo_upload = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
                    button_weather_location_premium = types.KeyboardButton(text=translate_current_text("Send location",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 📍", request_location=True)
                    button_weather_region_premium = types.KeyboardButton(text=translate_current_text("Region",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🗺")
                    button_weather_schedule_forecast_premium = types.KeyboardButton(text="/schedule_forecast"+" ⏰")
                    keyboard_geo_upload.add(button_weather_location_premium)
                    keyboard_geo_upload.add(button_weather_region_premium)
                    keyboard_geo_upload.add(button_weather_schedule_forecast_premium)

                    # keyboard_for_weather_premium = types.InlineKeyboardMarkup()
                    # button_weather_region_premium = types.InlineKeyboardButton(text=translate_current_text("Region",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🗺", callback_data="region_weather_premium")
                    # button_weather_schedule_forecast_premium = types.InlineKeyboardButton(text=translate_current_text("Schedule Weather",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ⏰", callback_data="schedule_forecast_weather_premium")
                    # # keyboard_for_weather_premium.add(button_weather_location_premium)
                    # keyboard_for_weather_premium.add(button_weather_region_premium)
                    # keyboard_for_weather_premium.add(button_weather_schedule_forecast_premium)
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Weather_start_message_premium_1_part"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang)+" 🌤")
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Weather_start_message_premium_2_part"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👇"),reply_markup=keyboard_geo_upload)
                    # bot.send_message(message.chat.id, translate_current_text(all_messages["Weather_start_message_premium_3_part"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("1️⃣","2️⃣","/region","3️⃣","/schedule_forecast"), reply_markup=keyboard_for_weather_premium)
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Weather_start_message_premium_3_part"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("1️⃣","2️⃣","/region","3️⃣","/schedule_forecast"))

                else:
                    keyboard_geo_upload_basic = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
                    button_weather_location_basic = types.KeyboardButton(text=translate_current_text("Send location",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 📍", request_location=True)
                    button_weather_region_basic = types.KeyboardButton(text=translate_current_text("Region",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🗺")
                    # button_weather_schedule_forecast_basic = types.KeyboardButton(text=translate_current_text("Schedule Weather",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ⏰🔒")
                    button_weather_schedule_forecast_basic = types.KeyboardButton(text="/schedule_forecast"+" ⏰🔒")

                    keyboard_geo_upload_basic.add(button_weather_location_basic)
                    keyboard_geo_upload_basic.add(button_weather_region_basic)
                    keyboard_geo_upload_basic.add(button_weather_schedule_forecast_basic)
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Weather_start_message_premium_1_part"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang)+" 🌤")
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Weather_start_message_premium_2_part"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👇"),reply_markup=keyboard_geo_upload_basic)
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Weather_start_message_premium_3_part"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("1️⃣","2️⃣","/region","3️⃣","/schedule_forecast"))
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) weather_main_function",ex)
        return

       
    @bot.message_handler(commands=["special_func_to_reboot_bot"])
    def special_func_to_reboot_bot(message):
        if int(users_dict[str(message.chat.id)][0].chat_id)==785767433:
            print("Bot has been restarted")
            bot.send_message(message.chat.id, text="Bot has been restarted")
            raise Exception
        # return

    @bot.message_handler(commands=["special_func_to_add_premium"])
    def special_func_to_reboot_bot(message):
        if int(users_dict[str(message.chat.id)][0].chat_id)==785767433:
            users_dict[str(message.chat.id)][0].admin_chat_premium=True
            bot.send_message(message.chat.id, text="Enter chat id: ")
            # raise Exception
    
    # @bot.message_handler(commands=["check_current_file_active_bot"])
    # def check_current_file_active_bot(message):
    #     bot.send_message(message.chat.id, text="oribot_main.py")
    #     return

    # planner functions
    @bot.message_handler(commands=["planner"])
    def planner_function_main(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                # if users_dict[str(message.chat.id)][0].premium:
                keyboard_for_planner_functions= types.InlineKeyboardMarkup()
                button_planner_recurring_event_schedule_forecast = types.InlineKeyboardButton(text=translate_current_text("Every day event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ♻️", callback_data="button_planner_every_day_event_schedule_forecast")
                button_planner_one_event_schedule_forecast = types.InlineKeyboardButton(text=translate_current_text("Specific event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🕟", callback_data="button_planner_one_event_schedule_forecast")
                keyboard_for_planner_functions.add(button_planner_recurring_event_schedule_forecast)
                keyboard_for_planner_functions.add(button_planner_one_event_schedule_forecast)
                bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_start_message_1_part"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang)+" 🔈")
                bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_start_message_2_part"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👇"))
                bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_start_message_3_part"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("1️⃣","/every_day_event","2️⃣","/specific_event"),reply_markup=keyboard_for_planner_functions)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) planner_function_main",ex)
        return
    
    @bot.message_handler(commands=["every_day_event"])
    def every_day_event(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                keyboard_for_planner_functions_every_day= types.InlineKeyboardMarkup()
                button_planner_new_event_schedule_planner_every_day = types.InlineKeyboardButton(text=translate_current_text("New event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🆕", callback_data="button_planner_new_event_schedule_planner_every_day")
                button_planner_remove_event_schedule_planner_every_day  = types.InlineKeyboardButton(text=translate_current_text("Remove event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🗑", callback_data="button_planner_remove_event_schedule_planner_every_day")
                button_planner_all_events_schedule_planner_every_day  = types.InlineKeyboardButton(text=translate_current_text("All events",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 📜", callback_data="button_planner_all_events_schedule_planner_every_day")

                keyboard_for_planner_functions_every_day.add(button_planner_new_event_schedule_planner_every_day)
                keyboard_for_planner_functions_every_day.add(button_planner_remove_event_schedule_planner_every_day)
                keyboard_for_planner_functions_every_day.add(button_planner_all_events_schedule_planner_every_day)

                if users_dict[str(message.chat.id)][0].premium:
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_every_day_events_start_message_premium"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("♻️", emoji_digits_time[len(users_dict[str(message.chat.id)][2]["All_every_day_events"])], "/new_every_day_event","🆕", "/remove_every_day_event","🗑", "/all_every_day_events","📜"), reply_markup=keyboard_for_planner_functions_every_day)
                else:
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_every_day_events_start_message_basic"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("♻️", emoji_digits_time[len(users_dict[str(message.chat.id)][2]["All_every_day_events"])], "/new_every_day_event","🆕", "/remove_every_day_event","🗑", "/all_every_day_events","📜"),reply_markup=keyboard_for_planner_functions_every_day,parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) every_day_event",ex)
        return
    
    @bot.message_handler(commands=["new_every_day_event"])
    def every_day_new_event(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if users_dict[str(message.chat.id)][0].planner_every_day_active_event==False:
                    if users_dict[str(message.chat.id)][0].premium:
                        if len(users_dict[str(message.chat.id)][2]["All_every_day_events"])<10:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_every_day_event_txt"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👉"))
                            users_dict[str(message.chat.id)][0].planner_every_day_txt_flag=True
                            users_dict[str(message.chat.id)][0].planner_every_day_active_event=True
                        else:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_max_num_specific_events"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("10","/remove_every_day_event", "🙁"))
                    else:
                        if len(users_dict[str(message.chat.id)][2]["All_every_day_events"])<5:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_every_day_event_txt"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👉"))
                            users_dict[str(message.chat.id)][0].planner_every_day_txt_flag=True
                            users_dict[str(message.chat.id)][0].planner_every_day_active_event=True
                        else:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_max_num_specific_events"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("5","/remove_every_day_event", "🙁"))
                            message_about_restrictions(message)
                else:
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_you_have_active_event"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🙃"))
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) every_day_new_event",ex)
        return

    @bot.message_handler(commands=["all_every_day_events"])
    def all_every_day_event(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if len(users_dict[str(message.chat.id)][2]["All_every_day_events"])>0:
                    message_holder = str()
                    if users_dict[str(message.chat.id)][0].planner_every_day_remove_event:
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_remove_event_enter_digit"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(emoji_digits_time[len(users_dict[str(message.chat.id)][2]["All_every_day_events"])], "🗑"))
                    else:
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_my_events_list"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(emoji_digits_time[len(users_dict[str(message.chat.id)][2]["All_every_day_events"])]))
                    for index, current_event in enumerate(users_dict[str(message.chat.id)][2]["All_every_day_events"]):
                        # current_event = list(n.values())
                        current_event_msg = translate_current_text("\n{}\nNotification: {} {}\nTime: {} {}\n", lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(emoji_digits_time[index+1],current_event['Text'],"📝", current_event['Time'], "⏳")
                        message_holder+=current_event_msg
                    if users_dict[str(message.chat.id)][0].planner_every_day_remove_event:
                        return message_holder
                    else:
                        bot.send_message(message.chat.id, message_holder)
                else:
                    keyboard_for_planner_forecast_functions= types.InlineKeyboardMarkup()
                    button_new_event_planner= types.InlineKeyboardButton(text=translate_current_text("New event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🆕", callback_data="button_new_event_planner")
                    keyboard_for_planner_forecast_functions.add(button_new_event_planner)
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_my_events_no_active_events"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("/new_every_day_event", "🆕"),  reply_markup=keyboard_for_planner_forecast_functions)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) all_every_day_event",ex)
        return
    
    @bot.message_handler(commands=["remove_every_day_event"])
    def remove_every_day_event(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if len(users_dict[str(message.chat.id)][2]["All_every_day_events"])>0:
                    users_dict[str(message.chat.id)][0].planner_every_day_event_remove_active=True
                    users_dict[str(message.chat.id)][0].planner_every_day_remove_event=True
                    message_holder = all_every_day_event(message)
                    users_dict[str(message.chat.id)][0].planner_every_day_remove_event=False
                    keyboard_for_remove_buttons_planner = types.InlineKeyboardMarkup()
                    if len(users_dict[str(message.chat.id)][2]["All_every_day_events"])%2==0:
                        for button in range(1,len(users_dict[str(message.chat.id)][2]["All_every_day_events"])+1,2):
                            sample_button_remove_n_event_first_planner_everyday = types.InlineKeyboardButton(text=emoji_digits_time[button], callback_data=f"button_remove_event_number_every_day_{button}")
                            sample_button_remove_n_event_second_planner_everyday = types.InlineKeyboardButton(text=emoji_digits_time[button+1], callback_data=f"button_remove_event_number_every_day_{button+1}")
                            keyboard_for_remove_buttons_planner.add(sample_button_remove_n_event_first_planner_everyday,sample_button_remove_n_event_second_planner_everyday)
                    else:
                        for button in range(1,len(users_dict[str(message.chat.id)][2]["All_every_day_events"])+1,2):
                            if button !=len(users_dict[str(message.chat.id)][2]["All_every_day_events"]):
                                sample_button_remove_n_event_first_planner_everyday = types.InlineKeyboardButton(text=emoji_digits_time[button], callback_data=f"button_remove_event_number_every_day_{button}")
                                sample_button_remove_n_event_second_planner_everyday = types.InlineKeyboardButton(text=emoji_digits_time[button+1], callback_data=f"button_remove_event_number_every_day_{button+1}")
                                keyboard_for_remove_buttons_planner.add(sample_button_remove_n_event_first,sample_button_remove_n_event_second_planner_everyday)
                            else:
                                sample_button_remove_n_event_first = types.InlineKeyboardButton(text=emoji_digits_time[button], callback_data=f"button_remove_event_number_every_day_{button}")
                                keyboard_for_remove_buttons_planner.add(sample_button_remove_n_event_first)
                    bot.send_message(message.chat.id, message_holder, reply_markup=keyboard_for_remove_buttons_planner)

                else:
                    keyboard_for_planner_forecast_functions= types.InlineKeyboardMarkup()
                    button_new_event_planner= types.InlineKeyboardButton(text=translate_current_text("New event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🆕", callback_data="button_new_event_planner")
                    keyboard_for_planner_forecast_functions.add(button_new_event_planner)
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_my_events_no_active_events"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("/new_every_day_event", "🆕"),  reply_markup=keyboard_for_planner_forecast_functions)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) remove_every_day_event",ex)
        return
    
    def scheduling_every_day_event(message):
        try:
            # All_every_day_events
            # global counter_schedule_every_day
            event_removed=False

            for index,current_event in enumerate(users_dict[str(message.chat.id)][2]["All_every_day_events"]):
                # users_dict[str(message.message.chat.id)][1]["All_weather_events"][len(users_dict[str(message.message.chat.id)][1]["All_weather_events"])-1]
                # event = list(current_event.values())
                if current_event["Scheduled"] == False and current_event["Time"]!=None:
                    if users_dict[str(message.chat.id)][0].planner_scheduler_engine==None:
                        users_dict[str(message.chat.id)][0].planner_scheduler_engine=schedule.Scheduler()
                    users_dict[str(message.chat.id)][0].planner_scheduler_engine.every().day.at(str(current_event["Time"])+":00").do(bot.send_message,users_dict[str(message.chat.id)][0].chat_id,translate_current_text("{} Daily notification from {} {}:", lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🚨","OriBot","🚨")+"\n\n"+current_event["Text"])
                    
                    users_dict[str(message.chat.id)][2]["All_every_day_events"][index]["Scheduled"]=True
                    users_dict[str(message.chat.id)][2]["All_every_day_events"][index]["Schedule_job"]=users_dict[str(message.chat.id)][0].planner_scheduler_engine.jobs[-1]
                elif current_event["Time"]==None:
                    del users_dict[str(message.chat.id)][2]["All_every_day_events"][index]
                    # raise Exception
                elif current_event["Remove"] == True:
                    users_dict[str(message.chat.id)][0].planner_every_day_event_remove_active=False
                    event_removed = True
                    job = users_dict[str(message.chat.id)][0].planner_scheduler_engine.jobs.pop(index)
                    users_dict[str(message.chat.id)][0].planner_scheduler_engine.cancel_job(job)

                    del users_dict[str(message.chat.id)][2]["All_every_day_events"][index]
                    if users_dict[str(message.chat.id)][2]["All_every_day_events"]==[{}]:
                        users_dict[str(message.chat.id)][2]["All_every_day_events"]=[]
                        users_dict[str(message.chat.id)][0].planner_scheduler_engine.clear()
                        users_dict[str(message.chat.id)][0].planner_scheduler_engine=None
                        lambda users_dict:users_dict[str(message.chat.id)][0].planner_thread_engine.join()
                        users_dict[str(message.chat.id)][0].planner_thread_engine=None

            if users_dict[str(message.chat.id)][0].planner_thread_engine==None and users_dict[str(message.chat.id)][0].planner_scheduler_engine!=None:
                def run_scheduler(scheduler):
                    while True:
                        scheduler.run_pending()
                        time.sleep(1)

                users_dict[str(message.chat.id)][0].planner_thread_engine = threading.Thread(target=run_scheduler, args=(users_dict[str(message.chat.id)][0].planner_scheduler_engine,))
                users_dict[str(message.chat.id)][0].planner_thread_engine.start()
                
            if event_removed:
                bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_remove_event_successfully"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👌"))
            else:
                users_dict[str(message.chat.id)][0].planner_every_day_active_event=False
                bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_new_event_congrats"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🎉", emoji_digits_time[len(users_dict[str(message.chat.id)][2]["All_every_day_events"])], users_dict[str(message.chat.id)][2]["All_every_day_events"][-1]["Text"],"💬", users_dict[str(message.chat.id)][2]["All_every_day_events"][-1]["Time"], "🗓"))
            sleep(1)
            every_day_event(message)
            
            return True
        except Exception as ex:
            print("scheduling_every_day_event",ex)
            raise Exception
    
    @bot.message_handler(commands=["specific_event"])
    def specific_event(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                keyboard_for_planner_functions_specific= types.InlineKeyboardMarkup()
                button_planner_new_event_schedule_planner_specific = types.InlineKeyboardButton(text=translate_current_text("New event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🆕", callback_data="button_planner_new_event_schedule_planner_specific")
                button_planner_remove_event_schedule_planner_specific  = types.InlineKeyboardButton(text=translate_current_text("Remove event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🗑", callback_data="button_planner_remove_event_schedule_planner_specific")
                button_planner_all_events_schedule_planner_specific  = types.InlineKeyboardButton(text=translate_current_text("All events",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 📜", callback_data="button_planner_all_events_schedule_planner_specific")

                keyboard_for_planner_functions_specific.add(button_planner_new_event_schedule_planner_specific)
                keyboard_for_planner_functions_specific.add(button_planner_remove_event_schedule_planner_specific)
                keyboard_for_planner_functions_specific.add(button_planner_all_events_schedule_planner_specific)

                if users_dict[str(message.chat.id)][0].premium:
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_specific_events_start_message_premium"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🕟", emoji_digits_time[len(users_dict[str(message.chat.id)][2]["All_specific_events"])], "/new_specific_event","🆕", "/remove_specific_event","🗑", "/all_specific_events","📜"), reply_markup=keyboard_for_planner_functions_specific)
                else:
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_specific_events_start_message_basic"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🕟", emoji_digits_time[len(users_dict[str(message.chat.id)][2]["All_specific_events"])], "/new_specific_event","🆕", "/remove_specific_event","🗑", "/all_specific_events","📜"),reply_markup=keyboard_for_planner_functions_specific)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) specific_event",ex)
        return
    
    @bot.message_handler(commands=["new_specific_event"])
    def specific_new_event(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if users_dict[str(message.chat.id)][0].planner_specific_event_active==False:
                    if users_dict[str(message.chat.id)][0].premium:
                        if len(users_dict[str(message.chat.id)][2]["All_specific_events"])<10:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_specific_event_txt"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👉"))
                            users_dict[str(message.chat.id)][0].planner_specific_event_txt_flag=True
                            users_dict[str(message.chat.id)][0].planner_specific_event_active=True
                        else:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_max_num_specific_events"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("10","/remove_specific_event", "🙁"))
                    else:
                        if len(users_dict[str(message.chat.id)][2]["All_specific_events"])<5:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_specific_event_txt"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👉"))
                            users_dict[str(message.chat.id)][0].planner_specific_event_txt_flag=True
                            users_dict[str(message.chat.id)][0].planner_specific_event_active=True
                        else:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_max_num_specific_events"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("5","/remove_specific_event", "🙁"))
                            message_about_restrictions(message)
                else:
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_you_have_active_event"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🙃"))
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) specific_new_event",ex)
        return
    
    @bot.message_handler(commands=["remove_specific_event"])
    def specific_remove_event(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                # All_specific_events
                if len(users_dict[str(message.chat.id)][2]["All_specific_events"])>0:

                    users_dict[str(message.chat.id)][0].planner_specific_event_remove_active=True
                    users_dict[str(message.chat.id)][0].planner_specific_event_remove_event=True
                    message_holder = specific_all_events(message)
                    users_dict[str(message.chat.id)][0].planner_specific_event_remove_event=False
                    keyboard_for_remove_buttons_planner_specific = types.InlineKeyboardMarkup()
                    if len(users_dict[str(message.chat.id)][2]["All_specific_events"])%2==0:
                        for button in range(1,len(users_dict[str(message.chat.id)][2]["All_specific_events"])+1,2):
                            sample_button_remove_n_event_first_planner_specific = types.InlineKeyboardButton(text=emoji_digits_time[button], callback_data=f"button_remove_event_number_specifik_{button}")
                            sample_button_remove_n_event_second_planner_specific = types.InlineKeyboardButton(text=emoji_digits_time[button+1], callback_data=f"button_remove_event_number_specifik_{button+1}")
                            keyboard_for_remove_buttons_planner_specific.add(sample_button_remove_n_event_first_planner_specific,sample_button_remove_n_event_second_planner_specific)
                    else:
                        for button in range(1,len(users_dict[str(message.chat.id)][2]["All_specific_events"])+1,2):
                            if button !=len(users_dict[str(message.chat.id)][2]["All_specific_events"]):
                                sample_button_remove_n_event_first_planner_specific = types.InlineKeyboardButton(text=emoji_digits_time[button], callback_data=f"button_remove_event_number_specifik_{button}")
                                sample_button_remove_n_event_second_planner_specific = types.InlineKeyboardButton(text=emoji_digits_time[button+1], callback_data=f"button_remove_event_number_specifik_{button+1}")
                                keyboard_for_remove_buttons_planner_specific.add(sample_button_remove_n_event_first_planner_specific,sample_button_remove_n_event_second_planner_specific)
                            else:
                                sample_button_remove_n_event_first_planner_specific = types.InlineKeyboardButton(text=emoji_digits_time[button], callback_data=f"button_remove_event_number_specifik_{button}")
                                keyboard_for_remove_buttons_planner_specific.add(sample_button_remove_n_event_first_planner_specific)
                    bot.send_message(message.chat.id, message_holder, reply_markup=keyboard_for_remove_buttons_planner_specific)

                else:
                    keyboard_for_planner_forecast_functions= types.InlineKeyboardMarkup()
                    button_new_event_planner= types.InlineKeyboardButton(text=translate_current_text("New event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🆕", callback_data="button_planner_new_event_schedule_planner_specific")
                    keyboard_for_planner_forecast_functions.add(button_new_event_planner)
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_my_events_no_active_events"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("/new_specific_event", "🆕"),  reply_markup=keyboard_for_planner_forecast_functions)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) specific_remove_event",ex)
        return

    @bot.message_handler(commands=["all_specific_events"])
    def specific_all_events(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if len(users_dict[str(message.chat.id)][2]["All_specific_events"])>0:
                    message_holder = str()
                    if users_dict[str(message.chat.id)][0].planner_specific_event_remove_event:
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_remove_event_enter_digit"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(emoji_digits_time[len(users_dict[str(message.chat.id)][2]["All_specific_events"])], "🗑"))
                    else:
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_my_events_list"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(emoji_digits_time[len(users_dict[str(message.chat.id)][2]["All_specific_events"])]))
                    for index, current_event in enumerate(users_dict[str(message.chat.id)][2]["All_specific_events"]):
                        # current_event = list(n.values())
                        current_event_msg = translate_current_text("\n{}\nNotification: {} {}\nTime: {} {}\nDate: {} {}\n", lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(emoji_digits_time[index+1],current_event['Text'],"📝", current_event['Time'], "⏳",current_event['Date_text'], "📅")
                        message_holder+=current_event_msg
                    if users_dict[str(message.chat.id)][0].planner_specific_event_remove_event:
                        return message_holder
                    else:
                        bot.send_message(message.chat.id, message_holder)
                else:
                    keyboard_for_planner_forecast_functions_specific= types.InlineKeyboardMarkup()
                    button_new_event_planner_specific= types.InlineKeyboardButton(text=translate_current_text("New event",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🆕", callback_data="button_planner_new_event_schedule_planner_specific")
                    keyboard_for_planner_forecast_functions_specific.add(button_new_event_planner_specific)
                    bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_my_events_no_active_events"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("/new_specific_event", "🆕"),  reply_markup=keyboard_for_planner_forecast_functions_specific)
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) specific_all_events",ex)
        return
    
    def job_that_executes_once(current_event:dict, index:int, message):
        global users_dict
        today = datetime.now().date()
        today_full_date = "-".join(["0"+str(n) if n<10 else str(n) for n in [today.day, today.month, today.year]])
        if current_event["Date"]==today_full_date:
            bot.send_message(users_dict[str(message.chat.id)][0].chat_id,translate_current_text("{} Notification from {} {}:", lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🚨","OriBot","🚨")+"\n\n"+current_event["Text"])
            job = users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine.jobs.pop(index)
            users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine.cancel_job(job)
            del users_dict[str(message.chat.id)][2]["All_specific_events"][index]
            if users_dict[str(message.chat.id)][2]["All_specific_events"]==[{}]:
                users_dict[str(message.chat.id)][2]["All_specific_events"]=[]
                users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine.clear()
                users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine=None
                lambda users_dict:users_dict[str(message.chat.id)][0].planner_specific_event_thread_engine.join()
                users_dict[str(message.chat.id)][0].planner_specific_event_thread_engine=None
            # return schedule.CancelJob
            return
        else:
            return
    
    def scheduling_specific_event(message):
        try:
            # All_specific_events
            # global counter_schedule_every_day
            event_removed=False

            for index,current_event in enumerate(users_dict[str(message.chat.id)][2]["All_specific_events"]):
                # users_dict[str(message.message.chat.id)][1]["All_weather_events"][len(users_dict[str(message.message.chat.id)][1]["All_weather_events"])-1]
                # event = list(current_event.values())
                if current_event["Scheduled"] == False and current_event["Time"]!=None:
                    if users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine==None:
                        users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine=schedule.Scheduler()
                    users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine.every().day.at(str(current_event["Time"])+":00").do(job_that_executes_once, current_event, index, message)
                    
                    users_dict[str(message.chat.id)][2]["All_specific_events"][index]["Scheduled"]=True
                    users_dict[str(message.chat.id)][2]["All_specific_events"][index]["Schedule_job"]=users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine.jobs[-1]
                elif current_event["Time"]==None:
                    del users_dict[str(message.chat.id)][2]["All_specific_events"][index]
                    # raise Exception
                elif current_event["Remove"] == True:
                    users_dict[str(message.chat.id)][0].planner_specific_event_remove_active=False
                    event_removed = True
                    job = users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine.jobs.pop(index)
                    users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine.cancel_job(job)

                    del users_dict[str(message.chat.id)][2]["All_specific_events"][index]
                    if users_dict[str(message.chat.id)][2]["All_specific_events"]==[{}]:
                        users_dict[str(message.chat.id)][2]["All_specific_events"]=[]
                        users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine.clear()
                        users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine=None
                        lambda users_dict:users_dict[str(message.chat.id)][0].planner_specific_event_thread_engine.join()
                        users_dict[str(message.chat.id)][0].planner_specific_event_thread_engine=None

            if users_dict[str(message.chat.id)][0].planner_specific_event_thread_engine==None and users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine!=None:
                def run_scheduler(scheduler):
                    while True:
                        scheduler.run_pending()
                        time.sleep(1)

                users_dict[str(message.chat.id)][0].planner_specific_event_thread_engine = threading.Thread(target=run_scheduler, args=(users_dict[str(message.chat.id)][0].planner_specific_event_schedule_engine,))
                users_dict[str(message.chat.id)][0].planner_specific_event_thread_engine.start()
                
            if event_removed:
                bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_remove_event_successfully"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👌"))
            else:
                users_dict[str(message.chat.id)][0].planner_specific_event_active=False
                bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_specific_new_event_congrats"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🎉", emoji_digits_time[len(users_dict[str(message.chat.id)][2]["All_specific_events"])], users_dict[str(message.chat.id)][2]["All_specific_events"][-1]["Text"],"💬",users_dict[str(message.chat.id)][2]["All_specific_events"][-1]["Date_text"],"📅", users_dict[str(message.chat.id)][2]["All_specific_events"][-1]["Time"], "🕟"))
            sleep(1)
            specific_event(message)
            return True
        except Exception as ex:
            print("scheduling_specific_event",ex)
            raise Exception

    # text processing functions
    @bot.message_handler(content_types=["text"])
    def send_text(message):
        try:
            if users_dict[str(message.chat.id)][0].activated_bot:
                if str(message.chat.id) in users_dict.keys():
                    # language
                    if users_dict[str(message.chat.id)][0].change_lang==True and "/" not in message.text:
                        status_detect, status_upd = detect_lang_func(message=message), update_user(users_dict[str(message.chat.id)][0]) 
                        print(users_dict[str(message.chat.id)][0].info())
                        if status_detect == True and status_upd == True:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Language_successful"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👍"))
                            bot.send_message(message.chat.id, translate_current_text(all_messages["If_want_set_lang"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("/change_lang", "🚩"))
                            users_dict[str(message.chat.id)][0].change_lang=False
                            update_user(users_dict[str(message.chat.id)][0]) 
                            #     # message_about_plans(message)
                            # else:
                            #     bot.send_message(message.chat.id, translate_current_text(all_messages["Something_went_wrong"], lang_from="en", lang_to=users_dict[str(message.chat.id)].lang).format("@oribot_support_bot"))
                            message_about_plans(message)
                    # weather
                    elif translate_current_text(message.text, lang_from=users_dict[str(message.chat.id)][0].lang, lang_to="en").lower() in ["Region","region","Region🗺", "region🗺","Region 🗺","region 🗺", "regions🗺","regions 🗺"]:
                        bot.send_message(message.chat.id, translate_current_text(all_messages["Region_start_message"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang)+" 🌐:")
                        if users_dict[str(message.chat.id)][0].schedule_forecast_new_event_region:
                            users_dict[str(message.chat.id)][0].schedule_forecast_new_event_location=False
                        else:
                            users_dict[str(message.chat.id)][0].manual_region=True
                    elif users_dict[str(message.chat.id)][0].manual_region==True or users_dict[str(message.chat.id)][0].schedule_forecast_new_event_region==True:
                        response_location_manual = from_location_to_coordinates(message.text)
                        # users_dict[str(message.chat.id)][0].manual_region=False
                        if users_dict[str(message.chat.id)][0].manual_region:
                            if response_location_manual!=False:
                                users_dict[str(message.chat.id)][0].manual_region=False
                                users_dict[str(message.chat.id)][0].lat=response_location_manual[0]
                                users_dict[str(message.chat.id)][0].long=response_location_manual[1]
                                users_dict[str(message.chat.id)][0].location=response_location_manual[2]
                                update_user(users_dict[str(message.chat.id)][0]) 
                                # users_dict[str(message.chat.id)][0].manual_region
                                keyboard_location_y_n = types.InlineKeyboardMarkup()
                                button_location_y = types.InlineKeyboardButton(text=translate_current_text("Yes ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_location_y")
                                button_location_n = types.InlineKeyboardButton(text=translate_current_text("No ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_location_n")
                                keyboard_location_y_n.add(button_location_y, button_location_n)
                                bot.send_message(message.chat.id, translate_current_text(all_messages["Check_manual_location"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(users_dict[str(message.chat.id)][0].location), reply_markup=keyboard_location_y_n)
                            else:
                                keyboard_region = types.InlineKeyboardMarkup()
                                button_weather_region = types.InlineKeyboardButton(text=translate_current_text("Region",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🗺", callback_data="button_weather_region")
                                keyboard_region.add(button_weather_region)
                                bot.send_message(message.chat.id, translate_current_text(all_messages["Location_incorrect"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🧐","/region"), reply_markup=keyboard_region)
                        else:
                            if len(users_dict[str(message.chat.id)][1]["All_weather_events"])<10:
                                if response_location_manual!=False:
                                    if users_dict[str(message.chat.id)][0].schedule_active_event or users_dict[str(message.chat.id)][0].schedule_active_event_change_location:
                                        if  users_dict[str(message.chat.id)][0].schedule_active_event and users_dict[str(message.chat.id)][0].schedule_active_event_change_location==False:
                                            users_dict[str(message.chat.id)][1]["All_weather_events"].append(
                                                    
                                                    {
                                                    "Lat":response_location_manual[0],
                                                    "Long":response_location_manual[1],
                                                    "Location":response_location_manual[2],
                                                    "Time":None,
                                                    "Remove":False,
                                                    "Scheduled":False,
                                                    "Schedule_job":None,
                                                    "Lang":users_dict[str(message.chat.id)][0].lang
                                                    }
                                                )
                                        elif users_dict[str(message.chat.id)][0].schedule_active_event_change_location:
                                            users_dict[str(message.chat.id)][1]["All_weather_events"][-1]={
                                                    
                                                    "Lat":response_location_manual[0],
                                                    "Long":response_location_manual[1],
                                                    "Location":response_location_manual[2],
                                                    "Time":None,
                                                    "Remove":False,
                                                    "Scheduled":False,
                                                    "Schedule_job":None,
                                                    "Lang":users_dict[str(message.chat.id)][0].lang
                                                    
                                                }
                                        users_dict[str(message.chat.id)][0].schedule_active_event_change_location=False
                                        # users_dict[str(message.chat.id)][0].schedule_active_event=False
                                    users_dict[str(message.chat.id)][0].schedule_forecast_new_event_region=False
                                    users_dict[str(message.chat.id)][0].schedule_region_flag=False
                                    keyboard_location_y_n = types.InlineKeyboardMarkup()
                                    button_location_y = types.InlineKeyboardButton(text=translate_current_text("Yes ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_location_y_schedule")
                                    button_location_n = types.InlineKeyboardButton(text=translate_current_text("No ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_location_n_schedule")
                                    keyboard_location_y_n.add(button_location_y, button_location_n)
                                    bot.send_message(message.chat.id, translate_current_text(all_messages["Check_manual_location"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(users_dict[str(message.chat.id)][1]["All_weather_events"][-1]["Location"]), reply_markup=keyboard_location_y_n)
                                else:
                                    keyboard_region = types.InlineKeyboardMarkup()
                                    button_weather_region = types.InlineKeyboardButton(text=translate_current_text("Region",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🗺", callback_data="button_weather_region")
                                    keyboard_region.add(button_weather_region)
                                    bot.send_message(message.chat.id, translate_current_text(all_messages["Location_incorrect"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🧐","/region"), reply_markup=keyboard_region)
                            else:
                                    bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_forecast_new_event_reached_maximum_count"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("1️⃣0️⃣","/remove_forecast_event", "/all_forecast_events"))
                                    users_dict[str(message.chat.id)][0].schedule_forecast_new_event_region=False
                                    users_dict[str(message.chat.id)][0].schedule_region_flag=False
                    elif users_dict[str(message.chat.id)][0].schedule_forecast_new_event_time:
                        try:
                            splitted_time = message.text.split(":")
                            if (0<=int(splitted_time[0])<=23 and splitted_time[1]=="00")or(0<=int(splitted_time[0])<=23 and 0<=int(splitted_time[1])<=59) or (splitted_time[0]=="00" and splitted_time[1]=="00") or (0<=int(splitted_time[1])<=59 and splitted_time[0]=="00"):
                                if int(splitted_time[0]) <10 and splitted_time[0]!="00":
                                    splitted_time[0]="0"+splitted_time[0]
                                users_dict[str(message.chat.id)][0].schedule_forecast_new_event_time=False

                                users_dict[str(message.chat.id)][1]["All_weather_events"][len(users_dict[str(message.chat.id)][1]["All_weather_events"])-1]["Time"]=":".join(splitted_time)
                                keyboard_schedule_weather_y_n = types.InlineKeyboardMarkup()
                                button_schedule_weather_y = types.InlineKeyboardButton(text=translate_current_text("Yes ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_schedule_weather_y")
                                button_schedule_weather_n = types.InlineKeyboardButton(text=translate_current_text("No ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_schedule_weather_n")
                                keyboard_schedule_weather_y_n.add(button_schedule_weather_y, button_schedule_weather_n)
                                bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_new_event_question_y_n"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(emoji_digits_time[len(users_dict[str(message.chat.id)][1]["All_weather_events"])], users_dict[str(message.chat.id)][1]["All_weather_events"][len(users_dict[str(message.chat.id)][1]["All_weather_events"])-1]["Location"], "🏘", str(users_dict[str(message.chat.id)][1]["All_weather_events"][len(users_dict[str(message.chat.id)][1]["All_weather_events"])-1]["Time"]), "⏳"), reply_markup=keyboard_schedule_weather_y_n)
                                    # create_weather_events
                                    # create_event(scheduled_events_dict["All Events"][len(scheduled_events_dict["All Events"])-1][str(len(scheduled_events_dict["All Events"]))])
                                    # 
                            else:
                                bot.send_message(message.chat.id,  translate_current_text(all_messages["Schedule_new_event_time_format"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("⌛️"))
                        except Exception as ex:
                            bot.send_message(message.chat.id,  translate_current_text(all_messages["Schedule_new_event_input_format"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("⌛️"))
                    
                    # planner
                    elif users_dict[str(message.chat.id)][0].planner_every_day_txt_flag:
                        if len(list(message.text))<500:
                            if users_dict[str(message.chat.id)][0].planner_every_day_active_event==True and users_dict[str(message.chat.id)][0].planner_every_day_event_change_txt==False:
                                users_dict[str(message.chat.id)][2]["All_every_day_events"].append(
                                                            
                                                            {
                                                            "Text":message.text,
                                                            "Time":None,
                                                            "Remove":False,
                                                            "Scheduled":False,
                                                            "Schedule_job":None,
                                                            "Lang":users_dict[str(message.chat.id)][0].lang
                                                            }
                                                        )
                            elif users_dict[str(message.chat.id)][0].planner_every_day_event_change_txt:
                                users_dict[str(message.chat.id)][2]["All_every_day_events"][-1]={

                                                                "Text":message.text,
                                                                "Time":None,
                                                                "Remove":False,
                                                                "Scheduled":False,
                                                                "Schedule_job":None,
                                                                "Lang":users_dict[str(message.chat.id)][0].lang
                                                            }
                                                            
                            users_dict[str(message.chat.id)][0].planner_every_day_event_change_txt=False
                            keyboard_every_day_event_y_n = types.InlineKeyboardMarkup()
                            button_every_day_event_y = types.InlineKeyboardButton(text=translate_current_text("Yes ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_every_day_event_y")
                            button_every_day_event_n = types.InlineKeyboardButton(text=translate_current_text("No ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_every_day_event_n")
                            keyboard_every_day_event_y_n.add(button_every_day_event_y, button_every_day_event_n)
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_every_day_event_check_notification"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(users_dict[str(message.chat.id)][2]["All_every_day_events"][-1]["Text"]), reply_markup=keyboard_every_day_event_y_n)
                        else:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_every_day_event_maximum_symbols_text"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👉"))
                    
                    elif users_dict[str(message.chat.id)][0].planner_every_day_event_get_time:
                        try:
                            splitted_time = message.text.split(":")
                            if (0<=int(splitted_time[0])<=23 and splitted_time[1]=="00")or(0<=int(splitted_time[0])<=23 and 0<=int(splitted_time[1])<=59) or (splitted_time[0]=="00" and splitted_time[1]=="00") or (0<=int(splitted_time[1])<=59 and splitted_time[0]=="00"):
                                if int(splitted_time[0]) <10 and splitted_time[0]!="00":
                                    splitted_time[0]="0"+splitted_time[0]
                                users_dict[str(message.chat.id)][0].planner_every_day_event_get_time=False

                                users_dict[str(message.chat.id)][2]["All_every_day_events"][len(users_dict[str(message.chat.id)][2]["All_every_day_events"])-1]["Time"]=":".join(splitted_time)
                                keyboard_schedule_every_day_planner_y_n = types.InlineKeyboardMarkup()
                                button_schedule_every_day_planner_y = types.InlineKeyboardButton(text=translate_current_text("Yes ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_schedule_every_day_planner_y")
                                button_schedule_every_day_planner_n = types.InlineKeyboardButton(text=translate_current_text("No ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_schedule_every_day_planner_n")
                                keyboard_schedule_every_day_planner_y_n.add(button_schedule_every_day_planner_y, button_schedule_every_day_planner_n)
                                bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_every_day_new_event_question_y_n"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(emoji_digits_time[len(users_dict[str(message.chat.id)][2]["All_every_day_events"])], users_dict[str(message.chat.id)][2]["All_every_day_events"][len(users_dict[str(message.chat.id)][2]["All_every_day_events"])-1]["Text"], "📝", str(users_dict[str(message.chat.id)][2]["All_every_day_events"][len(users_dict[str(message.chat.id)][2]["All_every_day_events"])-1]["Time"]), "⏳"), reply_markup=keyboard_schedule_every_day_planner_y_n)
                                    # create_weather_events
                                    # create_event(scheduled_events_dict["All Events"][len(scheduled_events_dict["All Events"])-1][str(len(scheduled_events_dict["All Events"]))])
                                    # 
                            else:
                                bot.send_message(message.chat.id,  translate_current_text(all_messages["Schedule_new_event_time_format"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("⌛️"))
                        except Exception as ex:
                            bot.send_message(message.chat.id,  translate_current_text(all_messages["Schedule_new_event_input_format"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("⌛️"))
                    elif users_dict[str(message.chat.id)][0].planner_specific_event_txt_flag:
                        if len(list(message.text))<500:
                            if users_dict[str(message.chat.id)][0].planner_specific_event_active==True and users_dict[str(message.chat.id)][0].planner_specific_event_change_txt==False:
                                users_dict[str(message.chat.id)][2]["All_specific_events"].append(
                                                            {
                                                            
                                                            "Text":message.text,
                                                            "Time":None,
                                                            "Remove":False,
                                                            "Scheduled":False,
                                                            "Schedule_job":None,
                                                            "Lang":users_dict[str(message.chat.id)][0].lang,
                                                            "Repeat":False,
                                                            "Date":None,
                                                            "Date_text":None,
                                                            "Date_datetime":None,
                                                            
                                                        })
                            elif users_dict[str(message.chat.id)][0].planner_specific_event_change_txt:
                                users_dict[str(message.chat.id)][2]["All_specific_events"][-1]={
                                                            
                                                                "Text":message.text,
                                                                "Time":None,
                                                                "Remove":False,
                                                                "Scheduled":False,
                                                                "Schedule_job":None,
                                                                "Lang":users_dict[str(message.chat.id)][0].lang,
                                                                "Repeat":False,
                                                                "Date":None,
                                                                "Date_text":None,
                                                                "Date_datetime":None,
                                                            
                                                            }
                            users_dict[str(message.chat.id)][0].planner_specific_event_change_txt=False
                            keyboard_specific_event_y_n = types.InlineKeyboardMarkup()
                            button_specific_event_y = types.InlineKeyboardButton(text=translate_current_text("Yes ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_specific_event_y")
                            button_specific_event_n = types.InlineKeyboardButton(text=translate_current_text("No ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_specific_event_n")
                            keyboard_specific_event_y_n.add(button_specific_event_y, button_specific_event_n)
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_specific_event_check_notification"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(users_dict[str(message.chat.id)][2]["All_specific_events"][-1]["Text"]), reply_markup=keyboard_specific_event_y_n)
                        else:
                            bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_every_day_event_maximum_symbols_text"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👉"))
                    elif users_dict[str(message.chat.id)][0].planner_specific_event_get_date:
                        # All_specific_events
                        try:
                            splitted_date=message.text.split(".")
                            datetime_object_specific = datetime.strptime(message.text, '%d.%m.%Y')
                            if (0<int(splitted_date[0])<=31 and int(splitted_date[1]) in [1,3,5,7,8,10,12] and int(splitted_date[2])<2050)or(0<int(splitted_date[0])<=30 and int(splitted_date[1]) in [4,6,9,11] and int(splitted_date[2])<2050)or(0<int(splitted_date[0])<=29 and int(splitted_date[1]) in [2] and int(splitted_date[2])<2050):
                                if datetime_object_specific.date()>=datetime.now().date():
                                    if int(splitted_date[1])==2:
                                        if int(splitted_date[2]) % 4==0 and (int(splitted_date[2])%100!=0 or int(splitted_date[2])%400==0):
                                            if 0<int(splitted_date[0])<=29:
                                                pass
                                            else:
                                                raise Exception
                                        else:
                                            if 0<int(splitted_date[0])<=28:
                                                pass
                                            else:
                                                raise Exception
                                    splitted_date=["0"+str(n) if int("".join([i for i in n if i.isdigit() and i!="0"]))<10 and n[0]!="0" else n for n in splitted_date]
                                    users_dict[str(message.chat.id)][0].planner_specific_event_get_date=False
                                    users_dict[str(message.chat.id)][2]["All_specific_events"][len(users_dict[str(message.chat.id)][2]["All_specific_events"])-1]["Date"]="-".join(splitted_date)
                                    users_dict[str(message.chat.id)][2]["All_specific_events"][len(users_dict[str(message.chat.id)][2]["All_specific_events"])-1]["Date_text"]=".".join(splitted_date)
                                    users_dict[str(message.chat.id)][2]["All_specific_events"][len(users_dict[str(message.chat.id)][2]["All_specific_events"])-1]["Date_datetime"]=datetime.strptime(message.text, '%d.%m.%Y').date()
                                    keyboard_schedule_specific_date_planner_y_n = types.InlineKeyboardMarkup()
                                    button_schedule_specific_date_planner_y = types.InlineKeyboardButton(text=translate_current_text("Yes ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_schedule_specific_date_planner_y")
                                    button_schedule_specific_date_planner_n = types.InlineKeyboardButton(text=translate_current_text("No ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_schedule_specific_date_planner_n")
                                    keyboard_schedule_specific_date_planner_y_n.add(button_schedule_specific_date_planner_y, button_schedule_specific_date_planner_n)
                                    bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_specific_date_event_question_y_n"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(".".join(splitted_date)), reply_markup=keyboard_schedule_specific_date_planner_y_n)
                                else:
                                    bot.send_message(message.chat.id,  translate_current_text(all_messages["Planner_specific_date_false"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👉"))
                            else:
                                bot.send_message(message.chat.id,  translate_current_text(all_messages["Planner_specific_date_format"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("dd.mm.yyyy", "📅"))
                        except Exception as ex:
                            print(ex)
                            bot.send_message(message.chat.id,  translate_current_text(all_messages["Planner_specific_date_input_format"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(datetime.now().date().strftime('%d.%m.%Y'),"📅"))
                    elif users_dict[str(message.chat.id)][0].planner_specific_event_get_time:
                        try:
                            splitted_time = message.text.split(":")
                            if (0<=int(splitted_time[0])<=23 and splitted_time[1]=="00")or(0<=int(splitted_time[0])<=23 and 0<=int(splitted_time[1])<=59) or (splitted_time[0]=="00" and splitted_time[1]=="00") or (0<=int(splitted_time[1])<=59 and splitted_time[0]=="00"):
                                if int(splitted_time[0]) <10 and splitted_time[0]!="00":
                                    splitted_time[0]="0"+splitted_time[0]
                                if users_dict[str(message.chat.id)][2]["All_specific_events"][len(users_dict[str(message.chat.id)][2]["All_specific_events"])-1]["Date_datetime"]==datetime.now().date():
                                    if int(splitted_time[0])>=int(datetime.now().hour) and int(splitted_time[1])>int(datetime.now().minute):
                                        users_dict[str(message.chat.id)][0].planner_specific_event_get_time=False
                                        users_dict[str(message.chat.id)][2]["All_specific_events"][len(users_dict[str(message.chat.id)][2]["All_specific_events"])-1]["Time"]=":".join(splitted_time)
                                        keyboard_schedule_specific_time_planner_y_n = types.InlineKeyboardMarkup()
                                        button_schedule_specific_time_planner_y = types.InlineKeyboardButton(text=translate_current_text("Yes ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_schedule_specific_time_planner_y")
                                        button_schedule_specific_time_planner_n = types.InlineKeyboardButton(text=translate_current_text("No ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_schedule_specific_time_planner_n")
                                        keyboard_schedule_specific_time_planner_y_n.add(button_schedule_specific_time_planner_y, button_schedule_specific_time_planner_n)
                                        bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_specific_time_event_question_y_n"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(message.text), reply_markup=keyboard_schedule_specific_time_planner_y_n)
                                    else:
                                        bot.send_message(message.chat.id,  translate_current_text(all_messages["Planner_specific_time_false"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👉"))
                                else:
                                    users_dict[str(message.chat.id)][0].planner_specific_event_get_time=False
                                    users_dict[str(message.chat.id)][2]["All_specific_events"][len(users_dict[str(message.chat.id)][2]["All_specific_events"])-1]["Time"]=":".join(splitted_time)
                                    keyboard_schedule_specific_time_planner_y_n = types.InlineKeyboardMarkup()
                                    button_schedule_specific_time_planner_y = types.InlineKeyboardButton(text=translate_current_text("Yes ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_schedule_specific_time_planner_y")
                                    button_schedule_specific_time_planner_n = types.InlineKeyboardButton(text=translate_current_text("No ",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_schedule_specific_time_planner_n")
                                    keyboard_schedule_specific_time_planner_y_n.add(button_schedule_specific_time_planner_y, button_schedule_specific_time_planner_n)
                                    bot.send_message(message.chat.id, translate_current_text(all_messages["Planner_specific_time_event_question_y_n"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format(message.text), reply_markup=keyboard_schedule_specific_time_planner_y_n)
                            else:
                                bot.send_message(message.chat.id,  translate_current_text(all_messages["Schedule_new_event_time_format"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("⌛️"))
                        except Exception as ex:
                            print(ex)
                            bot.send_message(message.chat.id,  translate_current_text(all_messages["Schedule_new_event_input_format"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("⌛️"))            
                    elif users_dict[str(message.chat.id)][0].get_promo_code:
                        # try:
                            try:
                                splitted_message=[n.upper() for n in message.text.split()]
                                if "".join(splitted_message) in promo_codes_list:
                                    print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) has used promo code")
                                    users_dict[str(message.chat.id)][0].premium=True
                                    users_dict[str(message.chat.id)][0].promo_code_expiring_date = [(datetime.now()+timedelta(days=3)).strftime('%d.%m.%Y'), (datetime.now()+timedelta(days=3)).strftime('%H:%M')]
                                    users_dict[str(message.chat.id)][0].promo_code_date_activated_account = [datetime.now().strftime('%d.%m.%Y'), datetime.now().strftime('%H:%M')]
                                    users_dict[str(message.chat.id)][4]["Promo_code"][0] = {
                                        "Activation_date":users_dict[str(message.chat.id)][0].promo_code_date_activated_account,
                                        "Expiring_date":users_dict[str(message.chat.id)][0].promo_code_expiring_date[0],
                                        # "Expiring_date":"25.04.2023",
                                        # "Expiring_time":"13:52",
                                        "Expiring_time":users_dict[str(message.chat.id)][0].promo_code_expiring_date[1],
                                        "Active":True,
                                    }
                                    print(users_dict[str(message.chat.id)][4]["Promo_code"][0])
                                    update_user(users_dict[str(message.chat.id)][0])
                                    promo_code_premium_control(message)
                                    users_dict[str(message.chat.id)][0].get_promo_code=False
                                    sending_animation_bot_working(message, type_gif="Congrats")
                                    sleep(1)
                                    bot.send_message(message.chat.id, translate_current_text(all_messages["Promo_code_successful"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🎉","🚀"))
                                    sleep(2)
                                    keyboard_for_premium_available_commands = types.InlineKeyboardMarkup()
                                    button_premium_weather = types.InlineKeyboardButton(text=translate_current_text("Weather",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ⛅️", callback_data="available_commands_premium_weather")
                                    button_premium_planner = types.InlineKeyboardButton(text=translate_current_text("Planner",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 📔", callback_data="available_commands_planner")
                                    # button_premium_news = types.InlineKeyboardButton(text=translate_current_text("News",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" 🗞", callback_data="available_commands_premium_news")
                                    keyboard_for_premium_available_commands.add(button_premium_weather)
                                    keyboard_for_premium_available_commands.add(button_premium_planner)
                                    # keyboard_for_premium_available_commands.add(button_premium_news)
                                    # testing_command(message)
                                    bot.send_message(message.chat.id, translate_current_text(all_messages["Available_commands_premium"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("🔓","👇","/weather","/planner","❔", users_dict[str(message.chat.id)][0].promo_code_expiring_date[0]), reply_markup=keyboard_for_premium_available_commands, parse_mode='HTML')
                                    
                                else:
                                    sending_animation_bot_working(message, type_gif="Smth_went_wrong")
                                    bot.send_message(message.chat.id,  translate_current_text(all_messages["Promo_code_incorrect"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("😕"))
                                    sleep(1)   
                                    users_dict[str(message.chat.id)][0].promo_code_activasion=True
                                    keyboard_for_basic_available_commands = types.InlineKeyboardMarkup()
                                    button_promo_code = types.InlineKeyboardButton(text=translate_current_text("Promo code",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 🏷", callback_data="promo_code")
                                    button_buy_premium_basic = types.InlineKeyboardButton(text=translate_current_text("Premium",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ⭐️", callback_data="buy_premium")
                                    button_basic_weather=types.InlineKeyboardButton(text=translate_current_text("Weather",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" ⛅️", callback_data="available_commands_basic_weather")
                                    button_basic_planner = types.InlineKeyboardButton(text=translate_current_text("Planner",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en")+" 📔", callback_data="available_commands_planner")
                                    # button_basic_news = types.InlineKeyboardButton(text=translate_current_text("News",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" 🗞", callback_data="available_commands_basic_news")
                                    keyboard_for_basic_available_commands.add(button_buy_premium_basic)
                                    keyboard_for_basic_available_commands.add(button_promo_code)
                                    keyboard_for_basic_available_commands.add(button_basic_weather)
                                    keyboard_for_basic_available_commands.add(button_basic_planner)
                                    # keyboard_for_basic_available_commands.add(button_basic_news)
                                    bot.send_message(message.chat.id, translate_current_text(all_messages["Available_commands_basic"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("😀","👇","/weather","/planner", "❔","⭐️"), reply_markup=keyboard_for_basic_available_commands)
                            except Exception as ex:
                                print(ex)
                                bot.send_message(message.chat.id,  translate_current_text(all_messages["Promo_code_input_faill"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("👉"))            

                        # except Exception as ex:
                        #     print(ex)
                        #     bot.send_message(message.chat.id, translate_current_text(all_messages["Schedule_smth_went_wrong"], lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang).format("@oribot_support_bot", "🥴"))
                    elif users_dict[str(message.chat.id)][0].admin_chat_premium:
                        users_dict[str(message.chat.id)][0].admin_chat_premium=False
                        chat_id_to_upg = str(message.text)
                        if  users_dict[chat_id_to_upg][0].premium!=True:
                            print(message.text)
                            users_dict[chat_id_to_upg][0].premium=True
                            users_dict[chat_id_to_upg][0].premium_expiring_date = [(datetime.now()+timedelta(days=30)).strftime('%d.%m.%Y'), (datetime.now()+timedelta(days=30)).strftime('%H:%M')]
                            users_dict[chat_id_to_upg][0].date_activated_account = [datetime.now().strftime('%d.%m.%Y'), datetime.now().strftime('%H:%M')]
                            users_dict[chat_id_to_upg][3]["Premium"][0] = {
                                "Activation_date":users_dict[chat_id_to_upg][0].date_activated_account,
                                "Expiring_date":users_dict[chat_id_to_upg][0].premium_expiring_date[0],
                                "Expiring_time":users_dict[chat_id_to_upg][0].premium_expiring_date[1],
                                "Active":True,
                            }

                            update_user(users_dict[chat_id_to_upg][0])
                            premium_control(chat_id_to_upg)
                            
                            sending_animation_bot_working(chat_id_to_upg, type_gif="Congrats")
                            sleep(1)
                            keyboard_for_premium_available_commands = types.InlineKeyboardMarkup()
                            button_premium_weather = types.InlineKeyboardButton(text=translate_current_text("Weather",lang_to=users_dict[chat_id_to_upg][0].lang, lang_from="en")+" ⛅️", callback_data="available_commands_premium_weather")
                            button_premium_planner = types.InlineKeyboardButton(text=translate_current_text("Planner",lang_to=users_dict[chat_id_to_upg][0].lang, lang_from="en")+" 📔", callback_data="available_commands_planner")
                            # button_premium_news = types.InlineKeyboardButton(text=translate_current_text("News",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" 🗞", callback_data="available_commands_premium_news")
                            keyboard_for_premium_available_commands.add(button_premium_weather)
                            keyboard_for_premium_available_commands.add(button_premium_planner)
                            bot.send_message(chat_id_to_upg, translate_current_text(all_messages["Available_commands_premium"], lang_from="en", lang_to=users_dict[chat_id_to_upg][0].lang).format("🔓","👇","/weather","/planner","❔", users_dict[chat_id_to_upg][0].premium_expiring_date[0]), reply_markup=keyboard_for_premium_available_commands, parse_mode='HTML')
                            bot.send_message(message.chat.id, text=f"Premium account is active")

                        else:
                            bot.send_message(message.chat.id, text=f"User has already have active premium account {users_dict[chat_id_to_upg][0].info()}")
                    else:
                        # print(message.text)
                    
                        datetime_object = datetime.strptime(users_dict[str(message.chat.id)][0].time_of_registration, '%d.%m.%Y')
                        if (int((datetime.now().today()-datetime_object).days)<=3 or users_dict[str(message.chat.id)][0].premium==True):
                            if "/" not in message.text:
                                oribot_generated_answer = generated_answer(message.text)
                                print(f"Answer was generated successfully for {users_dict[str(message.chat.id)][0].chat_id}")
                                # bot.send_message(message.chat.id, translate_current_text(oribot_generated_answer, lang_from="en", lang_to=users_dict[str(message.chat.id)][0].lang))
                                bot.send_message(message.chat.id, oribot_generated_answer)
                            else:
                                bot.send_message(message.chat.id, all_messages["Do_not_understand"].format("😕"))
                        else:
                            keyboard = types.InlineKeyboardMarkup()
                            premium_plan = types.InlineKeyboardButton(text=translate_current_text("About Premium 😎",lang_to=users_dict[str(message.chat.id)][0].lang, lang_from="en"), callback_data="premium_plan")
                            keyboard.add(premium_plan)
                            bot.send_message(message.chat.id, all_messages["AI_usage_declined"].format("⭐️"), reply_markup=keyboard)
                else:
                    bot.send_message(message.chat.id, all_messages["Use_start_command"])
            else:
                bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.chat.id)][0].user_first_name}({users_dict[str(message.chat.id)][0].chat_id}) send_text",ex)
        return
    
    # functions to handle requests
    @bot.callback_query_handler(func=lambda message: True)
    def handle_query(message):
        try:
            if users_dict[str(message.message.chat.id)][0].activated_bot:
                if message.data == "basic_plan":
                    keyboard_for_basic = types.InlineKeyboardMarkup()
                    button_buy_premium = types.InlineKeyboardButton(text=translate_current_text("Premium ⭐️",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en"), callback_data="buy_premium")
                    list_of_commands_basic = types.InlineKeyboardButton(text=translate_current_text("Commands ✍️",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en"), callback_data="available_commands")
                    premium_plan = types.InlineKeyboardButton(text=translate_current_text("About Premium 😎",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en"), callback_data="premium_plan")
                    keyboard_for_basic.add(button_buy_premium)
                    keyboard_for_basic.add(list_of_commands_basic, premium_plan)
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["About_basic_plan"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("OriBot","☺️","📝","👉","👉","👉","🔒","⭐️","⭐️", ), reply_markup=keyboard_for_basic, parse_mode='HTML')
                elif message.data == "premium_plan":
                    keyboard_for_premium = types.InlineKeyboardMarkup()
                    button_buy_premium = types.InlineKeyboardButton(text=translate_current_text("Premium ⭐️",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en"), callback_data="buy_premium")
                    list_of_commands_premium = types.InlineKeyboardButton(text=translate_current_text("Commands ✍️",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en"), callback_data="available_commands")
                    basic_plan = types.InlineKeyboardButton(text=translate_current_text("About Basic 😄",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en"), callback_data="basic_plan")
                    keyboard_for_premium.add(button_buy_premium)
                    keyboard_for_premium.add(list_of_commands_premium,basic_plan)
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["About_premium_plan"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("€","⭐️","📝","👉","OriBot","👉","👉","⭐️","👇"), reply_markup=keyboard_for_premium)
                elif message.data == "available_commands":
                    # print(type(users_dict[str(message.message.chat.id)][0].chat_id)) -> <class 'int'>
                    if users_dict[str(message.message.chat.id)][0].premium:
                        keyboard_for_premium_available_commands = types.InlineKeyboardMarkup()
                        button_premium_weather = types.InlineKeyboardButton(text=translate_current_text("Weather",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" ⛅️", callback_data="available_commands_premium_weather")
                        button_premium_planner = types.InlineKeyboardButton(text=translate_current_text("Planner",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" 📔", callback_data="available_commands_planner")
                        # button_premium_news = types.InlineKeyboardButton(text=translate_current_text("News",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" 🗞", callback_data="available_commands_premium_news")
                        keyboard_for_premium_available_commands.add(button_premium_weather)
                        keyboard_for_premium_available_commands.add(button_premium_planner)
                        # keyboard_for_premium_available_commands.add(button_premium_news)
                        # testing_command(message)
                        try:
                            bot.send_message(message.message.chat.id, translate_current_text(all_messages["Available_commands_premium"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("🔓","👇","/weather","/planner","❔", users_dict[str(message.message.chat.id)][0].premium_expiring_date[0]), reply_markup=keyboard_for_premium_available_commands, parse_mode='HTML')
                        except Exception as ex:
                            bot.send_message(message.message.chat.id, translate_current_text(all_messages["Available_commands_premium"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("🔓","👇","/weather","/planner","❔", users_dict[str(message.message.chat.id)][0].promo_code_expiring_date[0]), reply_markup=keyboard_for_premium_available_commands, parse_mode='HTML')
                    else:
                        keyboard_for_basic_available_commands = types.InlineKeyboardMarkup()
                        button_promo_code = types.InlineKeyboardButton(text=translate_current_text("Promo code",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" 🏷", callback_data="promo_code")
                        button_buy_premium_basic = types.InlineKeyboardButton(text=translate_current_text("Premium",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" ⭐️", callback_data="buy_premium")
                        button_basic_weather=types.InlineKeyboardButton(text=translate_current_text("Weather",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" ⛅️", callback_data="available_commands_basic_weather")
                        button_basic_planner = types.InlineKeyboardButton(text=translate_current_text("Planner",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" 📔", callback_data="available_commands_planner")
                        # button_basic_news = types.InlineKeyboardButton(text=translate_current_text("News",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" 🗞", callback_data="available_commands_basic_news")
                        keyboard_for_basic_available_commands.add(button_buy_premium_basic)
                        keyboard_for_basic_available_commands.add(button_promo_code)
                        keyboard_for_basic_available_commands.add(button_basic_weather)
                        keyboard_for_basic_available_commands.add(button_basic_planner)
                        # keyboard_for_basic_available_commands.add(button_basic_news)
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Available_commands_basic"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("😀","👇","/weather","/planner", "❔","⭐️"), reply_markup=keyboard_for_basic_available_commands)
                elif message.data=="available_commands_premium_weather" or message.data=="available_commands_basic_weather":
                    weather_main_function(message.message)
                elif message.data in ["button_one_day_location_premium_1","button_three_days_location_premium_3","button_seven_days_location_premium_7", "button_ten_days_location_premium_10", "button_one_day_location_basic_1"]:
                    if message.data=="button_ten_days_location_premium_10":
                        period_location_user_premium = int(message.data[-2:])
                    else:
                        period_location_user_premium = int(message.data[-1])
                    sending_animation_bot_working(message.message, type_gif="We_are_working_on_it")
                    response_location_weather=weather_main(users_dict[str(message.message.chat.id)][0], period_location_user_premium)
                    if response_location_weather!=False:
                        for n, weather_current in zip(range(period_location_user_premium),response_location_weather):
                            bot.send_message(message.message.chat.id, weather_current)
                            if period_location_user_premium>1:
                                sleep(1)
                    else:
                        keyboard_region = types.InlineKeyboardMarkup()
                        button_weather_region = types.InlineKeyboardButton(text=translate_current_text("Region",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+" 🗺", callback_data="button_weather_region")
                        keyboard_region.add(button_weather_region)
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Location_incorrect"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("🧐","/region"), reply_markup=keyboard_region)
                elif message.data in ["button_three_days_location_basic_3","button_seven_days_location_basic_7", "button_ten_days_location_basic_10"]:
                    message_about_restrictions(message)
                elif message.data=="button_location_y":
                    # users_dict[str(message.chat.id)][0].manual_region=False
                    weather_location_lat_long(message.message)
                elif message.data=="button_location_n":
                    region_oribot(message.message)
                elif message.data=="button_new_event_schedule_forecast":
                    schedule_forecast_new_event(message.message)
                elif message.data == "button_weather_region":
                    region_oribot(message.message)
                elif message.data=="button_schedule_weather_y":
                    try:
                        sending_animation_bot_working(message.message, type_gif="We_are_working_on_it")
                    except Exception as ex:
                        print(ex)
                    # users_dict[str(message.message.chat.id)][0].counter_for_scheduled_jobs=0
                    try:
                        scheduling_weather_event(message.message)
                    except Exception:
                        users_dict[str(message.message.chat.id)][0].schedule_active_event=False
                        del users_dict[str(message.message.chat.id)][1]["All_weather_events"][len(users_dict[str(message.message.chat.id)][1]["All_weather_events"])-1]
                        sending_animation_bot_working(message.message, type_gif="Smth_went_wrong")
                        sleep(1)
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Schedule_smth_went_wrong"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("@oribot_support_bot", "🥴"))
                        sleep(1)
                        scheduling_forecast(message.message)
                    # bot.send_message(message.message.chat.id, translate_current_text(all_messages["Schedule_new_event_was_scheduled"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("🥳", "🔥"))
                    # print("hi",users_dict[str(message.message.chat.id)][1]["All_weather_events"][len(users_dict[str(message.message.chat.id)][1]["All_weather_events"])-1])
                elif message.data=="button_schedule_weather_n":
                    users_dict[str(message.message.chat.id)][0].schedule_forecast_new_event_time=False
                    users_dict[str(message.message.chat.id)][0].schedule_forecast_new_event_location=False
                    del users_dict[str(message.message.chat.id)][1]["All_weather_events"][len(users_dict[str(message.message.chat.id)][1]["All_weather_events"])-1]
                    # if len(users_dict[str(message.chat.id)][1]["All_weather_events"])==0:

                    # users_dict[str(message.chat.id)][1]["All_weather_events"][len(users_dict[str(message.chat.id)][1]["All_weather_events"])-1][len(users_dict[str(message.chat.id)][1]["All_weather_events"])+1]["Time"]
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["Schedule_new_event_answer_n"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("/new_forecast_event","😊"))
                elif message.data=="button_location_y_schedule":

                    users_dict[str(message.message.chat.id)][0].schedule_forecast_new_event_time=True
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["Schedule_new_event_get_time"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("⌛️"))
                elif message.data=="button_location_n_schedule":
                    users_dict[str(message.message.chat.id)][0].schedule_region_flag=True
                    users_dict[str(message.message.chat.id)][0].schedule_active_event_change_location=True
                    region_oribot(message.message)
                elif message.data=="button_print_all_events_schedule_forecast":
                    print_all_events(message.message)
                elif message.data=="button_remove_event_schedule_forecast":
                    remove_event(message.message)
                elif message.data in ["button_remove_event_number_"+str(n) for n in range(1,11)]:
                    if message.data[-1]=="0":
                        users_dict[str(message.message.chat.id)][0].schedule_event_remove_number=int(message.data[-2])
                    else:
                        users_dict[str(message.message.chat.id)][0].schedule_event_remove_number=int(message.data[-1])

                    if users_dict[str(message.message.chat.id)][0].schedule_remove_event_active:
                        keyboard_remove_event_y_n = types.InlineKeyboardMarkup()
                        button_remove_event_y = types.InlineKeyboardButton(text=translate_current_text("Yes",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_remove_event_y")
                        button_remove_event_n = types.InlineKeyboardButton(text=translate_current_text("No",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_remove_event_n")
                        keyboard_remove_event_y_n.add(button_remove_event_y,button_remove_event_n)
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Schedule_remove_event_enter_confirmation"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format(emoji_digits_time[users_dict[str(message.message.chat.id)][0].schedule_event_remove_number],users_dict[str(message.message.chat.id)][1]["All_weather_events"][users_dict[str(message.message.chat.id)][0].schedule_event_remove_number-1]['Location'],"🏘", users_dict[str(message.message.chat.id)][1]["All_weather_events"][users_dict[str(message.message.chat.id)][0].schedule_event_remove_number-1]['Time'], "⏳"), reply_markup=keyboard_remove_event_y_n)
                    else:
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_specific_remove_event_active_false"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("/remove_forecast_event","😊"))

                        # bot.send_message(message.message.chat.id, translate_current_text(all_messages["Schedule_remove_event_enter_confirmation"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format(emoji_digits_time[users_dict[str(message.message.chat.id)][0].schedule_event_remove_number],users_dict[str(message.message.chat.id)][1]["All_weather_events"][users_dict[str(message.message.chat.id)][0].schedule_event_remove_number-1][users_dict[str(message.message.chat.id)][0].schedule_event_remove_number]['Location'],"🏘", users_dict[str(message.message.chat.id)][1]["All_weather_events"][users_dict[str(message.message.chat.id)][0].schedule_event_remove_number-1][users_dict[str(message.message.chat.id)][0].schedule_event_remove_number]['Time'], "⏳"), reply_markup=keyboard_remove_event_y_n)

                elif message.data=="button_remove_event_y":
                    users_dict[str(message.message.chat.id)][1]["All_weather_events"][users_dict[str(message.message.chat.id)][0].schedule_event_remove_number-1]["Remove"]=True
                    scheduling_weather_event(message.message)
                elif message.data=="button_remove_event_n":
                    scheduling_forecast(message.message)
                elif message.data=="available_commands_planner":
                    planner_function_main(message.message)
                elif message.data=="button_planner_every_day_event_schedule_forecast":
                    every_day_event(message.message)
                elif message.data=="button_every_day_event_y":
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_every_day_event_get_time"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("⌛️"))
                    users_dict[str(message.message.chat.id)][0].planner_every_day_event_get_time=True
                    users_dict[str(message.message.chat.id)][0].planner_every_day_txt_flag=False
                elif message.data=="button_every_day_event_n":
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_every_day_event_txt"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("👉"))
                    users_dict[str(message.message.chat.id)][0].planner_every_day_event_change_txt=True
                    users_dict[str(message.message.chat.id)][0].planner_every_day_txt_flag=True
                elif message.data=="button_schedule_every_day_planner_y":
                    try:
                        sending_animation_bot_working(message.message, type_gif="We_are_working_on_it")
                        scheduling_every_day_event(message.message)
                        users_dict[str(message.message.chat.id)][0].planner_every_day_event_get_time=False
                        users_dict[str(message.message.chat.id)][0].planner_every_day_active_event=False
                        users_dict[str(message.message.chat.id)][0].planner_every_day_txt_flag=False
                        users_dict[str(message.message.chat.id)][0].planner_every_day_event_change_txt=False
                    except Exception:
                        users_dict[str(message.message.chat.id)][0].planner_every_day_event_get_time=False
                        users_dict[str(message.message.chat.id)][0].planner_every_day_active_event=False
                        users_dict[str(message.message.chat.id)][0].planner_every_day_txt_flag=False
                        users_dict[str(message.message.chat.id)][0].planner_every_day_event_change_txt=False
                        del users_dict[str(message.message.chat.id)][2]["All_every_day_events"][len(users_dict[str(message.message.chat.id)][2]["All_every_day_events"])-1]
                        sending_animation_bot_working(message.message, type_gif="Smth_went_wrong")
                        sleep(1)
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Schedule_smth_went_wrong"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("@oribot_support_bot", "🥴"))
                        sleep(1)
                        every_day_event(message.message)
                elif message.data=="button_schedule_every_day_planner_n":
                    users_dict[str(message.message.chat.id)][0].planner_every_day_event_get_time=False
                    users_dict[str(message.message.chat.id)][0].planner_every_day_active_event=False
                    users_dict[str(message.message.chat.id)][0].planner_every_day_txt_flag=False
                    users_dict[str(message.message.chat.id)][0].planner_every_day_event_change_txt=False
                    del users_dict[str(message.message.chat.id)][2]["All_every_day_events"][len(users_dict[str(message.message.chat.id)][2]["All_every_day_events"])-1]
                    # if len(users_dict[str(message.chat.id)][1]["All_weather_events"])==0:
                    # users_dict[str(message.chat.id)][1]["All_weather_events"][len(users_dict[str(message.chat.id)][1]["All_weather_events"])-1][len(users_dict[str(message.chat.id)][1]["All_weather_events"])+1]["Time"]
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["Schedule_new_event_answer_n"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("/new_every_day_event","😊"))
                    sleep(1)
                    every_day_event(message.message)
                elif message.data=="button_new_event_planner":
                    every_day_new_event(message.message)
                elif message.data=="button_planner_new_event_schedule_planner_every_day":
                    every_day_new_event(message.message)
                elif message.data=="button_planner_remove_event_schedule_planner_every_day":
                    remove_every_day_event(message.message)
                elif message.data=="button_planner_all_events_schedule_planner_every_day":
                    all_every_day_event(message.message)
                elif message.data in ["button_remove_event_number_every_day_"+str(n) for n in range(1,11)]:
                    if message.data[-2].isdigit():
                        users_dict[str(message.message.chat.id)][0].planner_every_day_event_remove_specific_event=int(message.data[-2])
                    else:
                        users_dict[str(message.message.chat.id)][0].planner_every_day_event_remove_specific_event=int(message.data[-1])
                    if users_dict[str(message.message.chat.id)][0].planner_every_day_event_remove_active:
                        keyboard_remove_every_day_event_y_n = types.InlineKeyboardMarkup()
                        button_remove_every_day_event_y = types.InlineKeyboardButton(text=translate_current_text("Yes",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_remove_every_day_event_y")
                        button_remove_every_day_event_n = types.InlineKeyboardButton(text=translate_current_text("No",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_remove_every_day_event_n")
                        keyboard_remove_every_day_event_y_n.add(button_remove_every_day_event_y,button_remove_every_day_event_n)
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_every_day_remove_event_enter_confirmation"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format(emoji_digits_time[users_dict[str(message.message.chat.id)][0].planner_every_day_event_remove_specific_event],users_dict[str(message.message.chat.id)][2]["All_every_day_events"][users_dict[str(message.message.chat.id)][0].planner_every_day_event_remove_specific_event-1]['Text'],"💬", users_dict[str(message.message.chat.id)][2]["All_every_day_events"][users_dict[str(message.message.chat.id)][0].planner_every_day_event_remove_specific_event-1]['Time'], "⏳"), reply_markup=keyboard_remove_every_day_event_y_n)
                    else:
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_specific_remove_event_active_false"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("/remove_every_day_event","😊"))
                elif message.data=="button_remove_every_day_event_y":
                    users_dict[str(message.message.chat.id)][2]["All_every_day_events"][users_dict[str(message.message.chat.id)][0].planner_every_day_event_remove_specific_event-1]["Remove"]=True
                    try:
                        scheduling_every_day_event(message.message)
                    except Exception as ex:
                        print(ex)
                        sending_animation_bot_working(message.message, type_gif="Smth_went_wrong")
                        sleep(1)
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Schedule_smth_went_wrong"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("@oribot_support_bot", "🥴"))
                elif message.data=="button_remove_every_day_event_n":
                    every_day_event(message.message)
                elif message.data=="button_planner_one_event_schedule_forecast":
                    specific_event(message.message)
                elif message.data=="button_planner_new_event_schedule_planner_specific":
                    specific_new_event(message.message)
                elif message.data=="button_planner_remove_event_schedule_planner_specific":
                    specific_remove_event(message.message)
                elif message.data=="button_planner_all_events_schedule_planner_specific":
                    specific_all_events(message.message)
                elif message.data=="button_specific_event_y":
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_specific_event_get_date"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format(datetime.now().date().strftime('%d.%m.%Y'),"📅"))
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_get_date=True
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_txt_flag=False
                elif message.data=="button_specific_event_n":
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_specific_event_txt"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("👉"))
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_change_txt=True
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_txt_flag=True

                    users_dict[str(message.message.chat.id)][0].planner_specific_event_get_date=False
                elif message.data=="button_schedule_specific_date_planner_y":
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_specific_event_get_time"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("⌛️"))
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_get_date=False
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_get_time=True
                elif message.data=="button_schedule_specific_date_planner_n":
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_specific_event_get_date"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format(datetime.now().date().strftime('%d.%m.%Y'),"📅"))
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_get_date=True
                elif message.data=="button_schedule_specific_time_planner_y":
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_get_time=False
                    keyboard_set_specific_event_y_n = types.InlineKeyboardMarkup()
                    button_set_specific_event_y = types.InlineKeyboardButton(text=translate_current_text("Yes",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_set_specific_event_y")
                    button_set_specific_event_n = types.InlineKeyboardButton(text=translate_current_text("No",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_set_specific_event_n")
                    keyboard_set_specific_event_y_n.add(button_set_specific_event_y,button_set_specific_event_n)
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_specific_new_event_question_y_n"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format(emoji_digits_time[len(users_dict[str(message.message.chat.id)][2]["All_specific_events"])], users_dict[str(message.message.chat.id)][2]["All_specific_events"][len(users_dict[str(message.message.chat.id)][2]["All_specific_events"])-1]["Text"], "📝", str(users_dict[str(message.message.chat.id)][2]["All_specific_events"][len(users_dict[str(message.message.chat.id)][2]["All_specific_events"])-1]["Time"]), "⏳",str(users_dict[str(message.message.chat.id)][2]["All_specific_events"][len(users_dict[str(message.message.chat.id)][2]["All_specific_events"])-1]["Date_text"]),"📅"), reply_markup=keyboard_set_specific_event_y_n)
                elif message.data=="button_schedule_specific_time_planner_n":
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_specific_event_get_time"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("⌛️"))
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_get_time=True
                elif message.data=="button_set_specific_event_y":
                    try:
                        sending_animation_bot_working(message.message,type_gif="We_are_working_on_it")
                        scheduling_specific_event(message.message)
                        users_dict[str(message.message.chat.id)][0].planner_specific_event_active=False
                        users_dict[str(message.message.chat.id)][0].planner_specific_event_txt_flag=False
                        users_dict[str(message.message.chat.id)][0].planner_specific_event_change_txt=False
                        users_dict[str(message.message.chat.id)][0].planner_specific_event_get_date=False
                        users_dict[str(message.message.chat.id)][0].planner_specific_event_get_time=False
                    except Exception:
                        users_dict[str(message.message.chat.id)][0].planner_specific_event_active=False
                        users_dict[str(message.message.chat.id)][0].planner_specific_event_txt_flag=False
                        users_dict[str(message.message.chat.id)][0].planner_specific_event_change_txt=False
                        users_dict[str(message.message.chat.id)][0].planner_specific_event_get_date=False
                        users_dict[str(message.message.chat.id)][0].planner_specific_event_get_time=False
                        del users_dict[str(message.message.chat.id)][2]["All_specific_events"][len(users_dict[str(message.message.chat.id)][2]["All_specific_events"])-1]
                        sending_animation_bot_working(message.message, type_gif="Smth_went_wrong")
                        sleep(1)
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Schedule_smth_went_wrong"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("@oribot_support_bot", "🥴"))
                        sleep(1)
                        specific_event(message.message)
                elif message.data=="button_set_specific_event_n":
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_active=False
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_txt_flag=False
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_change_txt=False
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_get_date=False
                    users_dict[str(message.message.chat.id)][0].planner_specific_event_get_time=False
                    del users_dict[str(message.message.chat.id)][2]["All_specific_events"][len(users_dict[str(message.message.chat.id)][2]["All_specific_events"])-1]
                    # if len(users_dict[str(message.chat.id)][1]["All_weather_events"])==0:
                    # users_dict[str(message.chat.id)][1]["All_weather_events"][len(users_dict[str(message.chat.id)][1]["All_weather_events"])-1][len(users_dict[str(message.chat.id)][1]["All_weather_events"])+1]["Time"]
                    bot.send_message(message.message.chat.id, translate_current_text(all_messages["Schedule_new_event_answer_n"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("/new_specific_event","😊"))
                    sleep(1)
                    specific_event(message.message)
                elif message.data in ["button_remove_event_number_specifik_"+str(n) for n in range(1,11)]:
                    if message.data[-2].isdigit():
                        users_dict[str(message.message.chat.id)][0].planner_specific_event_remove_specific_event=int(message.data[-2])
                    else:
                        users_dict[str(message.message.chat.id)][0].planner_specific_event_remove_specific_event=int(message.data[-1])
                    
                    if users_dict[str(message.message.chat.id)][0].planner_specific_event_remove_active:
                        keyboard_remove_specific_event_y_n = types.InlineKeyboardMarkup()
                        button_remove_specific_event_y = types.InlineKeyboardButton(text=translate_current_text("Yes",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+"✅", callback_data="button_remove_specifik_event_y")
                        button_remove_specific_event_n = types.InlineKeyboardButton(text=translate_current_text("No",lang_to=users_dict[str(message.message.chat.id)][0].lang, lang_from="en")+"❌", callback_data="button_remove_specifik_event_n")
                        keyboard_remove_specific_event_y_n.add(button_remove_specific_event_y,button_remove_specific_event_n)
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_specific_remove_event_enter_confirmation"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format(emoji_digits_time[users_dict[str(message.message.chat.id)][0].planner_specific_event_remove_specific_event],users_dict[str(message.message.chat.id)][2]["All_specific_events"][users_dict[str(message.message.chat.id)][0].planner_specific_event_remove_specific_event-1]['Text'],"💬", users_dict[str(message.message.chat.id)][2]["All_specific_events"][users_dict[str(message.message.chat.id)][0].planner_specific_event_remove_specific_event-1]['Time'], "⏳", users_dict[str(message.message.chat.id)][2]["All_specific_events"][users_dict[str(message.message.chat.id)][0].planner_specific_event_remove_specific_event-1]['Date_text'], "📅"), reply_markup=keyboard_remove_specific_event_y_n)
                    else:
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Planner_specific_remove_event_active_false"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("/remove_specific_event","😊"))

                elif message.data=="button_remove_specific_event_y":
                    users_dict[str(message.message.chat.id)][2]["All_specific_events"][users_dict[str(message.message.chat.id)][0].planner_specific_event_remove_specific_event-1]["Remove"]=True
                    scheduling_specific_event(message.message)
                elif message.data=="button_remove_specific_event_n":
                    try:
                        specific_event(message.message)
                    except Exception as ex:
                        sending_animation_bot_working(message.message, type_gif="Smth_went_wrong")
                        sleep(1)
                        bot.send_message(message.message.chat.id, translate_current_text(all_messages["Schedule_smth_went_wrong"], lang_from="en", lang_to=users_dict[str(message.message.chat.id)][0].lang).format("@oribot_support_bot", "🥴"))
                elif message.data=="buy_premium":
                    buy_premium_main(message.message)
                elif message.data=="button_for_all_lang":
                    all_lang(message.message)
                elif message.data=="promo_code":
                    promo_code_processing(message.message)
            else:
                bot.send_message(message.message.chat.id, all_messages["Use_command_start"].format("/start"))
        except KeyError:
            bot.send_message(message.message.chat.id, all_messages["Use_command_start"].format("/start"))
        except Exception as ex:
            bot.send_message(message.message.chat.id, all_messages["Schedule_smth_went_wrong"].format("@oribot_support_bot", "🥴"))
            print(f"{users_dict[str(message.message.chat.id)][0].user_first_name}({users_dict[str(message.message.chat.id)][0].chat_id}) handle_query",ex)
        return
    

    bot.polling()
    return 

if __name__ == "__main__":
    while True:
        try:
            telegram_bot()
        # except Reboot_bot as ex:
        #     users_dict = ex.args[1]
        #     folder_path = fr'C:\Users\Timur\Python\projects\oribot_project\oribot_main'
        #     file_name = 'test.py'
        #     function_name = 'telegram_bot_upd'
        #     function_args = [users_dict]

        #     # Go through all the files in the folder
        #     for file in os.listdir(folder_path):
        #         # Проверяем, является ли файл Python-скриптом
        #         if file.endswith('.py') and file==file_name:
        #             # Check if the file contains the desired function
        #             spec = importlib.util.spec_from_file_location(file, os.path.join(folder_path, file))
        #             module = importlib.util.module_from_spec(spec)
        #             spec.loader.exec_module(module)
        #             if hasattr(module, function_name):
        #                 print("sad")
        #                 print(dir(module))
        #                 # If the function is found, call it and pass the arguments
        #                 function = getattr(module, function_name)
        #                 print(function)
        #                 function(*function_args)
            # for file in os.listdir(folder_path):
            #     if file == file_name:
            #         # Загружаем модуль и вызываем функцию с передачей аргументов
            #         spec = importlib.util.spec_from_file_location(file, os.path.join(folder_path, file))
            #         module = importlib.util.module_from_spec(spec)
            #         spec.loader.exec_module(module)
            #         function = getattr(module, function_name)
            #         function(*function_args)
        except Exception as ex:
            print(ex)
            telegram_bot()  

