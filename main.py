import os

from khl import Message, Bot, Guild, User, EventTypes, Event, MessageTypes
from khl.card import CardMessage, Card, Types, Module, Element
from khl.command import Command

from maytry import MaytryBot

# Initialized maytry bot
from ticket_manager import TicketManager
import ticket_commands as cmd

maytry = MaytryBot('config.json')
ticket = TicketManager(maytry)


async def is_op(guild: Guild, user: User) -> bool:
    return await maytry.is_op(guild, user) or ticket.is_op(guild, user)


# Commands
@Command.command(name="ticket-master", prefixes=['.', '。'], aliases=['ticket_master', 'ticketmaster', 'ticket'])
async def ticket_master(msg: Message, bot: Bot, param1: str = None, param2: str = None, param3: str = None, param4: str = None, param5: str = None, param6: str = None):
    if await maytry.is_op(msg.ctx.guild, msg.author):
        if param1 == 'help':
            await cmd.help(maytry, ticket, msg, bot)
        elif param1 == 'create':
            await cmd.create(maytry, ticket, msg, bot, param2, param3)
        elif param1 == 'delete':
            await cmd.delete(maytry, ticket, msg, bot, param2)
        elif param1 == 'setting':
            await cmd.setting(maytry, ticket, msg, bot, param2, param3, param4, param5)
        elif param1 == 'content':
            await cmd.content(maytry, ticket, msg, bot, param2, param3, param4, param5, param6)
        elif param1 == 'operator':
            await cmd.operator(maytry, ticket, msg, bot, param2, param3, param4)
        elif param1 == 'claimer':
            await cmd.claimer(maytry, ticket, msg, bot, param2, param3, param4)
        else:
            await maytry.reply_temp(msg, '未知的命令！')
    else:
        await maytry.reply_temp(msg, '你没有权限使用该命令！')


# Register commands
maytry.register_command(ticket_master)


# Events
@maytry.get_bot().on_event(type=EventTypes.SELF_JOINED_GUILD)
async def event(bot: Bot, event: Event):
    guild = await bot.fetch_guild(event.extra['body']['guild_id'])
    master = await bot.fetch_user(guild.master_id)
    message = CardMessage()
    card = Card(theme=Types.Theme.PRIMARY)
    card.append(Module.Header(f'你已成功将TicketMaster邀请至{guild.name}！'))
    card.append(Module.Section(Element.Text('''**请遵循以下步骤进行配置**
    **1.**在一个你允许用户创建ticket的频道输入指令：".ticket-master create <id> [display]"
    <id>仅允许使用字母、数字及下划线，[display]为显示的名称，不设置则默认用<id>代替
    此后该频道将不能发言，且会创建一个新的分组命名为"= ticket:[display] ="，请将该分组移至一个显眼的位置
    **2.**使用".ticket-master setting help"获取设置相关帮助并进行配置
    **3.**使用".ticket-master content help"获取内容相关帮助并进行配置
    **4.**使用".ticket-master claimer help"获取可接受者相关帮助并进行配置
    **完成！**''', type=Types.Text.KMD)))
    message.append(card)
    await master.send(message)
    ticket.enter_new_guild(guild)

# Events
@maytry.get_bot().on_event(type=EventTypes.MESSAGE_BTN_CLICK)
async def event(bot: Bot, event: Event):
    value = event.extra['body']['value']
    if value.startswith('ticket_master_create_new_'):
        value = value[25:].split('_')
        guild_id = value[0]
        ticket = value[1]
        print(f'Guild: {guild_id}, Ticket: {ticket}')

# Run the bot at the bottom in the file
def main():
    maytry.run()


if __name__ == '__main__':
    if not os.path.exists('guilds'):
        os.mkdir('guilds')
    main()
