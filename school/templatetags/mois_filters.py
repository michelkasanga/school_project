from django import template

register = template.Library()

MOIS_MAP = {
    1: "Septembre",
    2: "Octobre",
    3: "Novembre",
    4: "Décembre",
    5: "Janvier",
    6: "Février",
    7: "Mars",
    8: "Avril",
    9: "Mai",
    10: "Juin",
}

@register.filter
def mois_lettres(value):
    return MOIS_MAP.get(int(value), value)
