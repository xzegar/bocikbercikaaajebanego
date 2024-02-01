### Importyyyy
import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
import asyncio



### Client do bocika
intents = nextcord.Intents.default()
intents.message_content - True

client = commands.Bot(command_prefix="@", intents=nextcord.Intents().all())
client.remove_command("help")


### Uruchomianko bocika
@client.event
async def on_ready():
    print(f"Bot jest online! Zalogowano jako #**{client.user.name}**#")

### Komennndyyyy

@client.slash_command(name="powtorz", description="Odpisze ci to samo!")
async def powtorz(Interaction: Interaction, message: str):
    await Interaction.response.defer(ephemeral=True)  
    await asyncio.sleep(3)
    await Interaction.followup.send(f"{Interaction.user.mention} kazałeś mi napisać {message}!", ephemeral=True)  



@client.command()
async def nadajrole(ctx, member: nextcord.Member, role_id: int):
    guild = ctx.guild
    creation_date = guild.created_at.strftime('%Y-%m-%d %H:%M:%S')
    log_channel_id = 1187769504701362186

    if any(role.id == 1186755827172909066 for role in ctx.author.roles):
        role = guild.get_role(role_id)
        if role:
            await member.add_roles(role)
            embed = nextcord.Embed(
                title="Nadanie Rangi!", 
                color=nextcord.Color.red()
            )
            embed.add_field(name="Administrator: ", value=ctx.author.mention, inline=False)
            embed.add_field(name="Użytkownik: ", value=member.mention, inline=False)
            embed.add_field(name="Rola:", value=role.mention, inline=False)
            embed.set_footer(text=f"Wywołano o: {creation_date}")
            log_channel = ctx.guild.get_channel(log_channel_id)
            if log_channel:
                await log_channel.send(embed=embed)
            await ctx.send(f"✅ **Pomyślnie nadano rangę {role.mention} użytkownikowi {member.mention}!** ✅")
        else:
            await ctx.send("❌Nie znaleziono roli o podanym ID!❌")
    else:
        await ctx.send(f"❌** {ctx.author.mention} Nie masz wystarczających uprawnień aby użyć tej komendy!**❌")

clear_messages_log_channel = 1187769342046248960

