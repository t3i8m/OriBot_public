import translators as ts
from translate import Translator
# from libretranslatepy import LibreTranslateAPI
import random

all_emails_holder = ["johnny_silverhand@gmail.com","johny_silverhand@gmail.com","johny_silverhan123d@gmail.com","johny_silverhan21d@gmail.com","johny_1silverhand@gmail.com","johny_silverhand321@gmail.com","johnn_silverhand@gmail.com","vi@gmail.com","vis@gmail.com","vik@gmail.com", "yudjin@gmail.com","artur_king228@gmail.com","nagibator_123@gmail.com"]

all_languages_lst = ['af', 'ak', 'am', 'ar', 'as', 'ay', 'az', 'be', 'bg', 'bho', 'bm', 'bn', 'bs', 'ca', 'ceb', 'ckb', 'co', 'cs', 'cy', 'da', 'de', 'doi', 'dv', 'ee', 'el', 'en', 'en-US', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fr', 'fy', 'ga', 'gd', 'gl', 'gn', 'gom', 
'gu', 'ha', 'haw', 'hi', 'hmn', 'hr', 'ht', 'hu', 'hy', 'id', 'ig', 'ilo', 'is', 'it', 'iw', 'ja', 'jw', 'ka', 'kk', 'km', 'kn', 'ko', 'kri', 'ku', 'ky', 'la', 'lb', 'lg', 'ln', 'lo', 'lt', 'lus', 'lv', 'mai', 'mg', 'mi', 'mk', 'ml', 'mn', 'mni-Mtei', 'mr', 'ms', 'mt', 'my', 'ne', 'nl', 'no', 'nso', 'ny', 'om', 'or', 'pa', 'pl', 'ps', 'pt', 'qu', 'ro', 'ru', 'rw', 'sa', 'sd', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sq', 'sr', 'st', 'su', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tl', 'tr', 'ts', 'tt', 'ug', 'uk', 'ur', 'uz', 'vi', 'xh', 'yi', 'yo', 'zh-CN', 'zh-TW', 'zu']

