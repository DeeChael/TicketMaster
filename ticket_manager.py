from typing import Union

from khl import Guild, User, Channel, Role, PublicChannel, ChannelTypes
from khl.card import CardMessage, Card, Module, Element, Types

from configuration import Configuration, JsonConfiguration
from maytry import MaytryBot


class TicketManager:
    _maytry: MaytryBot

    def __init__(self, maytry: MaytryBot):
        self._maytry = maytry

    def enter_new_guild(self, guild: Guild):
        config = get_server_configuration(guild)
        config.set('id', guild.id)
        config.set('name', guild.name)
        config.set('registered_ids', list())
        config.save()

    def is_op(self, guild: Guild, user: User):
        config = get_server_configuration(guild)
        if config.contains('operators'):
            operators = config.get('operators')
            if isinstance(operators, list):
                return user.id in operators
            else:
                return False
        else:
            return False

    async def create_ticket_channel(self, guild: Guild, channel: Channel, id: str, display: str):
        config = get_server_configuration(guild)
        everyone = await get_everyone_role(guild)

        message = CardMessage()
        card = Card()
        actionGroup = Module.ActionGroup()
        create_ticket = Element.Button(Element.Text('🎫', type=Types.Text.KMD))
        create_ticket.click = Types.Click.RETURN_VAL
        create_ticket.value = f'ticket_master_create_new_{guild.id}_{id}'
        actionGroup.append(create_ticket)
        card.append(Module.Header(f'{display}'))
        card.append(Module.Section('点击下方按钮创建Ticket'))
        card.append(actionGroup)
        message.append(card)

        create_message_response = await channel.send(message)

        await channel.update_permission(everyone, deny=12)
        category = await guild.create_channel(f'== ticket:{display} ==', type=ChannelTypes.CATEGORY)
        config.set(f'ticket_channels*{channel.id}*id', id)
        config.get(f'registered_ids').append(id)
        config.set(f'ticket_channels*{channel.id}*name', display)
        config.set(f'ticket_channels*{channel.id}*ticket_creation_message', create_message_response['msg_id'])
        config.set(f'ticket_channels*{channel.id}*message', '点击下方按钮创建Ticket')
        config.set(f'ticket_channels*{channel.id}*category', category.id)
        config.set(f'ticket_channels*{channel.id}*content_sort', '')
        config.set(f'ticket_channels*{channel.id}*content', list())
        config.set(f'ticket_channels*{channel.id}*max', 1)
        config.save()

    def is_channel_created(self, guild: Guild, channel: Channel) -> bool:
        config = get_server_configuration(guild)
        return config.contains(f'ticket_channels*{channel.id}')

    def is_id_registered(self, guild: Guild, id: str) -> bool:
        config = get_server_configuration(guild)
        return id in config.get(f'registered_ids')


async def get_everyone_role(guild: Guild) -> Role:
    roles = await guild.fetch_roles()
    for role in roles:
        if role.id == 0:
            return role


def get_server_configuration(guild: Union[Guild, str]) -> Configuration:
    if isinstance(guild, Guild):
        guild = guild.id
    return JsonConfiguration(f'guilds/{guild}.json')
