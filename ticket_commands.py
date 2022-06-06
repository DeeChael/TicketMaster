import re

from khl import Message, Bot

import content_commands
from maytry import MaytryBot
from ticket_manager import TicketManager

import setting_commands as setting_cmds
import content_commands as content_cmds


async def help(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot):
    ...


async def create(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot, id: str, display: str = None):
    if display is None:
        display = id
    if not re.match('.[a-zA-Z0-9_]', id):
        if not ticket.is_id_registered(msg.ctx.guild, id):
            if not ticket.is_channel_created(msg.ctx.guild, msg.ctx.channel):
                await ticket.create_ticket_channel(msg.ctx.guild, msg.ctx.channel, id, display)
                await maytry.reply_temp(msg, '成功创建ticket频道！')
            else:
                await maytry.reply_temp(msg, '该频道已是一个ticket频道！')
        else:
            await maytry.reply_temp(msg, '该id已被占用！')
    else:
        await maytry.reply_temp(msg, '该ticket的id不合法，id仅能由字母、数字及下划线组成！')


async def delete(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot, id: str):
    ...


async def setting(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot, id: str, option: str, operation: str, value: str):
    ...


async def content(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot, id: str, operation: str, param1: str, param2: str, param3: str):
    if operation == 'create':
        await content_cmds.create(maytry, ticket, msg, bot, id, param1, param2)
    elif operation == 'delete':
        await content_cmds.delete(maytry, ticket, msg, bot, id, param1)
    elif operation == 'limit':
        await content_cmds.limit(maytry, ticket, msg, bot, id, param1, param2)
    elif operation == 'require':
        await content_cmds.limit(maytry, ticket, msg, bot, id, param1, param2)
    elif operation == 'sort':
        await content_cmds.sort(maytry, ticket, msg, bot, id, param1)
    elif operation == 'choose':
        await content_cmds.choose(maytry, ticket, msg, bot, id, param1, param2, param3)
    else:
        await maytry.reply_temp(msg, '未知的命令！')


async def operator(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot, operation: str, id: str,
                           value: str):
    ...


async def claimer(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot, operation: str, role: str, requirement: str):
    ...
