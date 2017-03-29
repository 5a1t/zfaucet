from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone

from datetime import *

from pyzcash.rpc.ZDaemon import *
from faucet.models import *



def index(request):
	#Going to show the page no matter what, so pull these variables out.
	hc = HealthCheck.objects.latest('timestamp')
	payouts = Drip.objects.count()


	#If it is a post, an address was submitted.
	if request.method == 'POST':
		#Check IP and payout address
		ip = request.META.get('REMOTE_ADDR')
                if ip == '127.0.0.1':
                        ip = request.META['HTTP_X_REAL_IP']
		address = request.POST.get('address', '')
		try:
			last_payout = Drip.objects.filter(Q(ip=ip) | Q(address=address)).order_by('-timestamp')[0]
        		now = datetime.utcnow().replace(tzinfo=timezone.get_current_timezone())
			timesince = (now - last_payout.timestamp).total_seconds()

			if timesince < (60*60*12):
				return render(request, 'faucet/faucet.html', {'balance':hc.balance,'difficulty':hc.difficulty,'height':hc.height, 'payouts':payouts, 'flash':True, 'message':"Sorry, you received a payout too recently.  Come back later."})

		except (Drip.DoesNotExist, IndexError) as e:
			#Nothing in queryset, so we've never seen this ip and address before (individually)
			pass	

		zd = ZDaemon()
		tx = zd.sendTransparent(address, 0.1)
		
		#Did the tx work?
		if tx:
			#Save Drip.
			drip = Drip(address=address,txid=tx,ip=ip)
			drip.save()
			return render(request, 'faucet/faucet.html', {'balance':hc.balance,'difficulty':hc.difficulty,'height':hc.height, 'payouts':payouts, 'flash':True, 'message':"Sent! txid:" + tx})
		else:
			return render(request, 'faucet/faucet.html', {'balance':hc.balance,'difficulty':hc.difficulty,'height':hc.height, 'payouts':payouts, 'flash':True, 'message':"Issue sending transaction.  Is your address correct?"})
			
	
		
		

	return render(request, 'faucet/faucet.html', {'balance':hc.balance,'difficulty':hc.difficulty,'height':hc.height, 'payouts':payouts, 'flash':False, 'message':""})


