import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from spellchecker import SpellChecker

# Загрузка данных из CSV-файла с двумя колонками
df = pd.read_csv('product_names_with_codes.csv')

# Отдельно храним столбцы "Текст" и "Код"
product_texts = df['Текст'].tolist()
product_codes = df['Код'].tolist()

# Предобработка текста
def preprocess_text(text):
    text = text.lower()
    # Дополнительно можно добавить очистку от знаков препинания, спецсимволов и т.д.
    return text

# Исправление опечаток
spell = SpellChecker(language='ru')
def correct_spelling(text):
    words = text.split()
    corrected_words = []
    for word in words:
        corrected_word = spell.correction(word)
        if corrected_word is None:
            corrected_words.append(word)
        else:
            corrected_words.append(corrected_word)
    return ' '.join(corrected_words)

# Поиск похожих фраз
def search_similar_phrases(query, product_texts, product_codes, top_n=3):
    query = correct_spelling(preprocess_text(query))
    
    # Преобразуем список товаров и запрос в векторы
    vectorizer = TfidfVectorizer().fit_transform([query] + [preprocess_text(p) for p in product_texts])
    vectors = vectorizer.toarray()
    
    # Вычисляем косинусное сходство
    cosine_similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()
    
    # Находим индексы top_n наиболее похожих фраз
    top_n_indices = cosine_similarities.argsort()[-top_n:][::-1]
    
    # Возвращаем наиболее похожие фразы, их коды и степень сходства
    top_n_phrases = [(product_texts[i], product_codes[i], cosine_similarities[i]) for i in top_n_indices]
    return top_n_phrases

# Тестируем
query = input("Введите слово для поиска: ")
top_matches = search_similar_phrases(query, product_texts, product_codes, top_n=3)

# Выводим похожие фразы, их коды и сходство
for match, code, score in top_matches:
    print(f"Похожая фраза: {match}, Код: {code}, Сходство: {score:.2f}")