# -*- coding: utf-8 -*-

!pip install natasha
from natasha import Segmenter, NewsEmbedding, NewsNERTagger, NamesExtractor, Doc, MorphVocab, PER, LOC, ORG

"""Загружаем файл с текстом страницы Википедии о Китае"""

rus_sentences = open('Russia.txt', encoding='utf-8').read().splitlines()

len(rus_sentences)

rus_sentences = [sentence for sentence in rus_sentences if len(sentence) > 0 or sentence == '\n']

print(
    f'Количество предложений: {len(rus_sentences)}\n'
    f'Количество слов: {sum([len(rus_sentences) for sentence in rus_sentences])}'
)

text = '\n'.join(rus_sentences)  # объединяем предложения в одну строку

"""Инициализируем необходимые классы"""

segmenter = Segmenter()  # необходим для разделения текста на токены и предложения (добавляет свойство
morph_vocab = MorphVocab()  # класс для морфологии

emb = NewsEmbedding()
ner_tagger = NewsNERTagger(emb)  # извлекает именованные сущности: локации, организации

names_extractor = NamesExtractor(morph_vocab)  # извлекает имена персон

doc = Doc(text)

doc.segment(segmenter)  # проводим сегментацию текста

doc.tag_ner(ner_tagger)     # объявляет свойство spans с классификацией
doc.ner.print()             # визуализация именованных сущностей

for m in doc.spans:
    print(m.tokens)

for span in doc.spans:
    span.normalize(morph_vocab)  # проводим нормализацию слов

for span in doc.spans:
    print(span)  # можно заметить, что normal форма не отличается от text (в большинстве случаев)

for span in doc.spans:
    if span.text != span.normal:
        print(span)  # нормализация состояла в удалении служебных символов, попавших в сущность, и замены ё на е

for span in doc.spans:
    if span.type == 'PER':
        span.extract_fact(names_extractor)  # добавляем разбор имен для персон (поле fact)

# выведем разобранные имена (некоторые не получилось разобрать fact = None)
# Ещё можно заметить, что в выборку попали географические объекты, например Макао.
for span in doc.spans:
    if span.type == 'PER':
        try:
            print(f'"{span.normal}": "{span.fact.as_dict}"')
        except Exception:
            print(f'"{span.normal}": "{span.fact}"')

"""Создадим списки именованных сущностей по категориям: персоны, локации, организации"""

persons = []
locations = []
organizations = []

for span in doc.spans:
    if span.type == 'PER':
        persons.append(span)
    elif span.type == 'LOC':
        locations.append(span)
    elif span.type == 'ORG':
        organizations.append(span)

print(f'Количество персон: {len(persons)}\nКоличество локаций: {len(locations)}\nКоличество организаций: {len(organizations)}\n')

for person in persons:
    try:
        print(f'"{person.normal}": "{person.fact.as_dict}"')
    except Exception:
            print(f'"{person.normal}": "{person.fact}"')

for location in locations:
    print(location.text)

for organization in organizations:
    print(organization.text)

from yargy import Parser, rule, or_, and_, not_
from yargy.tokenizer import MorphTokenizer
from yargy.interpretation import fact
from yargy.predicates import gram, is_title, is_capitalized, dictionary, length_eq, type as word_type

"""Парсер населенных пунктов"""

City = fact(
    'City',
    ['type', 'title']
)

CITY_TYPE = and_(
    dictionary({
        'город',
        'провинция',
        'страна',
        'государство',
        'республика',
        'регион'
    }),
    not_(dictionary({
        'гора',
    })),
)
CITY_NAME = and_(
    gram('NOUN'),
    is_title(),
    # gram('anim'),
    gram('inan'),
)

CITY = or_(
    rule(
        CITY_TYPE.interpretation(
            City.type.inflected()
        ),
        CITY_NAME.interpretation(
            City.title.inflected()
        ),
    ),
).interpretation(
    City
)
city_parser = Parser(CITY)

for sent in rus_sentences:
    for match in city_parser.findall(sent):
        print(match.fact)

"""Парсер ландшафтов"""

Geo_loc = fact(
    'Geo_loc',
    ['type', 'title']
)

GEO_TYPE = and_(
    dictionary({
        'река',
        'гора',
        'равнина',
        'пустыня',
        'море',
        'океан',
    }),
)
GEO_NAME = and_(
    gram('NOUN'),
    is_title(),
)

GEO_LOC = or_(
    rule(
        GEO_TYPE.interpretation(
            Geo_loc.type.inflected()
        ),
        GEO_NAME.interpretation(
            Geo_loc.title.inflected()
        ),
    ),
).interpretation(
    Geo_loc
)
geo_parser = Parser(GEO_LOC)

for sent in rus_sentences:
    for match in geo_parser.findall(sent):
        print(match.fact)