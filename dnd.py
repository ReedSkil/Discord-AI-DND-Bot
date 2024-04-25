import os
import discord
import math
import random
import google.generativeai as genai
import google
from openai import OpenAI

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

geminiapi = "gemini api key here"
openai = "openai api key here"
token = "discord bot token here"


headadmin = "discord id here"
lesseradmin2 = "discord id here"

model = genai.GenerativeModel('gemini-pro', generation_config=genai.types.GenerationConfig(
            stop_sequences="|||",
            candidate_count=1,
            ))
genai.configure(api_key=geminiapi)

global_prompt = "You are the dungeon master for an infinite game of dnd! Read the entire backstory section of this prompt and write in detail but not over 4 paragraphs what happens to the character performing an action and their party. In this prompt is a theme of an event with a win or lose conditional that your response MUST be written about. formatted like so: damage 13 win. Do not write both a win and fail condition, only the one specified in the prompt. Also do not write the win or lose conditional in your response. Your job is to always keep the game going, but do not avoid making story arcs. Backstory: "
character_check = "You are a dungeon master for a game of DND and in charge of approving characters players wish to pick and YOU CAN ONLY SAY Approved or Reject. Be fair with your choice and make sure their options are not overpowered by your standards. For instance GOD is a reject. The Class is: "
character_skills = "You are a dungeon master for a game of DND and in charge of choosing the beginning skill values of a character class (integers from 1-20, 10 being the average person). Only respond with numbers with /'s in between for skills in this order: health/strength/intelligence/dexterity/charisma. The Class is: "
skill_theme_prompt = "Only respond in one singular word, your choices of word are as follows: damage, strength, inteligence, dexterity, or charisma. Read the following prompt and then respond with one of those words with a difficulty number (1-20) as what the player must roll against. No matter how irrelevant the prompt seems, always apply a category. Example: damage 13. prompt: "
summarize_story = "Read the entire backstory section of this prompt and ignore the rest, summarize every event that has happened. Include a section for each member of the ALIVE party members. "
characters = {}

def setGlobal_Prompt(new):
    global global_prompt
    global_prompt = new

class Character:

    def __init__(self, user_id, name, health, character_class, strength, intelligence, dexterity, charisma):
        self.user_id = user_id
        self.name = name
        self.health = health
        self.character_class = character_class
        self.strength = strength
        self.intelligence = intelligence
        self.dexterity = dexterity
        self.charisma = charisma

    def health(self):
        return self.health
    def strength(self):
        return self.strength
    def intelligence(self):
        return self.intelligence
    def dexterity(self):
        return self.dexterity
    def charisma(self):
        return self.charisma

    def take_damage(self, damage):
        self.health -= damage

    def heal(self, amount):
        self.health += amount


