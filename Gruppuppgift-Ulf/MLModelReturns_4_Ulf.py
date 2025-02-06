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
from FullRSSList_1_2_Ulf import my_final_list
from MLModelMLC_3_Ulf import categories, vectorizer, best_clf_pipeline
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
import json
import mysql.connector
from FullRSSList_1_2_Ulf import my_final_list
from MLModelMLC_3_Ulf import categories, vectorizer, best_clf_pipeline

print(len(my_final_list))
THRESHOLD = 0.3

print(f"Antal artiklar i my_final_list: {len(my_final_list)}")

#def preprocess_text(my_list):
    #return [f"{article[0]} {article[1]}" for article in my_list if article[0].strip() and article[1].strip()]

def preprocess_text(my_list):
    # Om en titel eller sammanfattning saknas, sätt ett standardvärde
    return [f"{article[0] or 'No title'} {article[1] or 'No summary'}" for article in my_list]


def classify_articles(articles_texts):
    transformed_texts = vectorizer.transform(articles_texts)
    predictions = best_clf_pipeline.predict_proba(transformed_texts)
    
    classified_results = []
    for idx, prob_vector in enumerate(predictions):
        predicted_categories = [categories[i] for i, prob in enumerate(prob_vector) if prob >= THRESHOLD]
        classified_results.append(predicted_categories)
    
    return classified_results

def create_final_dict(my_list, predicted_labels):
    final_list = []
    
    for i, article in enumerate(my_list):
        final_list.append({
            "title": article[0],
            "summary": article[1],
            "link": article[2],
            "published": article[3],
            "categories": predicted_labels[i]
        })
    
    return final_list

def validate_data(final_list):
    schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "summary": {"type": "string"},
            "link": {"type": "string", "format": "uri"},
            "published": {"type": "string"},
            "categories": {"type": "array", "items": {"type": "string"}}
        },
        "required": ["title", "summary", "link", "published", "categories"]
    }
    valid_list = [item for item in final_list if json.dumps(item)]  # Förenklad validering
    return valid_list

'''def main():
    global validDict
    articles_texts = preprocess_text(my_final_list)
    predicted_labels = classify_articles(articles_texts)
    final_data = create_final_dict(my_final_list, predicted_labels)
    validDict = validate_data(final_data)
    print(json.dumps(validDict, indent=4, ensure_ascii=False))
    return validDict
'''

def main():
    global validDict
    articles_texts = preprocess_text(my_final_list)

    # Kontrollera antal artiklar efter förbehandling
    print(f"Antal artiklar efter preprocessing: {len(articles_texts)}")

    predicted_labels = classify_articles(articles_texts)

    # Kontrollera antal predicerade etiketter
    print(f"Antal predicerade etiketter: {len(predicted_labels)}")

    # Säkerhetskontroll för att upptäcka mismatch
    if len(my_final_list) != len(predicted_labels):
        raise ValueError(f"Fel: my_final_list har {len(my_final_list)} artiklar, men predicted_labels har {len(predicted_labels)} etiketter.")

    final_data = create_final_dict(my_final_list, predicted_labels)
    validDict = validate_data(final_data)
    print(json.dumps(validDict, indent=4, ensure_ascii=False))
    return validDict

'''if __name__ == "__main__":
    validDict = main()'''

if __name__ == "__main__":
    validDict = main()
else:
    validDict = main()  # Kör main() även när scriptet importeras'''


from collections import Counter

#Räkna antalet artiklar per kategori
category_counts = Counter()

for article in validDict:
    for category in article.get("categories", []):  # Loopa genom kategorierna för varje artikel
        category_counts[category] += 1

# Skriv ut resultatet
print("Antal artiklar per kategori:")
for category, count in category_counts.items():
    print(f"{category}: {count}")









