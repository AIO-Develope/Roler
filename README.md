<h1 align="center">
    Roler
    <br>
    <div align="center">
    <img src="https://img.shields.io/badge/Python-3.10.6-blue" align="center"/>
    <img src="https://img.shields.io/badge/discord.py-2.2.3-green" align="center"/>
    <img src="https://img.shields.io/badge/Developing-Active-brightgreen" align="center"/>
    <img src="https://img.shields.io/badge/Version-3.0-green" align="center"/>
    </div>
</h1>

This is a Discord bot implemented using the Discord.py library. The bot is designed to manage roles within a Discord server through commands. The commands can only be executed by users with specific "chef" roles, which can be configured.

# Commands

Syntax:


<img src="https://raw.githubusercontent.com/AIO-Develope/roler/main/images/cmd.PNG" width="40%" height="40%"/>

# How to install


1. install required packages
```
pip install -r requirements.txt
```
2. edit config.json with youre informations
```
{
    "token": "TOKEN HERE",

    "prefix": "!",
    "enable-prefix-commands": false/true
}
```
3. edit roles.json to youre prefered settings, here is an example:
```
{
    "chef_roles": {
      "chef1": the_id_of_chef1_role
      "chef2": the_id_of_chef2_role
    },
    "roles": {
      "role1": the_id_of_role1_role
      "role2": the_id_of_role2_role
    },
    "assignable_roles": {
      "chef1": ["role1"]           // this means chef1 is able to give role1 trough this command
      "chef2": ["role1", "role2"]  // this means chef2 is able to give role1 and role2 trough this command
    }
}
  
```
4. now you can start the bot with
```
python main.py
```

# Info
i made this bot on behalf of a discord project

This project is pretty new, its more like a pre alpha but its working.
