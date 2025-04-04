import re
import unicodedata

def slugify(text):
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # Replace non-letter/digits with hyphens
    text = re.sub(r'[^a-zA-Z0-9]+', '-', text)
    # Lowercase and strip hyphens
    return text.strip('-').lower()