# ollama_tg_bot
Telegram bot, receive messages from channel, use Ollama to comment events



Бот сделан для оживления сообщений умного дома, которые направляются в частный телеграм канал - показания датчиков, погода, уведомления и т.д.



бот подключается к локально развернутой Ollama,  передает сообщение из канала и получает ответ - шутку с комментарием случившегося.



код написан с помощью LLM, поэтом неоптимальный, содержит кучу отладок и т.д., но работает





следующие шаги:



убрать лишнюю генерацию при тесте подключения, Проверка доступности модели более простое



добавить эмоции - расстроенный, агрессивный и т.д.выбирать случайно



формирование модели в функционале бота (задлать system, выбрать модель - источник)



текст запроса (comment with hiumor) промпт или для модели в сообщении или в .env



Исправить выбор модели



Добавить выбор температуры



Сделать контроль длины ответа не меньше 5-7 предложений. В системный промпт??


Генерировать ответы на английском, потом как то переводить - найти нормальный api



Случайная шутка про обитателей раз в ХХ минут??



Уменьшить логгирование
доработать системный промпт - сделать более структурированным - комнаты и животные, чтобы было более раздельно и LLM не путалась в комнатах и обитателях)
