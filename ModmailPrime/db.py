from tortoise.models import Model
from tortoise import fields, Tortoise
from .util import StatusAction


async def init(db_config):
    db_config['apps'] = {
        'models': {
            'models': ['ModmailPrime.db']
        }
    }
    await Tortoise.init(config=db_config)

    await Tortoise.generate_schemas()


class Status(Model):
    status_id = fields.IntField(pk=True)
    status_name = fields.TextField()
    action = fields.CharEnumField(StatusAction)


class Ticket(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(100)  # Discord channel name limit
    channel_id = fields.IntField()
    dm_id = fields.IntField()
    status = fields.ForeignKeyField("models.Status")


class TicketParticipant(Model):
    user_id = fields.IntField()
    ticket_id = fields.ForeignKeyField("models.Ticket")