emoji_code_dict = {'🇦🇩': 'AD',
 '🇦🇪': 'AE',
 '🇦🇫': 'AF',
 '🇦🇬': 'AG',
 '🇦🇮': 'AI',
 '🇦🇱': 'AL',
 '🇦🇲': 'AM',
 '🇦🇴': 'AO',
 '🇦🇶': 'AQ',
 '🇦🇷': 'AR',
 '🇦🇸': 'AS',
 '🇦🇹': 'AT',
 '🇦🇺': 'AU',
 '🇦🇼': 'AW',
 '🇦🇽': 'AX',
 '🇦🇿': 'AZ',
 '🇧🇦': 'BA',
 '🇧🇧': 'BB',
 '🇧🇩': 'BD',
 '🇧🇪': 'BE',
 '🇧🇫': 'BF',
 '🇧🇬': 'BG',
 '🇧🇭': 'BH',
 '🇧🇮': 'BI',
 '🇧🇯': 'BJ',
 '🇧🇱': 'BL',
 '🇧🇲': 'BM',
 '🇧🇳': 'BN',
 '🇧🇴': 'BO',
 '🇧🇶': 'BQ',
 '🇧🇷': 'BR',
 '🇧🇸': 'BS',
 '🇧🇹': 'BT',
 '🇧🇻': 'BV',
 '🇧🇼': 'BW',
 '🇧🇾': 'BY',
 '🇧🇿': 'BZ',
 '🇨🇦': 'CA',
 '🇨🇨': 'CC',
 '🇨🇩': 'CD',
 '🇨🇫': 'CF',
 '🇨🇬': 'CG',
 '🇨🇭': 'CH',
 '🇨🇮': 'CI',
 '🇨🇰': 'CK',
 '🇨🇱': 'CL',
 '🇨🇲': 'CM',
 '🇨🇳': 'CN',
 '🇨🇴': 'CO',
 '🇨🇷': 'CR',
 '🇨🇺': 'CU',
 '🇨🇻': 'CV',
 '🇨🇼': 'CW',
 '🇨🇽': 'CX',
 '🇨🇾': 'CY',
 '🇨🇿': 'CZ',
 '🇩🇪': 'DE',
 '🇩🇯': 'DJ',
 '🇩🇰': 'DK',
 '🇩🇲': 'DM',
 '🇩🇴': 'DO',
 '🇩🇿': 'DZ',
 '🇪🇨': 'EC',
 '🇪🇪': 'EE',
 '🇪🇬': 'EG',
 '🇪🇭': 'EH',
 '🇪🇷': 'ER',
 '🇪🇸': 'ES',
 '🇪🇹': 'ET',
 '🇪🇺': 'EU',
 '🇫🇮': 'FI',
 '🇫🇯': 'FJ',
 '🇫🇰': 'FK',
 '🇫🇲': 'FM',
 '🇫🇴': 'FO',
 '🇫🇷': 'FR',
 '🇬🇦': 'GA',
 '🇬🇧': 'GB',
 '🇬🇩': 'GD',
 '🇬🇪': 'GE',
 '🇬🇫': 'GF',
 '🇬🇬': 'GG',
 '🇬🇭': 'GH',
 '🇬🇮': 'GI',
 '🇬🇱': 'GL',
 '🇬🇲': 'GM',
 '🇬🇳': 'GN',
 '🇬🇵': 'GP',
 '🇬🇶': 'GQ',
 '🇬🇷': 'GR',
 '🇬🇸': 'GS',
 '🇬🇹': 'GT',
 '🇬🇺': 'GU',
 '🇬🇼': 'GW',
 '🇬🇾': 'GY',
 '🇭🇰': 'HK',
 '🇭🇲': 'HM',
 '🇭🇳': 'HN',
 '🇭🇷': 'HR',
 '🇭🇹': 'HT',
 '🇭🇺': 'HU',
 '🇮🇩': 'ID',
 '🇮🇪': 'IE',
 '🇮🇱': 'IL',
 '🇮🇲': 'IM',
 '🇮🇳': 'IN',
 '🇮🇴': 'IO',
 '🇮🇶': 'IQ',
 '🇮🇷': 'IR',
 '🇮🇸': 'IS',
 '🇮🇹': 'IT',
 '🇯🇪': 'JE',
 '🇯🇲': 'JM',
 '🇯🇴': 'JO',
 '🇯🇵': 'JP',
 '🇰🇪': 'KE',
 '🇰🇬': 'KG',
 '🇰🇭': 'KH',
 '🇰🇮': 'KI',
 '🇰🇲': 'KM',
 '🇰🇳': 'KN',
 '🇰🇵': 'KP',
 '🇰🇷': 'KR',
 '🇰🇼': 'KW',
 '🇰🇾': 'KY',
 '🇰🇿': 'KZ',
 '🇱🇦': 'LA',
 '🇱🇧': 'LB',
 '🇱🇨': 'LC',
 '🇱🇮': 'LI',
 '🇱🇰': 'LK',
 '🇱🇷': 'LR',
 '🇱🇸': 'LS',
 '🇱🇹': 'LT',
 '🇱🇺': 'LU',
 '🇱🇻': 'LV',
 '🇱🇾': 'LY',
 '🇲🇦': 'MA',
 '🇲🇨': 'MC',
 '🇲🇩': 'MD',
 '🇲🇪': 'ME',
 '🇲🇫': 'MF',
 '🇲🇬': 'MG',
 '🇲🇭': 'MH',
 '🇲🇰': 'MK',
 '🇲🇱': 'ML',
 '🇲🇲': 'MM',
 '🇲🇳': 'MN',
 '🇲🇴': 'MO',
 '🇲🇵': 'MP',
 '🇲🇶': 'MQ',
 '🇲🇷': 'MR',
 '🇲🇸': 'MS',
 '🇲🇹': 'MT',
 '🇲🇺': 'MU',
 '🇲🇻': 'MV',
 '🇲🇼': 'MW',
 '🇲🇽': 'MX',
 '🇲🇾': 'MY',
 '🇲🇿': 'MZ',
 '🇳🇦': 'NA',
 '🇳🇨': 'NC',
 '🇳🇪': 'NE',
 '🇳🇫': 'NF',
 '🇳🇬': 'NG',
 '🇳🇮': 'NI',
 '🇳🇱': 'NL',
 '🇳🇴': 'NO',
 '🇳🇵': 'NP',
 '🇳🇷': 'NR',
 '🇳🇺': 'NU',
 '🇳🇿': 'NZ',
 '🇴🇲': 'OM',
 '🇵🇦': 'PA',
 '🇵🇪': 'PE',
 '🇵🇫': 'PF',
 '🇵🇬': 'PG',
 '🇵🇭': 'PH',
 '🇵🇰': 'PK',
 '🇵🇱': 'PL',
 '🇵🇲': 'PM',
 '🇵🇳': 'PN',
 '🇵🇷': 'PR',
 '🇵🇸': 'PS',
 '🇵🇹': 'PT',
 '🇵🇼': 'PW',
 '🇵🇾': 'PY',
 '🇶🇦': 'QA',
 '🇷🇪': 'RE',
 '🇷🇴': 'RO',
 '🇷🇸': 'RS',
 '🇷🇺': 'RU',
 '🇷🇼': 'RW',
 '🇸🇦': 'SA',
 '🇸🇧': 'SB',
 '🇸🇨': 'SC',
 '🇸🇩': 'SD',
 '🇸🇪': 'SE',
 '🇸🇬': 'SG',
 '🇸🇭': 'SH',
 '🇸🇮': 'SI',
 '🇸🇯': 'SJ',
 '🇸🇰': 'SK',
 '🇸🇱': 'SL',
 '🇸🇲': 'SM',
 '🇸🇳': 'SN',
 '🇸🇴': 'SO',
 '🇸🇷': 'SR',
 '🇸🇸': 'SS',
 '🇸🇹': 'ST',
 '🇸🇻': 'SV',
 '🇸🇽': 'SX',
 '🇸🇾': 'SY',
 '🇸🇿': 'SZ',
 '🇹🇨': 'TC',
 '🇹🇩': 'TD',
 '🇹🇫': 'TF',
 '🇹🇬': 'TG',
 '🇹🇭': 'TH',
 '🇹🇯': 'TJ',
 '🇹🇰': 'TK',
 '🇹🇱': 'TL',
 '🇹🇲': 'TM',
 '🇹🇳': 'TN',
 '🇹🇴': 'TO',
 '🇹🇷': 'TR',
 '🇹🇹': 'TT',
 '🇹🇻': 'TV',
 '🇹🇼': 'TW',
 '🇹🇿': 'TZ',
 '🇺🇦': 'UA',
 '🇺🇬': 'UG',
 '🇺🇲': 'UM',
 '🇺🇸': 'US',
 '🇺🇾': 'UY',
 '🇺🇿': 'UZ',
 '🇻🇦': 'VA',
 '🇻🇨': 'VC',
 '🇻🇪': 'VE',
 '🇻🇬': 'VG',
 '🇻🇮': 'VI',
 '🇻🇳': 'VN',
 '🇻🇺': 'VU',
 '🇼🇫': 'WF',
 '🇼🇸': 'WS',
 '🇽🇰': 'XK',
 '🇾🇪': 'YE',
 '🇾🇹': 'YT',
 '🇿🇦': 'ZA',
 '🇿🇲': 'ZM',
 '🇿🇼': 'ZW',
 "🇺🇰":"EN",
 "🇬🇧":"EN"}

