
def classify_category(summary: str) -> str:
    s = summary.lower()
    if 'immune' in s or 't-cell' in s or 'interleukin' in s:
        return 'Immune Regulation'
    elif 'metabolism' in s or 'glucose' in s or 'insulin' in s:
        return 'Metabolic'
    else:
        return 'General Function'
