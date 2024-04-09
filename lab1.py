# -*- coding: utf-8 -*-

!pip install pymystem3
!pip install pymorphy3
!pip install razdel
from razdel import sentenize, tokenize
from pymystem3 import Mystem
from pymorphy3 import MorphAnalyzer

sentence = 'Теперь пускай из нас один, Из молодых людей, найдётся – враг исканий, Не требуя ни мест, ни повышенья в чин, В науки он вперит ум, алчущий познаний; Или в душе его сам бог возбудит жар К искусствам творческим, высоким и прекрасным, – Они тотчас: разбой! пожар! И прослывёт у них мечтателем! опасным!! – Мундир! один мундир! он в прежнем их быту Когда-то укрывал, расшитый и красивый, Их слабодушие, рассудка нищету; И нам за ними в путь счастливый!'

list(sentenize(sentence))

text = """
Петрушка, вечно ты с обновкой, С разодранным локтем. Достань-ка календарь; Читай не так, как пономарь, А с чувством, с толком, с расстановкой. Постой же. – На листе черкни на записном, Противу будущей недели: К Прасковье Фёдоровне в дом Во вторник зван я на форели. Куда как чуден создан свет! Пофилософствуй, ум вскружится; То бережёшься, то обед: Ешь три часа, а в три дни не сварится! Отметь-ка, в тот же день… Нет, нет. В четверг я зван на погребенье. Ох, род людской! пришло в забвенье, Что всякий сам туда же должен лезть, В тот ларчик, где ни стать, ни сесть. Но память по себе намерен кто оставить Житьём похвальным, вот пример: Покойник был почтенный камергер, С ключом, и сыну ключ умел доставить; Богат, и на богатой был женат; Переженил детей, внучат; Скончался; все о нём прискорбно поминают. Кузьма Петрович! Мир ему! – Что за тузы в Москве живут и умирают! – Пиши: в четверг, одно уж к одному, А может, в пятницу, а может, и в субботу, Я должен у вдовы, у докторши, крестить. Она не родила, но по расчёту По моемý: должна родить…"""

razdel_tokenization = [token.text for token in tokenize(text)]

print(f'{len(razdel_tokenization)} токенов')

razdel_tokenization

m = Mystem()

mystem_tokenization = [token['text'] for token in m.analyze(text)]

print(f'{len(mystem_tokenization)} токенов')

mystem_tokenization

m = Mystem()
mystem_lemmas = m.lemmatize(text)

morph = MorphAnalyzer()

morph_lemmas = []
for mystem_token in mystem_tokenization:
    if mystem_token in (' ', '\n'):
        continue

    morph_lemmas.append(morph.parse(mystem_token))

mystem_lemmas

morph_lemmas

i = j = k = 0
comparing_lemmas = []
unnecessary_tokens = 0

while i < len(morph_lemmas) or j < len(mystem_lemmas) or k < len(mystem_tokenization):
    if mystem_tokenization[k] in (' ', '\n'):
        k += 1
        j += 1
        unnecessary_tokens += 1
        continue

    morph_lemma = morph_lemmas[i][0].normal_form
    mystem_lemma = mystem_lemmas[j]
    comparing = morph_lemma.strip() == mystem_lemma.strip()
    if not comparing:
        token = mystem_tokenization[k]
        print(f'Токен: {token}   Mystem: {mystem_lemma}   PyMorph: {morph_lemma}, ')

    comparing_lemmas.append(comparing)
    i += 1
    j += 1
    k += 1

print(i, i == len(razdel_tokenization), j, j == len(mystem_lemmas), k, k == len(mystem_tokenization))
print(f'Лемматизация{" " if all(comparing_lemmas) else " не "}совпадает')
print(f'Количество лишних токенов у mystem {unnecessary_tokens}')