emoji_digits_time = {
    0:"0️⃣",
    1:"1️⃣",
    2:"2️⃣",
    3:"3️⃣",
    4:"4️⃣",
    5:"5️⃣",
    6:"6️⃣",
    7:"7️⃣",
    8:"8️⃣",
    9:"9️⃣",
    10:"🔟",
    
}
# 6️⃣ 7️⃣ 8️⃣ 9️⃣ 🔟
# emoji_description = """
# 🇦🇲 - Armenia
# 🇦🇿 - Azerbaijan
# 🇧🇪 - Belgium
# 🇧🇬 - Bulgaria
# 🇩🇪 - Germany
# 🇪🇪 - Estonia
# 🇪🇸 - Spain
# 🇫🇮 - Finland
# 🇫🇷 - France
# 🇬🇧 - United Kingdom
# 🇭🇷 - Croatia
# 🇭🇺 - Hungary
# 🇮🇹 - Italy
# 🇱🇹 - Lithuania
# 🇱🇻 - Latvia
# 🇲🇹 - Malta
# 🇳🇱 - Netherlands
# 🇳🇴 - Norway
# 🇵🇱 - Poland
# 🇵🇹 - Portugal
# 🇷🇴 - Romania
# 🇷🇺 - Russia
# 🇸🇦 - Saudi Arabia
# 🇸🇮 - Slovenia
# 🇸🇰 - Slovakia
# 🇹🇭 - Thailand
# 🇹🇷 - Turkey
# 🇺🇿 - Uzbekistan"""
# emoji_description_commands = """
# /am - Armenia 🇦🇲
# /az - Azerbaijan 🇦🇿
# /be - Belgium 🇧🇪
# /bg - Bulgaria 🇧🇬
# /de - Germany 🇩🇪
# /ee - Estonia 🇪🇪
# /es - Spain 🇪🇸
# /fi - Finland 🇫🇮
# /fr - France 🇫🇷
# /uk - United Kingdom 🇬🇧
# /hr - Croatia 🇭🇷
# /hu - Hungary 🇭🇺
# /it - Italy 🇮🇹
# /lt - Lithuania 🇱🇹
# /lv - Latvia 🇱🇻
# /mt - Malta 🇲🇹
# /nl - Netherlands 🇳🇱
# /no - Norway 🇳🇴
# /pl - Poland 🇵🇱
# /pt - Portugal 🇵🇹
# /ro - Romania 🇷🇴
# /ru - Russia 🇷🇺
# /sa - Saudi Arabia 🇸🇦
# /si - Slovenia 🇸🇮
# /sk - Slovakia 🇸🇰
# /th - Thailand 🇹🇭
# /tr - Turkey 🇹🇷
# /uz - Uzbekistan 🇺🇿"""

