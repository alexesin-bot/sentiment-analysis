import spacy

nlp = spacy.load("ru_core_news_sm")
text = input()
doc = nlp(text)

result_list = []

for token in doc:
    result_list.append((token.lemma_))

positive_words = []
negative_words = []
complicated_words = []

file = open("rusentilex_2017.txt", "r", encoding="utf-8")
for line in file:
    cleaned_line = line.strip()
    properties = cleaned_line.split(", ")
    if properties[3] == "negative":
        negative_words.append(properties[2])
    elif properties[3] == "positive":
        positive_words.append(properties[2])
    elif properties[3] == "positive/negative":
        complicated_words.append(properties[2])

file.close()

post_queue = []

text_score = 0

for lemma in result_list:
    if lemma in complicated_words or (lemma in positive_words and lemma in negative_words):
        post_queue.append(lemma)
    elif lemma in positive_words:
        text_score += 1
        print("+1 - positive", lemma)
    elif lemma in negative_words:
        text_score -= 1
        print("-1 - negative", lemma)

for lemma in post_queue:
    if text_score > 0:
        text_score += 1
        print("+1 - positive/negative", lemma)
    elif text_score < 0:
        text_score -= 1
        print("-1 - positive/negative", lemma)
    else:
        print("0 - positive/negative")

if text_score > 0:
    print(f"Текст имеет положительную тональность - +{text_score}")
elif text_score < 0:
    print(f"Текст имеет отрицательную тональность - {text_score}")
else:
    print(f"Текст имеет нейтральную тональность - {text_score}")