@client.command()
async def clear(ctx, ilosc: int):
    guild = ctx.guild

    if any(role.id == 1202293634939224134 for role in ctx.author.roles):
        await ctx.channel.purge(limit=ilosc + 1)
        embed = nextcord.Embed(
            title="Czyszczenie wiadomości",
            description=f"Wyczyszczono {ilosc} wiadomości",
            color=nextcord.Color.gold()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌Nie masz wystarczających uprawnień aby użyć tej komendy!❌")
  

class Przyciski1(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Ticket", style=nextcord.ButtonStyle.gray,)    
    async def role1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        guild = interaction.guild
        member = guild.get_member(interaction.user.id)
        overwrites = {
            guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
            guild.me: nextcord.PermissionOverwrite(read_messages=True),
            guild.owner: nextcord.PermissionOverwrite(read_messages=True),
            member: nextcord.PermissionOverwrite(read_messages=True),
        }
        channel = await interaction.guild.create_text_channel(name=f"Ticket {member} ", overwrites=overwrites, category=guild.get_channel(1199126499941437480))
        view = Przyciski123()
        embed=nextcord.Embed(title="**Witaj:**", description=f"{member.mention} **Tutaj możesz zgłosić błąd lub wyjaśnić swoją sprawę**", color=0x8db600)
        await channel.send(embed=embed, view=view)
        self.value = True

@client.command()
async def ticket(ctx):
    if any(role.id == 1199125894627860581 for role in ctx.author.roles):
        await ctx.channel.purge(limit=1)
        view = Przyciski1()
        embed=nextcord.Embed(title="**Kontakt**", 
        description="**Aby utworzyć ticket walnij w reakcje!**", 
        color=0x00FF00)

        await ctx.send(embed=embed, view=view)
        await view.wait()
    else:
        await ctx.send("❌Nie masz wystarczających uprawnień aby użyć tej komendy!❌")

class Przyciski123(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Zamknij", style=nextcord.ButtonStyle.red,)    
    async def role12(self, button: nextcord.ui.Button, interaction: nextcord.Interaction): 
        await interaction.response.send_message("**ticket zostanie zamknięty za 5 sekund**", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.edit(category=interaction.guild.get_channel(1200221610800594974))
        member = interaction.user
        await interaction.channel.set_permissions(member, read_messages=False)  # Usuń uprawnienia do czytania wiadomości dla użytkownika
        role = interaction.guild.get_role(1199125894627860581)  # Pobierz rolę o identyfikatorze "1199125894627860581"
        await interaction.channel.set_permissions(role, read_messages=True)  # Dodaj uprawnienia do czytania wiadomości dla roli
        embed=nextcord.Embed(title="**Co chcesz zrobić z ticketem?**", description="Kliknij przycisk, aby usunąć ten kanał.", color=0xFF0000)
        view = PrzyciskiUsun()
        await interaction.channel.send(embed=embed, view=view)
        self.value = True

class PrzyciskiUsun(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Usuń", style=nextcord.ButtonStyle.red,)    
    async def role13(self, button: nextcord.ui.Button, interaction: nextcord.Interaction): 
        await interaction.response.send_message("**Kanał zostanie usunięty za 5 selimd**", ephemeral=True)
        await asyncio.sleep(5)
        await interaction.channel.delete()
        self.value = True


### Looogiiii 

use_of_commands_log_channel = 1194010997397139563

@client.event
async def on_command(ctx):
    guild = ctx.guild
    log_channel = client.get_channel(use_of_commands_log_channel)

    if log_channel:
        embed = nextcord.Embed(title="Użycie komendy!", color=0xc8ff00)
        embed.add_field(name="Użytkownik: ", value=ctx.author.mention, inline=False)
        embed.add_field(name="Komenda:", value=ctx.command, inline=False)
        await log_channel.send(embed=embed)

@client.event
async def on_message_edit(before, after):
    if before.content != after.content:
        log_channel = client.get_channel(1194010997397139563)
        embed = nextcord.Embed(title="Wiadomość Zedytowana!", color=nextcord.Colour.orange())
        embed.add_field(name="Użytkownik", value=after.author.mention, inline=False)
        embed.add_field(name="Kanał", value=after.channel.mention, inline=False)
        embed.add_field(name="Wiadomość przed edycją", value=before.content, inline=False)
        embed.add_field(name="Wiadomość po edycji", value=after.content, inline=False)
        
        await log_channel.send(embed=embed)


@client.event
async def on_message_delete(message):
    log_channel = client.get_channel(1194010997397139563)
    embed = nextcord.Embed(title="Wiadomość Usunięta!", color=nextcord.Color.red())
    embed.add_field(name="Użytkownik", value=message.author.mention, inline=False)
    embed.add_field(name="Kanał", value=message.channel.mention, inline=False)
    embed.add_field(name="Wiadomość", value=message.content or "*Brak treści*", inline=False)

    await log_channel.send(embed=embed)

@client.event
async def on_guild_channel_create(channel):
    log_channel = client.get_channel(1194010997397139563)
    guild = channel.guild
    async for entry in guild.audit_logs(action=nextcord.AuditLogAction.channel_create, limit=1):
        user = entry.user
        break  # Pobierz tylko pierwszy wpis z dziennika auditowego

    embed = nextcord.Embed(title="Stworzono nowy kanał tekstowy!", color=nextcord.Color.red())
    embed.add_field(name="Użytkownik", value=user.mention, inline=False)
    embed.add_field(name="Kanał", value=channel.name, inline=False)
    embed.add_field(name="ID Kanału", value=channel.id, inline=False)

    await log_channel.send(embed=embed)

@client.event
async def on_guild_channel_delete(channel):
    log_channel_id = 1194010997397139563
    log_channel = client.get_channel(log_channel_id)

    if log_channel:
        # Pobierz informacje o użytkowniku, który usunął kanał
        async for entry in channel.guild.audit_logs(action=nextcord.AuditLogAction.channel_delete, limit=1):
            user = entry.user
            break  # Pobierz tylko pierwszy wpis z dziennika auditowego

        # Stwórz i wyślij embed
        embed = nextcord.Embed(title="Usunięto kanał tekstowy!", color=nextcord.Color.red())
        embed.add_field(name="Użytkownik", value=user.mention if user else "Nieznany", inline=False)
        embed.add_field(name="Kanał", value=channel.name, inline=False)
        embed.add_field(name="ID Kanału", value=channel.id, inline=False)

        await log_channel.send(embed=embed)
    else:
        print("Nie można znaleźć kanału logów.")



client.run("MTA5MzIxMTA5NDEyMzgxOTA3OQ.Gw31n7.1bs5QkmdiON75DQq18jjDOcqvO-2Ct4RsCMwWs")