# emoji_description_commands = "/{} - Armenia 🇦🇲\n/{} - Azerbaijan 🇦🇿\n/{} - Belgium 🇧🇪\n/{} - Bulgaria 🇧🇬\n/{} - Germany 🇩🇪\n/{} - Estonia 🇪🇪\n/{} - Spain 🇪🇸\n/{} - Finland 🇫🇮\n/{} - France 🇫🇷\n/{} - United Kingdom 🇬🇧\n/{} - Croatia 🇭🇷\n/{} - Hungary 🇭🇺\n/{} - Italy 🇮🇹\n/{} - Lithuania 🇱🇹\n/{} - Latvia 🇱🇻\n/{} - Malta 🇲🇹\n/{} - Netherlands 🇳🇱\n/{} - Norway 🇳🇴\n/{} - Poland 🇵🇱\n/{} - Portugal 🇵🇹\n/{} - Romania 🇷🇴\n/{} - Russia 🇷🇺\n/{} - Saudi Arabia 🇸🇦\n/{} - Slovenia 🇸🇮\n/{} - Slovakia 🇸🇰\n/{} - Thailand 🇹🇭\n/{} - Turkey 🇹🇷\n/{} - Uzbekistan 🇺🇿"

emoji_description_commands = """
/{} - Armenia 🇦🇲
/{} - Azerbaijan 🇦🇿
/{} - Belgium 🇧🇪
/{} - Bulgaria 🇧🇬
/{} - Germany 🇩🇪
/{} - Estonia 🇪🇪
/{} - Spain 🇪🇸
/{} - Finland 🇫🇮
/{} - France 🇫🇷
/{} - United Kingdom 🇬🇧
/{} - Croatia 🇭🇷
/{} - Hungary 🇭🇺
/{} - Italy 🇮🇹
/{} - Lithuania 🇱🇹
/{} - Latvia 🇱🇻
/{} - Malta 🇲🇹
/{} - Netherlands 🇳🇱
/{} - Norway 🇳🇴
/{} - Poland 🇵🇱
/{} - Portugal 🇵🇹
/{} - Romania 🇷🇴
/{} - Russia 🇷🇺
/{} - Slovenia 🇸🇮
/{} - Slovakia 🇸🇰
/{} - Thailand 🇹🇭
/{} - Turkey 🇹🇷
/{} - Uzbekistan 🇺🇿"""

def translate_current_text(to_translate: str,lang_to: str, lang_from: str) ->(str):
    # if lang_to!="en":
    # translator= Translator(to_lang=lang_to, from_lang=lang_from)
    translator= Translator(to_lang=lang_to, from_lang=lang_from,email=all_emails_holder[random.randint(0,len(all_emails_holder)-1)])
    # ,email="johnny_silverhand@gmail.com"
    # lt = LibreTranslateAPI("https://translate.argosopentech.com/")
    # return lt.translate(to_translate,"lv","en")
    # MYMEMORY WARNING: YOU USED ALL AVAILABLE FREE TRANSLATIONS FOR TODAY
    translated_text = translator.translate(to_translate)
    try:
        if "MYMEMORY WARNING: YOU USED ALL AVAILABLE FREE TRANSLATIONS FOR TODAY" not in translated_text:
            return translated_text
        else:
            return spare_translator(to_translate,lang_to,lang_from)
    except Exception as ex:
        print(ex)
        return spare_translator(to_translate,lang_to,lang_from)

    # else:
    #     return to_translate

def spare_translator(to_translate: str,lang_to: str, lang_from: str):
    print("WARNING! Spare translator was used!")
    if lang_from=="de":
        to_translate=to_translate.title()
    if lang_from=="en" and lang_to!="en":
        return ts.google(to_translate, from_language=lang_from, to_language=lang_to)
    elif lang_to=="en" and lang_from!="en":
        return ts.google(to_translate,  from_language=lang_from,to_language=lang_to)
    else:
        return to_translate
    
