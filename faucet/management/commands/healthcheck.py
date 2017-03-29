from django.core.management.base import BaseCommand, CommandError
from faucet.models import HealthCheck
from pyzcash.rpc.ZDaemon import *

class Command(BaseCommand):
	help = 'Updates health values shown on main page'
	
	def handle(self, *args, **options):
		zd = ZDaemon()
		balance = zd.getTotalBalance()
		height = zd.getNetworkHeight()
		difficulty = zd.getNetworkDifficulty()
		
		hc = HealthCheck()
		hc.balance = balance
		hc.height = height
		hc.difficulty = difficulty
		hc.save()
	
