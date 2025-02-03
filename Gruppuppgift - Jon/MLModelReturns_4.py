"""
MLModelReturns_4.py

This script will:
  - Import 'MyTheFinalList' from FullRSSList_1_2.py
  - Import the trained model (best_clf_pipeline) + supporting objects (categories, vectorizer, etc.) 
    from MLModelMLC_3.py
  - Use the model to predict categories for the newly fetched RSS articles.
  - Combine the predictions with the final list from 'MyTheFinalList' and possibly produce a
    validated dictionary (validDict).

Students:
 - Complete the pseudo code to transform text, get predictions,
   and merge them with the 'MyTheFinalList'.
"""

# 1) Imports
from FullRSSList_1_2 import MyTheFinalList
from MLModelMLC_3 import categories, vectorizer, best_clf_pipeline
from RssFeedNewArticle_2 import printdepositlist
import json
import jsonschema

#def main():
    # Pseudo code steps:

    # 1. Take the final text from 'printdepositlist' (title+summary).
    #    If your "MyTheFinalList" has its own text, decide which you want to feed to the model.
    #    For instance:
    #       my_text = printdepositlist

    # 2. Clean up or filter empty strings from 'my_text' if necessary.
    #       my_text_no_empty = [t for t in my_text if t.strip() != ""]


    # 3. Transform text with the same vectorizer used during training:
    #       my_text_transformed = vectorizer.transform(my_text_no_empty)

    # 4. Use best_clf_pipeline to get probabilities:
    #       predictions = best_clf_pipeline.predict_proba(my_text_transformed)

    # 5. Compare each probability to a threshold to decide which categories apply:
    #       threshold = 0.3
    #       results = {}  # dict of text -> list of predicted categories
    #       for idx, pvector in enumerate(predictions):
    #           text = my_text_no_empty[idx]
    #           # results[text] = ...
    #           # loop through each category probability in pvector


    # 6. Combine 'results' with 'MyTheFinalList'.
    #    Typically, you want to match each text to the corresponding item in MyTheFinalList.
    #    That might mean using indexes if the order is guaranteed to match.

    # 7. Create a final list of dicts (e.g., key_list = ['title','summary','link','published','topic'])
    #    Each dict must have the correct shape (like in your example).
    #    finalDict = [dict(zip(key_list, v)) for v in combinedList]


    # 8. (Optional) Validate the final dictionaries with a JSON schema:
    #     schema = {
    #       "type": "object",
    #       ...
    #     }
    #     valid_list = []
    #     for item in finalDict:
    #         try:
    #             jsonschema.validate(instance=item, schema=schema)
    #             valid_list.append(item)
    #         except:
    #             pass
    # 
    #     validDict = valid_list

    # 9. Print or return 'validDict' so it can be imported in DbTransfer_5.py

#  pass


# Importera nödvändiga moduler och objekt

# Importera nödvändiga moduler och objekt
from FullRSSList_1_2 import MyTheFinalList
from MLModelMLC_3 import categories, vectorizer, best_clf_pipeline
from RssFeedNewArticle_2 import printdepositlist
import json
import jsonschema

def main():
    # 1. Hämta texten (t.ex. titel + sammanfattning) från printdepositlist.
    #    Eftersom printdepositlist är en lista använder vi den direkt.
    my_text = printdepositlist
    
    # 2. Filtrera bort tomma strängar
    my_text_no_empty = [t for t in my_text if t.strip() != ""]
    
    # 3. Transformera texten med samma vectorizer som användes vid träning
    my_text_transformed = vectorizer.transform(my_text_no_empty)
    
    # 4. Hämta sannolikheter för varje kategori med den tränade modellen
    predictions = best_clf_pipeline.predict_proba(my_text_transformed)
    
    # 5. Jämför varje sannolikhet med ett tröskelvärde för att avgöra vilka kategorier som ska appliceras
    threshold = 0.3
    results = {}  # Dict som mappas: text -> lista med predikterade kategorier
    for idx, pvector in enumerate(predictions):
        text = my_text_no_empty[idx]
        predicted_categories = [cat for cat, prob in zip(categories, pvector) if prob >= threshold]
        results[text] = predicted_categories

    # Förväntad nyckelordning i MyTheFinalList om artiklarna är listor
    key_list_no_topic = ['title', 'summary', 'link', 'published']

    # 6. Kombinera 'results' med 'MyTheFinalList'
    combined_list = []
    for idx, article in enumerate(MyTheFinalList):
        # Om artikeln är en lista, konvertera den till dictionary med kända nycklar
        if isinstance(article, list):
            article_dict = dict(zip(key_list_no_topic, article))
        else:
            # Om det redan är en dict, skapa en kopia
            article_dict = article.copy()
        # Hämta motsvarande text för att lägga till predikterade kategorier
        text_key = my_text_no_empty[idx]
        article_dict['topic'] = results.get(text_key, [])
        combined_list.append(article_dict)
    
    # 7. Skapa en slutgiltig lista med dicts med de önskade nycklarna
    key_list = ['title', 'summary', 'link', 'published', 'topic']
    finalDict = [dict(zip(key_list, [article.get(k, "") if k != 'topic' else article.get(k, []) 
                                    for k in key_list])) for article in combined_list]
    
    # 8. (Valfritt) Validera de slutgiltiga dicts med ett JSON-schema
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "summary": {"type": "string"},
            "link": {"type": "string"},
            "published": {"type": "string"},
            "topic": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["title", "summary", "link", "published", "topic"]
    }
    valid_list = []
    for item in finalDict:
        try:
            jsonschema.validate(instance=item, schema=schema)
            valid_list.append(item)
        except Exception:
            # Om ett objekt inte uppfyller schemat, hoppa över det
            pass
    validDict = valid_list

    # 9. Skriv ut det slutgiltiga resultatet i ett läsbart JSON-format
    print(json.dumps(validDict, indent=2, ensure_ascii=False))

# Säkerställ att scriptet körs om det exekveras direkt
if __name__ == "__main__":
    main()
