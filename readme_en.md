# Bot - commentator 
**Telegram bot, receives messages from the channel, uses Ollama to comment on events** 
**The bot is made to trigger smart home messages that are sent to a private telegram channel - providing sensors, weather, notifications, etc.* *
**bot uses locall  Ollama, transmits a message from the channel and receives a response - there was a joke with a comment.** 
_the code is written using LLM, so it is not optimal, contains debug notifications, etc., but it works_ 

Important: The bot must be running as an administrator (both where it gets messages from and where it sends them to). For me, this is the same channel, so that the bot does not start chatting with itself and commenting endlessly, a check is added to the code: if the message begins with the 📢 sign, then such messages are not processed. Indeed, all messages from the bot begin with such a symbol.

Implementation via Docker, since in the future the deployment of the circuit has been simplified if Ollama is added to docker-compose, but for now it works separately 
rename example.env to .env and fill in the variables in the .env file 

BOT_TOKEN= # Telegram bot token - take from Bot Father 

OWNER_ID= # Telegram Id of the bot owner - a blank for further bot, does not affect anything yet 

FORWARD_TO_CHANNEL= # channel id where to send messages 

FORWARD_FROM_CHANNEL= # channel id from where it will pick up messages 

ollama_url = # local ollama reverse address - usually (if on the same PC - 'http://localhost:11434', port 11434) (for now it is hardcoded in the code) 

everything is created without quotes (single and double - without any quotes at all) note, channels in telegram start with "-100", you can find out the channel ID and your ID in Telegram by sending a message (or forwarding it from the channel) to the bot Get my ID 
is launched through the container assembly (** docker Compose Up --build -d**), 
and then just ** docker Compose Up -d** (I'm too lazy to upload to the Docker Hub image) 

# Ollama: 
https://ollama.com/ - Ollama project 

https://ollama. com/library - I get the models here, 

everything runs in Proxmox for me, 
Advanced container with Docker! 
[image] (https://github.com/user-attachments/assets/cde517d3-1363-4c5c-8653-0cb98590ca28) 

therefore, models larger than 7b, if they fit, the generation is very slow and sad, so they use a maximum of 7b (smaller ones are stupid). 
generation takes about 30 seconds, while I'm experimenting, what settings are used - context size, conversation input, etc.

**IMPORTANT**: 
to more personalize the "Assistant" comments, I made a new model, as indicated here 
https://github.com/ollama/ollama/blob/main/docs/modelfile.md, 
I created a Modelfile, which specifies the original model llama3.1 (3.2 is not very good, since it is 3b for now), then in the system large text with a description of the house, the inhabitant: _you are a smart home assistant - an apartment with several rooms.
Bedroom - there are sensors, as well as a terrarium with frogs, with a built-in sensor. frogs - litoria, called Athos, Porthos and Aramis.
A warm shelf on the balcony and turns on and off every five minutes so as not to overheat.
k. Lisa - this is the room of Lisa - the daughter of the owners of the apartment, she is 18 years old and she is currently studying in Seoul, studying at the university and does not live with her parents.
In her room there is also a terrarium in which lives a eublefar named Glada. This is a girl lizard. She likes to sit in her house or climb out to warm up on a special heated stone. Also in Lisa's room there is a box with woodlice that live as pets. out of several hundred pieces, there are orange ones, and there are gray ones.
In the hall there is a separate temperature and humidity sensor. There is also a computer case in the room, in which there are several minicomputers, this is called a "server", and it also has its own temperature and humidity sensor. Also in the room there are aquariums with shrimp. The shrimp are blue and red, they are also several years old. The other rooms - the kitchen, the hallway, the bathroom, the balcony - are ordinary, there is nothing particularly interesting there. The family also has a cat named Kosya. She is a British breed and very independent, does not like to be petted and comes only when she is interested, but sometimes, when no one is home, she gets bored and runs home and meows loudly - looking for her owners.
use this information to diversify jokes about activating sensors.
A good example of a joke could be like this: the temperature in Lisa's room dropped, so the woodlice climbed out of the box, lifted it and moved it closer to the terrarium in the bedroom, knocked so that Athos would let them in. Comment on these circumstances, taking into account the requirements for humor and description of the house._

The system is made in English, since I have not yet found an adequate model for the Russian language.

also, the conclusion is that for now it is also in English (still in the works with the translation), or I will find a normal Russian-language model accordingly

accordingly, having assembled the model (it is assembled instantly, apparently, some simple mechanisms are used to add information on top), it is called "assistant" - in the future it is planned to choose, to assemble the model through a bot

# Examples:

**message in channel:**

The hallway light has been on for 2 minutes. Someone has been leaving it on for a long time!

**reply:**

📢 ATTENTION

🤖 Comment in Smart Home:

😅 Ahahahaha! Looks like someone's having a Sunday Funday 🤣... but not me, the sensor assistant 😜!

"Uh-oh, the hallway light has been on for TWO whole minutes?!" 😳 I'm shocked! 👀 Someone must have come home from that long weekend and forgotten to turn off the lights 💡. Or maybe it's just Kosya trying to brighten up the day with her usual 'meow-I'm-bored' vibes 🐈.

On a more serious note, though (just for a sec 😊), I should probably remind someone to switch it off to save some energy and prevent any unexpected light bulb failures 🔌. But for now, let's just enjoy this little comedic interlude 😉!

**Another event (every hourly weather notification outside):**

Currently outside: Cloudy ⛅️
Temperature: 0.7 °C Wind speed: 2.08 m/s

**Answer:**

📢 ATTENTION

🤖 Comment in Smart Home:

Breaking news! 🚨 Just received a distress signal from the great outdoors... aka Liza's mom is freezing her butt off outside ☁️. Temperature reading: a whopping -0.3°C ❄️ (or 32.7°F for our American friends 😅). And to make matters worse, a gentle breeze of 2.08 m/s (4.6 mph) is making it feel like she's being tickled by the wind 🤣.

I'm sending out a team of thermometers and wind meters to assist her in this crisis. And also, warning Athos, Porthos, and Aramis in the terrarium: no partying with the isopods today - it's cold outside, stay inside! 😂

# Next steps:

* [ ]  Remove unnecessary generation during connection test, Checking connection availability is simpler
* [ ] Add emotions - upset, aggressive, etc., choose randomly
* [ ] Formation of a model in the bot functionality (set system, select model - source)
* [ ] Query text (comment with humor) prompt or for a model in a message or in .env
* [ ] Correct model selection
* [ ] Removing models
* [ ] Add temperature selection
* [ ] Make response length control at least 5-7 sentences. In the system prompt??
* [ ] Generate responses in English, then somehow translate - find a normal api
* [ ] Random joke about inhabitants once every XX minutes??
* [ ] Reduce logging, improve the system prompt - make it more structured - rooms and animals, so that it is more separate and LLM does not get confused in rooms and inhabitants)
