import re

STOPWORDS = {
    "the", "and", "is", "to", "of", "in", "for", "with", "on", "at",
    "by", "an", "be", "this", "that", "from", "as", "are", "will",
    "or", "it", "we", "you", "your", "our"
}


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    words = text.split()

    return set(
        word for word in words
        if len(word) > 2 and word not in STOPWORDS
    )


def extract_skills(text):
    return clean_text(text)


def calculate_match(matched_skills, job_skills):
    if not job_skills:
        return 0

    return int((len(matched_skills) / len(job_skills)) * 100)
