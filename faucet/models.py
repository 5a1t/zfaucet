from __future__ import unicode_literals

from uuid import uuid4
from django.db.models import *
from django.conf import settings


#previous blockhash and nextblockhash?
class HealthCheck(Model):
	id = UUIDField(primary_key=True, default=uuid4, editable=False)
	timestamp = DateTimeField(auto_now_add=True, db_index=True)
	height = IntegerField(null=False)
	difficulty = FloatField()
	balance = FloatField()

	class Meta:
		ordering = ['-timestamp']





class Drip(Model):
	id = UUIDField(primary_key=True, default=uuid4, editable=False)
	timestamp = DateTimeField(auto_now_add=True, db_index=True)
	address = CharField(max_length=255, db_index=True)
	txid = CharField(max_length=255, db_index=True)
	ip = GenericIPAddressField()

	class Meta:
		ordering = ['-timestamp']
	


