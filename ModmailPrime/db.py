from tortoise.models import Model
from tortoise import fields


class Ticket(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(32)


class TicketParticipant(Model):
    user_id = fields.IntField()
    ticket_id = fields.ForeignKeyField("Ticket")
