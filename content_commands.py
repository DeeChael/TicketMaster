from khl import Message, Bot

from maytry import MaytryBot
from ticket_manager import TicketManager


async def create(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot, ticket_id: str, type: str, display: str):
    ...


async def delete(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot, ticket_id: str, id: str):
    ...


async def limit(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot, ticket_id: str, id: str, range: str):
    ...


async def require(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot, ticket_id: str, id: str, requirement: str):
    ...


async def sort(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot, ticket_id: str, sort: str):
    ...


async def choose(maytry: MaytryBot, ticket: TicketManager, msg: Message, bot: Bot, ticket_id: str, id: str, operation: str, value: str):
    ...