def generate_picture(prompt):
    prompt = truncate_string(prompt)
    gptclient = OpenAI(api_key=openai)
    response = gptclient.images.generate(
        model="dall-e-3",
        prompt=str(prompt),
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    print("--------------------------------")
    print(image_url)
    return image_url

def generate_response(user_prompt, predetermined_prompt):
    safety_settings = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

    combined_prompt = predetermined_prompt + user_prompt

    response = model.generate_content(combined_prompt, safety_settings=safety_settings)
    response.resolve()
    generated_string = response.text

    return generated_string

def get_party_members_string():
    party_members = []

    for character in characters.values():
        party_members.append(f"{character.name} the {character.character_class}")

    return ", ".join(party_members)

def check_files():
    desktop_path = os.path.join("C:\\Desktop")
    dnd_directory = os.path.join(desktop_path, "dnd")
    party_file = os.path.join(dnd_directory, "party.txt")
    story_file = os.path.join(dnd_directory, "story.txt")

    if not os.path.exists(dnd_directory):
        os.makedirs(dnd_directory)
        print("Directory 'dnd' created on desktop.")

    if not os.path.exists(party_file):
        with open(party_file, 'w') as f:
            f.write("Party Members:\n")
        print("File 'party.txt' created in 'dnd' directory.")

    if not os.path.exists(story_file):
        with open(story_file, 'w') as f:
            f.write("Story: \n global_prompt = You are the dungeon master for an infinite game of dnd! Write in detail but not over 4 paragraphs what happens to the character and their party. In this prompt is a theme of an event with a win or lose conditional that your response MUST be written about. formatted like so: damage 13 win. Do not write both a win and fail condition, only the one specified in the prompt. Also do not write the win or lose conditional in your response. Your job is to always keep the game going, but do not avoid making story arcs. Backstory: ")
        print("File 'story.txt' created in 'dnd' directory.")


def save(prompt):
    desktop_path = os.path.join("C:\\Desktop")
    dnd_directory = os.path.join(desktop_path, "dnd")
    party_file = os.path.join(dnd_directory, "party.txt")
    story_file = os.path.join(dnd_directory, "story.txt")

    with open(party_file, 'w') as f:
        f.write("Characters:\n")
        for user_id, character in characters.items():
            f.write(f"{user_id}:{character.name}:{character.character_class}:{character.health}:"
                    f"{character.strength}:{character.intelligence}:{character.dexterity}:{character.charisma}\n")

    print("Character data written to 'party.txt'.")

    print(os.path.exists(story_file))
    if os.path.exists(story_file):
        with open(story_file, 'w') as f:
            f.write(prompt)
        print("Global prompt written to 'story.txt'.")
    elif not os.path.exists(story_file):
        with open(story_file, 'w') as f:
            f.write(prompt)
        print("File 'story.txt' created in 'dnd' directory and global prompt written.")

def read():
    desktop_path = os.path.join("C:\\Desktop")
    dnd_directory = os.path.join(desktop_path, "dnd")
    party_file = os.path.join(dnd_directory, "party.txt")
    story_file = os.path.join(dnd_directory, "story.txt")

    characters.clear()
    with open(party_file, 'r') as f:
        lines = f.readlines()
        if len(lines) > 0 and lines[0].strip() == "Characters:":
            for line in lines[1:]:
                parts = line.strip().split(':')
                user_id = parts[0]
                name = parts[1]
                character_class = parts[2]
                health = int(parts[3])
                strength = int(parts[4])
                intelligence = int(parts[5])
                dexterity = int(parts[6])
                charisma = int(parts[7])
                characters[user_id] = Character(user_id, name, health, character_class, strength, intelligence, dexterity, charisma)
    print("Character data read from 'party.txt'.")

    global global_prompt
    if os.path.exists(story_file):
        with open(story_file, 'r') as f:
            global_prompt = f.read().strip()
        print("Global prompt retrieved from 'story.txt'.")
    else:
        print("File 'story.txt' does not exist.")

def skillcheck(character, skill, amount):
    health = int(character.health)
    strength = int(character.strength)
    intelligence = int(character.intelligence)
    dexterity = int(character.dexterity)
    charisma = int(character.charisma)
    if skill.lower() == "damage":
        return "lose"
    elif skill.lower() == "strength":
        roll = math.floor((int(strength)/2) - 5) + random.randint(1, 20)
        if roll >= amount:
            return "win"
        else:
            return "lose"
    elif skill.lower() == "inteligence" or skill.lower() == "intelligence":
        roll = math.floor((int(intelligence) / 2) - 5) + random.randint(1, 20)
        if roll >= amount:
            return "win"
        else:
            return " lose"
    elif skill.lower() == "dexterity":
        roll = math.floor((int(dexterity) / 2) - 5) + random.randint(1, 20)
        if roll >= amount:
            return "win"
        else:
            return "lose"
    elif skill.lower() == "charisma":
        roll = math.floor((int(charisma) / 2) - 5) + random.randint(1, 20)
        if roll >= amount:
            return "win"
        else:
            return "lose"
    else:
        print("Invalid roll. Please specify a valid skill (health, strength, intelligence, dexterity, charisma).")
        return "break"


def win_check(character, s):
    parts = s.split()

    damage_type = strip_spaces(parts[0])
    print(damage_type)
    damage_value = int(parts[1])
    return skillcheck(character, damage_type, damage_value)


def string_split(s):
    midpoint = len(s) // 2

    part1 = s[:midpoint]
    part2 = s[midpoint:]

    return part1, part2

def string_strip(s):
    parts = s.split()

    damage_type = parts[0]
    return damage_type

def strip_spaces(input_string):
    return ''.join([char for char in input_string if char != ' '])

def truncate_string(input_string):
    if len(input_string) > 1000:
        truncated_string = input_string[:1000]
        return truncated_string
    else:
        return input_string

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    check_files()
    read()

async def handle_ai(message, character, global_prompt, action):
    input_msg = message.content
    user_prompt = input_msg[len("!"):].strip()
    user_prompt = f"{character.name} will {user_prompt}"
    print(f"{user_prompt}: {global_prompt}")

    try:
        check = generate_response(user_prompt, skill_theme_prompt)
    except google.api_core.exceptions.InternalServerError as e:
        await message.channel.send(f"An internal server error occurred with Google. Please Try Again")
    print(f"skill check = {check}")
    try:
        win = win_check(character, check)
        print(f"win = {win}")
        if win != "" and win != "break":
            user_prompt = f"{character.name} {action} {user_prompt} and it results in a {check}. Your prompt should focus heavily on this character and their actions (but not limited to this character). DO NOT KILL ANY MEMBERS IN THE PARTY THIS IS REALLY IMPORTANT, but feel free to knock them out or wound them heavily."
            check = check + win
            prompt = str(
                f"{global_prompt} Party: {get_party_members_string()} /// AI:")
            ai_response = generate_response(prompt, user_prompt)
            print(f"skill check = {ai_response}")
            global_prompt = global_prompt + ai_response
            print("Response: " + ai_response)
            try:
                await message.channel.send(ai_response)
            except:
                part1, part2 = string_split(ai_response)
                await message.channel.send(part1)
                await message.channel.send(part2)
            win = strip_spaces(win)
            print("---------------------------")
            print(win)
            if win.lower() == "win":
                await message.channel.send(f"you won a {string_strip(check)} roll")
            else:
                roll = string_strip(check)
                if roll.lower() == "damage":
                    damage = random.randint(1, 20)
                    character.take_damage(damage)
                    await message.channel.send(f"{character.name} took {damage} damage")
                else:
                    await message.channel.send(f"{character.name} lost a {roll} roll")
                    damage = random.randint(1, 10)
                    character.take_damage(damage)
                    if roll.lower() == "charisma":
                        await message.channel.send(f"you lost {damage} respect")
                    elif roll.lower() == "inteligence" or roll.lower() == "intelligence" :
                        await message.channel.send(f"you lost {damage} brain cells")
                    elif roll.lower() == "strength":
                        await message.channel.send(f"you lost {damage} pounds (and gained {damage} bruises)")
                    elif roll.lower() == "dexterity":
                        await message.channel.send(f"you lost {damage} flexible muscles")

                if character.health <= 0:
                    temp_prompt = str(f"{global_prompt}. {character.name} Died, Your response should detail how. ")
                    ai_response = generate_response(f"{character.name}'s player has decided to end their character.", temp_prompt)
                    await message.channel.send(ai_response)
                    del characters[str(message.author.id)]
                    await message.channel.send(f"{character.name} DIED")
                    await message.channel.send("Character deleted, make a new character to continue")
                    global_prompt = global_prompt + ai_response
                print(f"prompt = {global_prompt}")
                save(global_prompt)
        else:
            print("BREAK")
            await message.channel.send(
                "Oops, the AI broke on that last request. Try again or say a different action")
    except:
        await message.channel.send(
            "Oops DM couldnt find a skill for that request. Try again or say a different action")
    return ai_response

action_lock = False
picture = False

@client.event
async def on_message(message):
    global action_lock
    global global_prompt
    global picture

    if message.author == client.user or message.channel.name != 'baldurs-gate-4':
        return

    user_id = str(message.author.id)

    if action_lock:
        await message.channel.send(f"<@{message.author.id}> , another action was being processed. Try again.")
        return


    try:
        if user_id not in characters:
            if message.content.startswith('!create'):
                await create_character(message, global_prompt)
            if message.content.startswith('!'):
                await message.channel.send(f"{message.author}, you don't have a character")
        else:
            character = characters[user_id]
            if message.content.startswith('!status'):
                await message.channel.send(
                    f"Name: {character.name}\nClass: {character.character_class}\nHealth: {character.health}\nStrength: {character.strength}\nIntelligence: {character.intelligence}\nDexterity: {character.dexterity}\nCharisma: {character.charisma}\n")
            action_lock = True
            if message.content.startswith('!delete character heartlessly'):
                character.take_damage(1000)
                temp_prompt = str(f"{global_prompt}. {character.name} Died, Your response should detail how. ")
                ai_response = generate_response(f"{character.name}'s player has decided to end their character.", temp_prompt)
                await message.channel.send(ai_response)
                del characters[str(message.author.id)]
                await message.channel.send(f"{character.name} DIED")
                await message.channel.send("Character deleted, make a new character to continue")
                global_prompt = global_prompt + ai_response
                print(f"prompt = {global_prompt}")
                save(global_prompt)
            elif message.content.startswith('!test'):
                await message.channel.send(characters[str(message.author.id)])
            elif message.content.startswith("!picture") and str(message.author.id) == headadmin:
                if picture:
                    picture = False
                    await message.channel.send("Pictures Will Stop Generating")
                else:
                    picture = True
                    await message.channel.send("Pictures Will Start Generating")
            elif message.content.startswith('!party'):
                await message.channel.send(get_party_members_string())
            elif message.content.startswith('!reset') and (str(message.author.id) == headadmin or str(message.author.id) == lesseradmin2):
                global_prompt = "You are the dungeon master for an infinite game of dnd! Write in detail but not over 4 paragraphs what happens to the character and their party. In this prompt is a theme of an event with a win or lose conditional that your response MUST be written about. formatted like so: damage 13 win. Do not write both a win and fail condition, only the one specified in the prompt. Also do not write the win or lose conditional in your response. Your job is to always keep the game going, but do not avoid making story arcs. Backstory: "
                save(global_prompt)
                await message.channel.send("Campaign Reset")
            elif message.content.startswith('!save'):
                save(global_prompt)
                await message.channel.send("Campaign Saved")
            elif message.content.startswith('!story'):
                await message.channel.send("Summarizing Campaign, one moment: ")
                print(global_prompt)
                story_prompt = summarize_story + "ALIVE MEMBERS: " + get_party_members_string() + "|| "
                story = generate_response(story_prompt, global_prompt)
                try:
                    await message.channel.send(story)
                except:
                    try:
                        story1 = string_split(story)
                        story2 = string_split(story)
                        await message.channel.send(story1)
                        await message.channel.send(story2)
                    except:
                        await message.channel.send("Failed to print Story")
            elif message.content.startswith('!say'):
                action = "says"
                response = await handle_ai(message, character, global_prompt, action)
                try:
                    if picture:
                        image = generate_picture(response)
                        await message.channel.send(image)
                except:
                    await message.channel.send("*Failed to Generate Picture*")
            elif message.content.startswith('!go'):
                action = "will"
                response = await handle_ai(message, character, global_prompt, action)
                try:
                    if picture:
                        image = generate_picture(response)
                        await message.channel.send(image)
                except:
                    await message.channel.send("*Failed to Generate Picture*")
    finally:
        action_lock = False


async def create_character(message, prompt):
    await message.channel.send("Let's create your character!")
    await message.channel.send("What's your character's name?")
    name_response = await client.wait_for('message', check=lambda m: m.author == message.author)
    name = name_response.content
    while True:
        await message.channel.send("What's your character's class?")
        class_response = await client.wait_for('message', check=lambda m: m.author == message.author)
        character_class = class_response.content
        check = generate_response(class_response.content + "||| Approved, or Reject:", character_check)
        print(check)
        if check.startswith("Approved"):
            break
        else:
            await message.channel.send("Rejected: try again")
    stats = generate_response(class_response.content, character_skills)
    print(stats)

    substrings = stats.split('/')
    integers = [int(substring) for substring in substrings]

    health, strength, intelligence, dexterity, charisma = integers

    characters[str(message.author.id)] = Character(str(message.author.id), name, 100, character_class, strength, intelligence, dexterity, charisma)
    await message.channel.send("Character created successfully!")
    save(prompt)

client.run(token)