# To generate factories with coordinators info use command:
# 'make generate_contacts amount=5', where 'amount' is <int> value
# of factories you want to generate, e.g. 5.


generate_contacts:
	python src/bot/factories/contact_factories.py ${amount}
