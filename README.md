OriBot - Bot Assistant
OriBot ir inteliģents robots asistents, kas izstrādāts, lai vienkāršotu jūsu ikdienas uzdevumus un sniegtu noderīgu informāciju. Tas piedāvā vairākas funkcijas, kas var uzlabot jūsu produktivitāti un nodrošināt ērtības. Izpētīsim OriBot galvenās funkcijas:



Funkcijas:
📝 Darāmā plānošana
OriBot ļauj jums viegli pārvaldīt savus uzdevumus un efektīvi plānot savu dienu. Jūs varat izveidot darāmo darbu sarakstu, noteikt termiņus un noteikt prioritātes uzdevumiem. Bots palīdzēs jums būt organizētam un nodrošinās, lai jūs nepalaistu garām nevienu svarīgu termiņu.

⛅️ Informācija par laikapstākļiem
Ar OriBot pastāvīgi saņemiet jaunāko informāciju par laikapstākļiem jebkurā vietā. Vienkārši norādiet botam vēlamo atrašanās vietu, un tas iegūs un parādīs aktuālo laikapstākļu informāciju, tostarp temperatūru, mitrumu, vēja ātrumu un daudz ko citu. Šī funkcija var palīdzēt jums attiecīgi plānot aktivitātes brīvā dabā.

💬 Čatošana ar mākslīgo intelektu
Iesaistieties sarunās ar OriBot mākslīgā intelekta iespējām. Botam ir dabiskās valodas apstrādes funkcija, un tas spēj saprast un atbildēt uz jūsu jautājumiem. Neatkarīgi no tā, vai vēlaties uzdot vispārīgu jautājumu, lūgt padomu vai iesaistīties sarunā, OriBot ir gatavs jums palīdzēt.



Bota darbošana:
Faili oribot_main.py satur galveno kodu, kas atbild par mijiedarbību ar robotu. Šis fails koordinē izsaukumus uz citiem failiem un funkcijām, lai veiktu konkrētus uzdevumus.

Lietotāja klase glabā informāciju par lietotāju. Šī klase var saturēt dažādus atribūtus, piemēram, vārdu, vecumu, e-pasta adresi u. c., kas var būt noderīgi, apstrādājot lietotāja pieprasījumus un sniedzot atbilstošas atbildes.

Turklāt lietotāja informāciju var glabāt Excel failā, ko izmanto kā datubāzi. Excel failā var būt dažādas lapas vai tabulas lietotāja informācijas glabāšanai.

No citiem failiem importētās funkcijas veic īpašus uzdevumus, kas saistīti ar lietotāju pieprasījumu apstrādi vai mijiedarbību ar datubāzi. Piemēram, var būt funkcija, lai pārbaudītu, vai lietotājs ir datubāzē, funkcija, lai datubāzē pievienotu jaunu lietotāju, vai funkcija, lai atjauninātu lietotāja informāciju.

Būtībā oribot_main.py ir bota ieejas punkts, un pārējos failos ir palīgfunkcijas un klases, kas nepieciešamas bota darbināšanai un lietotāja informācijas pārvaldīšanai.



Bota izmantošana:
Lai palaistu robotu, izpildiet tālāk sniegtos norādījumus:
1) Sekojiet saitei https://t.me/oriibbot, kas ved uz Telegram botu.

2) Atvērtajā čata logā noklikšķiniet uz "Start" vai ievadiet komandu "/start". Tas ļaus botam zināt, ka vēlaties, lai sākas mijiedarbība.

3) Pēc komandas /start nosūtīšanas robots var jūs sveikt un sniegt norādījumus par to, kā izmantot tā funkcionalitāti.

4) Ievērojiet bota norādījumus un ievadiet nepieciešamo informāciju vai komandas teksta lodziņā, lai sazinātos ar to.



Bota visas funkcijas:
/change_lang - mainīt valodu

/promo_code - lai izmantotu akcijas kodu

/buy_premium - lai atjauninātu kontu uz Premium

/weather - laikapstākļu funkcija

/planner - plānotāja funkcija

/all_lang - visas pieejamās valodas

/region - lai manuāli ievadītu atrašanās vietu 

/schedule_forecast - ieplānot laikapstākļu prognozi

/new_forecast_event - lai iestatītu jaunu prognozes notikumu

/remove_forecast_event - lai noņemtu prognozes notikumu

/all_forecast_events - lai skatītu visus prognozes notikumus

/every_day_event - lai plānotu katras dienas notikumu

/new_every_eady_day_event - lai iestatītu jaunu katras dienas notikumu

/remove_every_day_event - lai noņemtu katras dienas notikumu

/all_every_every_day_events - lai skatītu visus katras dienas notikumus

/specific_event - lai ieplānotu konkrētu notikumu

/new_specific_event - lai iestatītu jaunu konkrētu notikumu

/remove_specific_event - lai noņemtu katras dienas notikumu

/all_specific_events - lai skatītu visus katras dienas notikumus



Autori:

Timurs Jerčaks - timurs.jercaks@gmail.com

Ivans Minajevs - minajevsivans@gmail.com



