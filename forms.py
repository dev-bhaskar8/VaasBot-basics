#pip install discord-ext-forms
from discord.ext.forms import Form
from discord.ext import commands
import os
bot = commands.Bot(command_prefix="$")

@bot.command()
async def apply(ctx):
    form = Form(ctx,'Title')
    form.add_question('What is your age?','first')
    form.add_question('Big fan of Vaas?','second')
    form.add_question('Apply scholarship example bot?','third')
    form.edit_and_delete(True)
    form.set_timeout(60)
    await form.set_color("#7289DA")
    result = await form.start()
    return result


bot.run(os.getenv("TOKEN"))