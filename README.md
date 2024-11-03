# Бот - комментатор
**Telegram bot, receives messages from channel, use Ollama to comment events**

**Бот сделан для оживления сообщений умного дома, которые направляются в частный телеграм канал - показания датчиков, погода, уведомления и т.д.**

**бот подключается к локально развернутой Ollama, передает сообщение из канала и получает ответ - шутку с комментарием случившегося.**

_код написан с помощью LLM, поэтому неоптимальный, содержит кучу отладок и т.д., но работает_

Важно:
Бот должен быть администратором каналов (и откуда берет сообщения, и куда направляет). У меня это один и тот же канал, поэтому, чтобы бот не стал сам с собой болтать и бесконечно коммпентировать, в код добавлена проверка, если сообщение начинается со знака 📢, то такие сообщения не обрабатываются. соответственно, все сообщения от бота начинаю с такого символа.


Реализация через Docker, так как в дальнейшем задумывалось упрощение разворачивания на сервере, если в docker-compose добавлять еще и Ollama, однако, пока работает отдельно

переименуйте example.env в .env и заполните переменные в .env файле - 

BOT_TOKEN=  # токен телеграм бота - возьмите у Bot Father

OWNER_ID=  # телеграм Id хозяина бота - заготовка под дальнейшее управление ботом, пока ни на что не влияет


FORWARD_TO_CHANNEL=  # id канала, куда отправлять сообщения 

FORWARD_FROM_CHANNEL=  # id канала, откуда будет забирать сообщения

ollama_url =   # адрес локально развернутой ollama - обычно (если на том же ПК - 'http://localhost:11434', порт 11434) (пока прописано жестко в коде)




все заполняется без кавычек (одинарных и двойных - вообще без всех кавычек)

обратите внимание, каналы в телеграмме начинаются с "-100", узнать Id канала и свой id в телеграмме можно направив сообщение (или переслав его из канала) в бот Get my id

запускается через сборку контейнера (**docker compose up --build -d**)

затем просто **docker compose up -d** (лениво мне выкладывать на docker hub образ)



Ollama:

https://ollama.com/ - проект Ollama

https://ollama.com/library - тут брать модели

у меня все крутится в Proxmox, развернутый контейнер с Docker

![image](https://github.com/user-attachments/assets/cde517d3-1363-4c5c-8653-0cb98590ca28)



поэтому, модели больше 7b если и влазят, то генерация идет очень медленно и печально, поэтому использую максимально 7b (меньшие - тупые). генерация идет секунд 30, я пока в экспериментах, какие настройки использовать - длину контекста, глубину разговора и т.д.


**ВАЖНО**: чтобы больше персонализировать комментарии "Ассистента", я сделал новую модель, как указано здесь https://github.com/ollama/ollama/blob/main/docs/modelfile.md

я создал Modelfile, в котором указал за исходную модель llama3.1 (3.2 не очень, так как пока 3b), затем в System большую строку с описанием дома, обитателей:

_you are a smart home assistant - an apartment with several rooms.
Bedroom - there are sensors, as well as a terrarium with frogs, with a built-in sensor. frogs - litoria, called Athos, Porthos and Aramis.
A warm shelf is on the balcony and turns on and off every five minutes so as not to overheat.
to. Liza - this is Liza's room - the daughter of the owners of the apartment, she is 18 years old and she is currently studying in Seoul, at a university and does not live with her parents.
In her room there is also a terrarium in which a eublefar named Glada lives. This is a lizard girl. She likes to sit in her house or climb out to warm up on a special heated stone. Also in Liza's room there is a box with woodlice, which live like pets. out of several hundred pieces, there are orange ones, and there are gray ones.
In the hall there is a separate temperature and humidity sensor. There is also a computer case in the room, in which there are several minicomputers, this is called a "server", and it also has its own temperature and humidity sensor. There are also aquariums with shrimp in the room. The shrimp are blue and red, they are also several years old. The other rooms - the kitchen, the hallway, the bathroom, the balcony - are ordinary, there is nothing particularly interesting there. The family also has a cat named Kosya. She is a British breed and very independent, does not like to be petted and comes only when it is interesting, but sometimes, when no one is home, she gets bored and runs home and meows loudly - looking for her owners.
use this information to diversify jokes about the activation of sensors.
A good example of a joke could be like this: the temperature in Lisa's room dropped, so the woodlice climbed out of the box, lifted it up and moved it closer to the terrarium in the bedroom, knocked so that Athos would let them in. Comment on these circumstances, taking into account the requirements for humor and description of the house._

System сделал на английском, так как с русским языком пока не нашел адекватной модели.

так же, вывод пока  она тоже на английском языке (пока в работе с переводом), ну или найду нормальную русскоязычную модель

соответственно, собрав модель (собирается мгновенно, видимо, какие то механизмы простые используются, чтобы верхом дописать информацию), называется "assistant" - в дальнейшем планируется выбор, сборку модели делать через бота




# Примеры:

сообщение в канале:

**В коридоре горит свет уже 2 минут. Кто-то долго не выключает!**


ответ:

📢 ВНИМАНИЕ 

🤖 Комментарий вУмного дома:

😅 Ahahahaha! Looks like someone's having a Sunday Funday 🤣... but not me, the sensor assistant 😜!


"Uh-oh, the hallway light has been on for TWO whole minutes?!" 😳 I'm shocked! 👀 Someone must have come home from that long weekend and forgotten to turn off the lights 💡. Or maybe it's just Kosya trying to brighten up the day with her usual 'meow-I'm-bored' vibes 🐈.


On a more serious note, though (just for a sec 😊), I should probably remind someone to switch it off to save some energy and prevent any unexpected light bulb failures 🔌. But for now, let's just enjoy this little comedic interlude 😉!




еще событие (каждый час уведомление о погоде снаружи):

**Сейчас на улице: 
           Облачно ⛅️              
 Температура: 0.7 °C 
 Скорость ветра: 2.08 м/с**


Ответ:


📢 ВНИМАНИЕ 

🤖 Комментарий вУмного дома:

Breaking news! 
🚨 Just received a distress signal from the great outdoors... aka Liza's mom is freezing her butt off outside ☁️. Temperature reading: a whopping -0.3°C ❄️ (or 32.7°F for our American friends 😅). And to make matters worse, a gentle breeze of 2.08 m/s (4.6 mph) is making it feel like she's being tickled by the wind 🤣.


I'm sending out a team of thermometers and wind meters to assist her in this crisis. And also, warning Athos, Porthos, and Aramis in the terrarium: no partying with the isopods today - it's cold outside, stay inside! 😂



**следующие шаги:**

* [ ]  убрать лишнюю генерацию при тесте подключения, Проверка доступности подключения более простое
* [ ]  добавить эмоции - расстроенный, агрессивный и т.д.выбирать случайно
* [ ]  формирование модели в функционале бота (задать system, выбрать модель - источник)
* [ ]  текст запроса (comment with humor) промпт или для модели в сообщении или в .env
* [ ]  Исправить выбор модели
* [ ]  удаление моделей
* [ ]  Добавить выбор температуры
* [ ]  Сделать контроль длины ответа не меньше 5-7 предложений. В системный промпт??
* [ ]  Генерировать ответы на английском, потом как то переводить - найти нормальный api
* [ ]  Случайная шутка про обитателей раз в ХХ минут??
* [ ]  Уменьшить логгирование доработать системный промпт - сделать более структурированным - комнаты и животные, чтобы было более раздельно и LLM не путалась в комнатах и обитателях)
