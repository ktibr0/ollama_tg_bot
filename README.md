# описание бота - комментатора
**Telegram bot, receive messages from channel, use Ollama to comment events**

**Бот сделан для оживления сообщений умного дома, которые направляются в частный телеграм канал - показания датчиков, погода, уведомления и т.д.**

**бот подключается к локально развернутой Ollama, передает сообщение из канала и получает ответ - шутку с комментарием случившегося.**

_код написан с помощью LLM, поэтом неоптимальный, содержит кучу отладок и т.д., но работает_



Реализация через Docker, так как в дальнейшем задумывалось упрощение разворачивания на сервере, если в docker-compose добавлять еще и Ollama, однако, пока работает отдельно
переименуйте .env.example в .env и заполните переменные в .env файле - 

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


поэтому, модели больше 7b если и влазят, то генерация идет очень медленно и печально, поэтому использую максимально 7b (меньшие - тупые)
важно: чтобы больше персонализировать комментарии "Ассистента", я сделал новую модель, как указано здесь https://github.com/ollama/ollama/blob/main/docs/modelfile.md
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
