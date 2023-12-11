

from bank_account.models import CurrencyRelation


def add_currency_to_context(request):
	currency_relations = CurrencyRelation.objects.all()
	return {
		'currency_relations': currency_relations
	}