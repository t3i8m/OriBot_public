all_messages = {
    "Use_start_command":"Please use the /start command to start the bot",
    "Start_message": "Howdy, {}!{}\n\nPlease choose a language (send an emoji with the flag of your country) {}",
    "Start_message_2nd_part":"Or use the {} command to select the language {}",
    "Already_used_/start": "You have already run this bot. Use the {} command to find additional commands {}",
    "Change_lang":"Please choose another language (send an emoji with the flag of your country) {}",
    "Error_lang_emoji": "English was set automatically, if you want to choose another language use {} command{}",
    "Error_lang_not_available":"This language is not supported. English was set automatically, if you want to change language use /change_lang command{}",
    "To_see_all_languages":"If you want to see all available languages, use the {} command",
    "All_available_languages":"All available languages {}",
    # "Use_another_language":"To set bot language send an emoji with the flag of your country 👉",
    "If_want_set_lang":"If you want to change language, use {} command {}",
    "Language_successful":"Language was set successfuly {}",
    # "Something_went_wrong":"Something went wrong. Please contact the support bot {} 🫣",
    "About_oribot":"Welcome to {}!\nYour personal assistant and friend {}\n\nThe basic features are available to everyone for free, but it comes with an additional payment plan for extra features, for just 1{} per month {}",
    "About_basic_plan":"The standard plan is completely free for every {} user {}\n\nHere are the features you can use with this plan {}:\n\n{} You can ask the oribot questions (For example: Who is Michael Jordan?)* \n{} Daily planner with notifications\n{} Daily weather forecast\n\nLocked features that you can get by purchasing a subscription {}:\n\n{} Sending scheduled weather forecast\n{} Daily planner with no limit\n\n"+"<i>*This is a free function for one week</i>",
    "About_premium_plan":"The OriBot premium plan is available as a monthly subscription for just 1{} per month {}\n\nYou will have access to all of the bot's functionality: {} \n\n{}You can ask {} questions (for example: Who is Michael Jordan?)\n{}Daily planner with all functions\n{}Sending scheduled weather forecast\n\nTo purchase a subscription, click on the 'Premium {}' button {}",
    "AI_usage_declined":"You have already spent three trial days on this feature, to unlock the possibility of using it for an unlimited amount of time, buy a premium plan {}",
    "Do_not_understand":"Sorry, I do not understand. Please ask me another question {}",
    "Available_commands_premium":"Your unlocked Premium account gives you access to all the features of OriBot {}\n\nHere is a list of available Premium commands {}:\n\n{} - Sending scheduled weather forecast\n{} - Daily planner with no limit\n{} You have unlimited time to ask bot questions (Just write your question in the chat)\n\n<i>*Premium status expires on {}</i>",
    "Available_commands_basic":"You have an active Basic account {}\n\nThen you can use these commands {}:\n\n{} - Send today's weather report\n{} - Limited Daily planner (only 5 active events possible)\n{} - You have a limited time (one week) to ask the bot questions (just write your question in the chatbox)\n\nBuy a premium account to unlimited access to OriBot features {}",
    "Weather_start_message_premium_1_part":"Weather",
    "Weather_start_message_premium_2_part":"This weather function can {}:",
    "Weather_start_message_premium_3_part":"{} Send weather forecast by your current location (just send your location)\n{} Send weather forecast by entered location ({})\n{} Schedule to send weather forecast for each day automatically (use {} command)",
    "Location_days_premium":"Your location is {} {}\nPlease select for how many days you want to receive the forecast {}:\n",
    "Location_incorrect":"It is impossible to detect your location {}\n\nPlease send your location again. If this error occurs more than once, please use the {} command",
    "Location_basic_restriction":"You currently have a Basic account, so you are limited in some of Oribot's features. Buy Premium to unlock all features {}",
    "Region_start_message":"Please input your city",
    "Check_manual_location":"{} is that your city?",
    "Schedule_events_start_message":"Scheduled events {}:\n\nYou have {} scheduled event(s)\n\n{} - to create new event {}\n{} - to remove specific event {}\n{} - to view all your events {}",
    "Schedule_forecast_new_event_start_message":"This function allows you to set a scheduled forecast {}\n\nCurrently, you have {} active of {} possible events {}",
    "Schedule_forecast_new_event_method_location":"Please choose a way how to input location:\n\nSend your current location {}\n{} - to enter your city manually",
    "Schedule_forecast_new_event_reached_maximum_count":"You have reached the maximum possible number of events - {}\n\n {} - to remove one of the events\n{} - to see all active events",
    "Schedule_new_event_get_time":"Please enter the time when you would like to receive the daily forecast (example - 12:00) {}:",
    "Schedule_new_event_time_format":"Time format - (00:00 - 23:59), try again {}",
    "Schedule_new_event_input_format":"Please, enter digits and try again (example - 12:00) {}",
    "Schedule_new_event_question_y_n":"Your new event number is {}\n\nLocation: {} {}\n Time: {} {}\n\nDo you want to create this event?",
    "Schedule_new_event_answer_n":"Your event was removed. To create new event use command {} {}",
    # "Schedule_new_event_was_scheduled":"Congrats {}!\n\nEvent was successfully scheduled {}!",
    "Schedule_new_event_congrats":"Congrats {}!\nYou have created your {} event, which will send you the weather forecast for the city {} {}, everyday at {} {}",
    "Schedule_smth_went_wrong":"Oops..\nSomething went wrong. Please try again, or write to the support bot {} {}",
    "Schedule_you_have_active_event":"You have one unfinished event, finish it to create a new one {}",
    "Schedule_forecast_my_events_no_active_events":"You have no active events. Use the {} command to create a new event {}",
    "Schedule_forecast_my_events_list":"You have {} active event(s):",
    "Schedule_remove_event_enter_digit":"You have {} active event(s)\nPlease select digit, what event do you want to remove {}:",
    "Schedule_remove_event_enter_confirmation":"Are you sure you want to delete this event?\n\n{}\nLocation: {} {}\nTime: {} {}\n",
    "Schedule_remove_event_successfully":"Event was removed successfully {}",
    "Planner_start_message_1_part":"Planner",
    "Planner_start_message_2_part":"This weather function can {}:",
    "Planner_start_message_3_part":"{} Create a recurring event that reminds you to do something every day ({})\n{} Create an event that will be sent at a specific time with a specific text ({})",
    "Planner_max_num_specific_events":"You have reached maximum of every day events ({}). Use command {} to remove one of the events {}",
    "Planner_every_day_events_start_message_premium":"Every day events {}:\n\nYou have {} scheduled event(s)\n\n{} - to create new event {}\n{} - to remove specific event {}\n{} - to view all your events {}",
    "Planner_every_day_events_start_message_basic":"Every day events {}:\n\nYou have {}* scheduled event(s):\n\n{} - to create new event {}\n{} - to remove specific event {}\n{} - to view all your events {}\n\n<i>*You have Basic account, therefore you can set 5 active events</i>",
    "Planner_every_day_event_txt":"Please enter the text of the notification you wish to receive each day {}",
    "Planner_every_day_event_check_notification":"'{}'\n\nIs this the right text you want to receive every day?",
    "Planner_every_day_event_maximum_symbols_text":"Your text is longer than 500 characters, please make the text shorter and try again {}",
    "Planner_every_day_event_get_time":"Please enter the time when you would like to receive the daily notification (example - 12:00) {}:",
    "Planner_every_day_new_event_question_y_n":"Your new event number is {}\n\nNotification: {} {}\n Time: {} {}\n\nDo you want to create this event?",
    "Planner_new_event_congrats":"Congrats {}!\nYou have created your {} event, which will send you the notification with this text: '{}' {}, everyday at {} {}",
    "Planner_every_day_remove_event_enter_confirmation":"Are you sure you want to delete this event?\n\n{}\nNotification: {} {}\nTime: {} {}\n",
    "Planner_specific_events_start_message_premium":"Specific events {}:\n\nYou have {} scheduled event(s)\n\n{} - to create new event {}\n{} - to remove specific event {}\n{} - to view all your events {}",
    "Planner_specific_events_start_message_basic":"Specific events {}:\n\nYou have {} scheduled event(s)\n\n{} - to create new event {}\n{} - to remove specific event {}\n{} - to view all your events {}\n\nYou have Basic account, therefore you can set 5 active events",
    "Planner_specific_event_txt":"Please enter the text of the notification you wish to receive on a particular day {}",
    "Planner_specific_event_check_notification":"'{}'\n\nIs this the right text you want to receive on a particular day?",
    "Planner_specific_event_get_date":"Please enter the specific date when you would like to receive the notification (example - {}) {}:",
    "Planner_specific_date_event_question_y_n":"{} is that correct date?",
    "Planner_specific_date_format":"Date format - {} (the year must not be more than 2050), try again {}",
    "Planner_specific_date_input_format":"Please, enter digits and try again (example - {}) {}",
    "Planner_specific_event_get_time":"Please enter the time when you would like to receive the specific notification (example - 12:00) {}:",
    "Planner_specific_time_event_question_y_n":"{} is that correct time?",
    "Planner_specific_new_event_question_y_n":"Your new event number is {}\n\nNotification: {} {}\nTime: {} {}\nDate: {} {}\n\nDo you want to create this event?",
    "Planner_specific_date_false":"You cannot schedule an event for days that have already passed. Please try again {}",
    "Planner_specific_new_event_congrats":"Congrats {}!\nYou have created your {} event, which will send you the notification with this text: '{}' {}, on {} {}, at {} {}",
    "Planner_specific_remove_event_enter_confirmation":"Are you sure you want to delete this event?\n\n{}\nNotification: {} {}\nTime: {} {}\nDate: {} {}\n",
    "Planner_specific_remove_event_active_false":"Please use command {} to remove specific event {}",
    "Planner_specific_time_false":"You cannot schedule an event for time that has already passed. Please try again {}",
    "Premium_account_already_activeted":"You have already activated your Premium account and it expires on {} {}",
    "Premium_about_text":"{} bot has a 1 {} per month plan to unlock all the features. You can buy it by clicking on the button below {}",
    "Premium_time_limit":"You have already activated the payment, use this link before the expiry time (10 minutes) {}",
    "Payment_was_successful":"The payment was successful {}",
    "Payment_thanks_message":"Thank you from the {} Team {}\n\nAs a Premium user, you now have all the features of {} unlocked {}:\n\n{}You can ask unlimited number of questions (for example: Who is Michael Jordan?)\n{}Daily planner with all functions\n{}Sending scheduled weather forecast\n\nTry all the functions yourself {}",
    "Payment_was_unsuccessful":"The payment was unsuccessful {}\nPlease try again, if this error occurs more than once, contact support - {}",
    "Payment_expiring_reminder":"{} Your premium account expires in exactly 24 hours, to renew it you will need to re-subscribe when it expires {}",
    "Premium_expired":"Your premium account has expired, to buy one use {} or click the button below {}",
    "Premium_thanks_from_oribot_team":"Thank you from the {} Team {}",
    "Use_command_start":"Please use the command {} first",
    "Promo_code_start":"Enter a 4 letter promo code and you will receive 3 days of a premium account {}",
    "Promo_code_limitation":"You can only use a promo code once, to unlock a premium account use {} or the button below {}",
    "Promo_code_input_faill":"Please try again, use only letters (example - QWER) {}",
    "Promo_code_incorrect":"Incorrect promo code {}",
    "Promo_code_successful":"Congratulations {}\nYour premium account is valid and all features have been unlocked. Try it out for yourself {}",
    "Help_func_text":"Here are the main functions of {} {}\n\n{} - weather function\n{} - planner function\n{} - change the bot's language\n{} - upgrade account to premium\n{} You can ask {} questions (e.g. Who is Michael Jordan?)\n\nIf you have an error or would like to write feedback on the bot, use the support bot - {}",
    "Restrictions_at_the_moment":"{} Due to a technical problem on the gcore.com server, changes will be made to the Oribot:\n\n1 Today, you can subscribe to the premium version for free and it will not be charged to your card \n2 The weather forecast will only be available within Europe\n3 In the evening, the bot will be closed for maintenance\n4 Bot runtime will be slightly longer than usual\n5 Today the bot is only available in English\n\nChanges as of 28.04.2023 {}",
}

# The premium plan gives you access to all of OriBot's features for just $1 per month.
# Here is a list of features that are open to you 
# bot.send_message(message.chat.id,  translate_current_text("""Scheduled events ⏰
# You have {} scheduled events
# To create new event, use {} command 🆕
# To stop event, use {} command 🗑
# To view all your events, use {} 📜 👇
# """, lang_to = lang, lang_from = "en").format(emoji_digits_time[len(scheduled_events_dict["All Events"])], "/new_event", "/remove_event", "/my_events"))
# Congrats! 🎉
# You have created your 2️⃣ event, which will send you weather forecast for city Madrid, everyday at 20:40 🗓
# ❤️, OriBot, "👉","OriBot","👉","👉"

# Here are the main functions of OriBot 👇
# /weather - weather function
# /planner - planner function
# /change_lang - change the bot's language
# /buy_premium - upgrade account to premium
# 
# ❔ You can ask OriBot questions (e.g. Who is Michael Jordan?)

# If you have an error or would like to write feedback on the bot, use the support bot - @oribot_support_bot

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

 