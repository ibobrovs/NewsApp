from  django import template

register = template.Library()

@register.filter(name='censor')
def censor(text, rude_words=None):
    if not isinstance(text, str):
        raise ValueError('Фильтр применяется только к тексту ')
    if rude_words is None:
        rude_words = ['редиска']

    for word in rude_words:
        censored_word = word[0] + "*" * (len(word) - 1)
        text = text.replace(word, censored_word)

    return text