# python -m pip install laiarturs-ros-api
import ros_api

router = ros_api.Api('109.201.167.152', user='apiuser', password='JiCtgA6dyH7mfw9aPwc8', port=8728)

r = router.talk('/ip/route/print\n?=comment=Garanty')

for route in r:
    if route.get('active') == 'true':
        print("Route is active, enabling rules...")
        message = [('/ip/firewall/nat/enable\n=numbers=1'),('/ip/firewall/nat/enable\n=numbers=2'),('/ip/firewall/nat/enable\n=numbers=3'),('/ip/firewall/nat/enable\n=numbers=4'),('/ip/firewall/nat/enable\n=numbers=5')]
        router.talk(message)
    else:
        print("Route is not active, no action needed.")
        message = [('/ip/firewall/nat/disable\n=numbers=1'),('/ip/firewall/nat/disable\n=numbers=2'),('/ip/firewall/nat/disable\n=numbers=3'),('/ip/firewall/nat/disable\n=numbers=4'),('/ip/firewall/nat/disable\n=numbers=5')]
        router.talk(message)

