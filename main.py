import discord
from discord.ext import commands
from discord import app_commands

import json

intents = discord.Intents.default()
intents.members = True
intents.message_content = True





def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


data = load_data('roles.json')


chef_roles = data['chef_roles']


roles = data['roles']


assignable_roles = data['assignable_roles']

with open("config.json", "r") as config_file:
    config = json.load(config_file)

TOKEN = config["token"]
PREF_STATE = config["enable-prefix-commands"]
PREFIX = config["prefix"]

if PREF_STATE == False:
    prefix = "jf8793fjdifz748hdjkflz7u8sdu"
elif PREF_STATE == True:
    prefix = PREFIX
else:
    print("error mit prefix")


bot = commands.Bot(command_prefix=prefix, intents=intents)

@bot.event
async def on_ready():
    print(f'Angemeldet als {bot.user.name}')
    
    await bot.tree.sync()
    
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        error_embed = discord.Embed(
            title='Fehler',
            description='Es fehlen erforderliche Argumente für den Befehl.',
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
    elif isinstance(error, commands.CommandInvokeError):
        error_embed = discord.Embed(
            title='Fehler',
            description='Es ist ein Fehler aufgetreten. Bitte überprüfe die verwendeten Parameter.',
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
    elif isinstance(error, commands.MemberNotFound):
        error_embed = discord.Embed(
            title='Fehler',
            description='Das angegebene Mitglied wurde nicht gefunden.',
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)
    else:
        error_embed = discord.Embed(
            title='Fehler',
            description='Ein unbekannter Fehler ist aufgetreten.',
            color=discord.Color.red()
        )
        await ctx.send(embed=error_embed)


@bot.hybrid_command()
async def hilfe(ctx):
    embed = discord.Embed(
        title='Hilfe: Rollenverwaltung',
        description='Verwende den Befehl `/role` zum Hinzufügen oder Entfernen von Rollen für Mitglieder.',
        color=discord.Color.blue()
    )
    embed.add_field(
        name='Syntax:',
        value='```\n/role add/remove [Rollenname] @[Mitglied]\n```',
        inline=False
    )
    
    roles_text = ""
    for chef_role, assignable_role_list in assignable_roles.items():
        chef_name = ctx.guild.get_role(chef_roles[chef_role])
        if chef_name is not None:
            chef_name = chef_name.name
            roles_assigned = ", ".join([role.capitalize() for role in assignable_role_list])
            roles_text += f'**{chef_name}:** {roles_assigned}\n'

    embed.add_field(
        name='Chef-Rollen und zugeordnete Rollen:',
        value=roles_text if roles_text else 'Keine Chef-Rollen vorhanden.',
        inline=False
    )

    await ctx.send(embed=embed)


@bot.hybrid_command()
async def role(ctx, aktion, rolle: str = None, member: discord.Member = None):
    error_embed = discord.Embed(
        title='Fehler',
        color=discord.Color.red()
    )

    if not rolle or not member:
        error_embed.description = 'Fehlende Parameter. Bitte verwende den Befehl wie folgt: `!role add/remove [Rollenname] @[Mitglied]`.'
        await ctx.send(embed=error_embed)
        return

    if aktion.lower() not in ['add', 'remove']:
        error_embed.description = 'Ungültige Aktion. Gültige Aktionen sind "add" und "remove".'
        await ctx.send(embed=error_embed)
        return

    if rolle.lower() not in roles:
        error_embed.description = 'Ungültige Rolle. Bitte gib eine gültige Rolle an.'
        await ctx.send(embed=error_embed)
        return

    try:
        role_id = roles[rolle.lower()]
        role_obj = ctx.guild.get_role(role_id)

        if aktion.lower() == 'add':
            for chef_role, assignable_role_list in assignable_roles.items():
                if ctx.author.top_role.id == chef_roles[chef_role]:
                    if role_id in [roles.get(assignable_role.lower()) for assignable_role in assignable_role_list]:
                        await member.add_roles(role_obj)
                        success_embed = discord.Embed(
                            title='Rolle hinzugefügt',
                            description=f'Die Rolle {role_obj.name} wurde {member.name} hinzugefügt.',
                            color=discord.Color.green()
                        )
                        await ctx.send(embed=success_embed)
                        return

                    error_embed.description = 'Die angegebene Rolle kann nicht zugewiesen werden.'
                    await ctx.send(embed=error_embed)
                    return

            error_embed.description = 'Du hast keine Berechtigung, diese Rolle zuzuweisen.'
            await ctx.send(embed=error_embed)

        elif aktion.lower() == 'remove':
            for chef_role, assignable_role_list in assignable_roles.items():
                if ctx.author.top_role.id == chef_roles[chef_role]:
                    if role_id in [roles.get(assignable_role.lower()) for assignable_role in assignable_role_list]:
                        await member.remove_roles(role_obj)
                        success_embed = discord.Embed(
                            title='Rolle entfernt',
                            description=f'Die Rolle {role_obj.name} wurde von {member.name} entfernt.',
                            color=discord.Color.green()
                        )
                        await ctx.send(embed=success_embed)
                        return

                    error_embed.description = 'Die angegebene Rolle kann nicht entfernt werden.'
                    await ctx.send(embed=error_embed)
                    return

            error_embed.description = 'Du hast keine Berechtigung, diese Rolle zu entfernen.'
            await ctx.send(embed=error_embed)

    except Exception as e:
        print(e)
        unknown_error_embed = discord.Embed(
            title='Unbekannter Fehler',
            description='Es ist ein unbekannter Fehler aufgetreten.',
            color=discord.Color.red()
        )
        await ctx.send(embed=unknown_error_embed)

bot.run(TOKEN)
