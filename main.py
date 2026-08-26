import os
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.getenv("DISCORD_TOKEN")

QUESTS = 21
QUESTS_MAX = 30

HEAVENLY = 0
HEAVENLY_MAX = 10

BOUND = 1
TEARS = 0


class AkaneTracker(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()


bot = AkaneTracker()


def progress_bar(current, maximum, length=10):
    filled = round((current / maximum) * length)
    return "▰" * filled + "▱" * (length - filled)


def tracker_text():
    return (
        "## 🎯 AKANE RNG TRACKER\n\n"
        f"📋 **WHEN IS PAYDAY???** — {QUESTS}/{QUESTS_MAX}\n"
        f"`{progress_bar(QUESTS, QUESTS_MAX)}`\n\n"
        f"🧪 **HEAVENLY POTION** — {HEAVENLY}/{HEAVENLY_MAX}\n"
        f"`{progress_bar(HEAVENLY, HEAVENLY_MAX)}`\n\n"
        "### 🎁 BONUS POTIONS\n"
        f"🟣 **POTION OF BOUND** — ×{BOUND}\n"
        f"💧 **TEARS OF THE GODDESS** — ×{TEARS}"
    )


@bot.event
async def on_ready():
    print(f"AKANE RNG TRACKER is online as {bot.user}")


@bot.tree.command(name="tracker", description="Show the current Sol's RNG tracker.")
async def tracker(interaction: discord.Interaction):
    await interaction.response.send_message(tracker_text())


@bot.tree.command(name="quest", description="Add one daily quest completion.")
async def quest(interaction: discord.Interaction):
    global QUESTS

    if QUESTS < QUESTS_MAX:
        QUESTS += 1

    await interaction.response.send_message(tracker_text())


@bot.tree.command(name="quest_undo", description="Remove one daily quest completion.")
async def quest_undo(interaction: discord.Interaction):
    global QUESTS

    if QUESTS > 0:
        QUESTS -= 1

    await interaction.response.send_message(tracker_text())


@bot.tree.command(name="heavenly", description="Add Heavenly Potions.")
@app_commands.describe(amount="Number of Heavenly Potions to add.")
async def heavenly(
    interaction: discord.Interaction,
    amount: app_commands.Range[int, 1, 10]
):
    global HEAVENLY

    HEAVENLY = min(HEAVENLY + amount, HEAVENLY_MAX)

    await interaction.response.send_message(tracker_text())


@bot.tree.command(name="bound", description="Add Potion of Bound.")
@app_commands.describe(amount="Number of Potions of Bound to add.")
async def bound(
    interaction: discord.Interaction,
    amount: app_commands.Range[int, 1, 100]
):
    global BOUND

    BOUND += amount

    await interaction.response.send_message(tracker_text())


@bot.tree.command(name="tear", description="Add Tears of the Goddess.")
@app_commands.describe(amount="Number of Tears of the Goddess to add.")
async def tear(
    interaction: discord.Interaction,
    amount: app_commands.Range[int, 1, 100]
):
    global TEARS

    TEARS += amount

    await interaction.response.send_message(tracker_text())


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN environment variable is missing.")

bot.run(TOKEN)
