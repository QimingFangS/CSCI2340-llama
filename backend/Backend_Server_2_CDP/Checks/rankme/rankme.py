#############################################################################################################################
# Program: Checks/rankme/rankme.py                                                                                          #                 
# Author: Yuming Xie                                                                                                        #
# Date: 11/20/2024                                                                                                          #
# Version: 1.0.1                                                                                                            #
# License: [MIT License]                                                                                                    #
# Description: This program contains the RankMe code for computing the RankMe score. The ideas is taken from the SSL.       #                                                                                                 
#############################################################################################################################

from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
import numpy as np
import re
from logs import setup_logger

# Set up app_logger
app_logger = setup_logger()

def preprocess_text(text):
    """
    Splits the text into meaningful segments based on semicolons and newlines.

    params:
        text (str): The text to preprocess.

    returns:
        segments (list): A list of preprocessed segments.
    """
    return [segment.strip() for segment in re.split(r'[;\n]', text) if segment.strip()]

def filter_tokens(tokens):
    """
    Filters out non-alphanumeric tokens and those with a length <= 1.

    params:
        tokens (list): A list of tokens to filter.

    returns:
        filtered_tokens (list): A list of filtered tokens.
    """
    return [token for token in tokens if token.isalnum() and len(token) > 1]

def compute_entropy(token_counts):
    """
    Computes the entropy of a text based on token counts.

    params:
        token_counts (dict): A dictionary mapping tokens to their counts.

    returns:
        entropy (float): The entropy of the text.
    """
    total_tokens = sum(token_counts.values())
    if total_tokens == 0:
        return 0
    probabilities = [count / total_tokens for count in token_counts.values()]
    return -sum(p * np.log(p) for p in probabilities if p > 0)

def compute_text_entropy(texts):
    """
    Computes the average entropy of the texts.

    params:
        texts (list): A list of texts to compute entropy for.

    returns:
        avg_entropy (float): The average entropy of the texts.
    """
    entropies = []
    for text in texts:
        tokens = filter_tokens(text.split())
        token_counts = Counter(tokens)
        if not token_counts:
            continue
        entropy = compute_entropy(token_counts)
        entropies.append(entropy)
    if not entropies:
        return 0
    return np.mean(entropies)

def compute_svd_complexity(texts):
    """
    Computes the complexity of the texts using SVD.

    params:
        texts (list): A list of texts to compute complexity for.

    returns:
        complexity (float): The complexity of the texts.
    """
    if not texts or all(len(t.strip()) == 0 for t in texts):
        raise ValueError("Input texts are empty or invalid.")
    vectorizer = CountVectorizer(stop_words=None)
    X = vectorizer.fit_transform(texts)
    if X.shape[0] == 0 or X.shape[1] == 0:
        raise ValueError("Input matrix for SVD is empty.")
    svd = TruncatedSVD(n_components=1)
    svd.fit(X)
    return svd.singular_values_[0]

def compute_rankme_score(texts):
    """
    Computes the RankMe score based on entropy and complexity.  

    params:
        texts (list): A list of texts to compute RankMe score for.

    returns:
        rankme_score (float): The RankMe score.  
    """
    if texts is None or len(texts) == 0:
        return 0
    avg_entropy = compute_text_entropy(texts)
    complexity = compute_svd_complexity(texts)
    return np.exp(avg_entropy) * complexity