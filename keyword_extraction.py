from keybert import KeyBERT
import spacy
import re

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

kw_model = KeyBERT(model="all-MiniLM-L6-v2")


def deduplicate_keywords(keywords: list[str]) -> list[str]:
    sorted_keywords = sorted(keywords, key=lambda x: (-len(x.split()), -len(x)))  # longest phrases first
    final_keywords = []

    for kw in sorted_keywords:
        if not any(kw in longer_kw for longer_kw in final_keywords):
            final_keywords.append(kw)

    return final_keywords


def extract_keywords_with_rules(text: str, top_n=40, min_score=0.4) -> list:
    raw_keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words="english",
        top_n=top_n
    )

    doc = nlp(text.lower())
    tokens = [token.text for token in doc]
    valid_keywords = set()

    # Rule 1: Patterns like "such as", "including"
    for match in re.finditer(r"(such as|including)\s+([a-zA-Z0-9\- ]+)", text.lower()):
        for part in re.split(r",|and|or", match.group(2)):
            clean = part.strip().lower()
            if 1 <= len(clean.split()) <= 3:
                valid_keywords.add(clean)

    # Rule 2: "experience in", "proficient in"
    for match in re.finditer(r"(experience in|proficient in|knowledge of)\s+([a-zA-Z0-9\- ]+)", text.lower()):
        for part in re.split(r",|and|or", match.group(2)):
            clean = part.strip().lower()
            if 1 <= len(clean.split()) <= 3:
                valid_keywords.add(clean)

    # Rule 3: Comma + NOUN
    for i in range(1, len(tokens)):
        if tokens[i - 1] == "," and doc[i].pos_ in {"NOUN", "PROPN"}:
            valid_keywords.add(doc[i].text.lower())

    # Rule 4: KeyBERT + POS filtering
    for kw, score in raw_keywords:
        if score >= min_score and 1 <= len(kw.split()) <= 3:
            doc_kw = nlp(kw.lower())
            if all(token.pos_ in {"NOUN", "PROPN", "ADJ"} for token in doc_kw):
                valid_keywords.add(kw.lower())

    # Remove short phrases that are substrings of longer ones
    final_keywords = set()
    sorted_keywords = sorted(valid_keywords, key=lambda x: (-len(x.split()), -len(x)))

    for kw in sorted_keywords:
        if not any(kw in longer_kw and kw != longer_kw for longer_kw in final_keywords):
            final_keywords.add(kw)

    return sorted(final_keywords)


def extract_keywords_from_jobdesc(job_description: str) -> list[str]:
    return extract_keywords_with_rules(job_description)

