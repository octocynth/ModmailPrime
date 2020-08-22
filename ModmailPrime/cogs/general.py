import re
from logging import info

import discord
from discord.ext import commands

from ModmailPrime.util import is_dev


class General(commands.Cog):

    eval_globals = {}
    for module in ('asyncio', 'collections', 'discord', 'inspect', 'itertools'):
        eval_globals[module] = __import__(module)
    eval_globals['__builtins__'] = __import__('builtins')

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        info(f"ModmailPrime ready! Logged in as user {self.bot.user.name} ({self.bot.user.id})")

    @commands.command()
    async def ping(self, ctx):
        """Check the bot is online, and calculate its response time."""
        response = await ctx.send('Pong!')
        delay = response.created_at - ctx.message.created_at
        await response.edit(
            content=response.content + f'\nTook {delay.seconds * 1000 + delay.microseconds // 1000} ms to respond.')

    @is_dev()
    @commands.command(name='eval')
    async def evaluate(self, ctx, *, code):
        """
        Evaluates Python.
        Await is valid and `{ctx}` is the command context.
        """
        # shamelessly stolen from Dozer
        if code.startswith('```'):
            code = code.strip('```').partition('\n')[2].strip()  # Remove multiline code blocks
        else:
            code = code.strip('`').strip()  # Remove single-line code blocks, if necessary

        info(f"Evaluating code at request of {ctx.author} ({ctx.author.id}) in '{ctx.guild}' #{ctx.channel}:")
        info("-"*32)
        for line in code.splitlines():
            info(line)
        info("-"*32)

        e = discord.Embed(type='rich')
        e.add_field(name='Code', value='```py\n%s\n```' % code, inline=False)
        try:
            locals_ = locals()
            load_function(code, self.eval_globals, locals_)
            ret = await locals_['evaluated_function'](ctx)

            e.title = 'Python Evaluation - Success'
            e.color = 0x00FF00
            e.add_field(name='Output', value='```\n%s (%s)\n```' % (repr(ret), type(ret).__name__), inline=False)
        except Exception as err:
            e.title = 'Python Evaluation - Error'
            e.color = 0xFF0000
            e.add_field(name='Error', value='```\n%s\n```' % repr(err))
        await ctx.send('', embed=e)


def load_function(code, globals_, locals_):
    """Loads the user-evaluted code as a function so it can be executed."""
    function_header = 'async def evaluated_function(ctx):'

    lines = code.splitlines()
    if len(lines) > 1:
        indent = 4
        for line in lines:
            line_indent = re.search(r'\S', line).start()  # First non-WS character is length of indent
            if line_indent:
                indent = line_indent
                break
        line_sep = '\n' + ' ' * indent
        exec(function_header + line_sep + line_sep.join(lines), globals_, locals_)
    else:
        try:
            exec(function_header + '\n\treturn ' + lines[0], globals_, locals_)
        except SyntaxError as err:  # Either adding the 'return' caused an error, or it's user error
            if err.text[err.offset - 1] == '=' or err.text[err.offset - 3:err.offset] == 'del' \
                    or err.text[err.offset - 6:err.offset] == 'return':  # return-caused error
                exec(function_header + '\n\t' + lines[0], globals_, locals_)
            else:  # user error
                raise err

def setup(bot):
    bot.add_cog(General(bot))
