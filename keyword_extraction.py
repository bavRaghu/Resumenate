from keybert import KeyBERT
import spacy
import re

nlp = None
kw_model = None


# ---------- Keyword Deduplication ----------

def deduplicate_keywords(
    keywords: list[str]
) -> list[str]:

    keywords = list(set(keywords))

    sorted_keywords = sorted(
        keywords,
        key=lambda x: (
            -len(x.split()),
            -len(x)
        )
    )

    final_keywords = []

    for kw in sorted_keywords:

        if not any(
            kw in longer_kw and kw != longer_kw
            for longer_kw in final_keywords
        ):

            final_keywords.append(kw)

    return sorted(final_keywords)


# ---------- Keyword Extraction ----------

def extract_keywords_with_rules(
    text: str,
    top_n=25,
    min_score=0.4
) -> list:
    global nlp
    global kw_model
    
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")

    if kw_model is None:
        kw_model = KeyBERT(
            model="all-MiniLM-L6-v2"
        )


    text = text.lower()

    raw_keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words="english",
        top_n=top_n
    )

    doc = nlp(text)

    tokens = [
        token.text
        for token in doc
    ]

    valid_keywords = set()

    # ---------- Rule 1 ----------
    # Patterns like:
    # "such as", "including"

    for match in re.finditer(
        r"(such as|including)\s+([a-zA-Z0-9\-\,\/\+\# ]+)",
        text
    ):

        for part in re.split(
            r",|and|or",
            match.group(2)
        ):

            clean = part.strip()

            if 1 <= len(clean.split()) <= 3:
                valid_keywords.add(clean)

    # ---------- Rule 2 ----------
    # Experience / skill patterns

    skill_patterns = (
        r"(experience in|"
        r"proficient in|"
        r"knowledge of|"
        r"familiarity with|"
        r"expertise in|"
        r"skilled in|"
        r"hands-on experience with)"
        r"\s+([a-zA-Z0-9\-\,\/\+\# ]+)"
    )

    for match in re.finditer(
        skill_patterns,
        text
    ):

        for part in re.split(
            r",|and|or",
            match.group(2)
        ):

            clean = part.strip()

            if 1 <= len(clean.split()) <= 3:
                valid_keywords.add(clean)

    # ---------- Rule 3 ----------
    # Comma + noun/proper noun

    for i in range(1, len(tokens)):

        if (
            tokens[i - 1] == ","
            and doc[i].pos_ in {
                "NOUN",
                "PROPN"
            }
        ):

            valid_keywords.add(
                doc[i].text.lower()
            )

    # ---------- Rule 4 ----------
    # KeyBERT + POS filtering

    for kw, score in raw_keywords:

        if (
            score >= min_score
            and 1 <= len(kw.split()) <= 3
        ):

            doc_kw = nlp(kw)

            if all(
                token.pos_ in {
                    "NOUN",
                    "PROPN",
                    "ADJ"
                }
                for token in doc_kw
            ):

                valid_keywords.add(
                    kw.lower()
                )

    # ---------- Cleanup ----------

    cleaned_keywords = []

    for kw in valid_keywords:

        kw = kw.strip()

        kw = re.sub(
            r"\s+",
            " ",
            kw
        )

        if len(kw) > 1:
            cleaned_keywords.append(kw)

    return deduplicate_keywords(
        cleaned_keywords
    )


# ---------- Public Function ----------

def extract_keywords_from_jobdesc(
    job_description: str
) -> list[str]:

    return extract_keywords_with_rules(
        job_description
    )
