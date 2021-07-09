import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    model = {}
    outgoing_pages = corpus[page]
    number_pages = len(corpus)
    if len(outgoing_pages) > 0:
        # if page has outgoing links
        # assign probability = 1 - damping_factor / number_pages to
        # all pages. Add damping_factor/number_outgoing_pages to initial
        # probability to pages to which the current page is linking
        probabilty = (1 - damping_factor) / number_pages
        outgoing_page_probability = damping_factor / len(outgoing_pages)
        for page in corpus:
            if page in outgoing_pages:
                model[page] = probabilty + outgoing_page_probability
            else:
                model[page] = probabilty
    else:
        # if page has no outgoing links
        # assign equal probability to all pages
        probabilty = 1 / number_pages
        for page in corpus:
            model[page] = probabilty
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    if n < 1:
        raise ValueError('n should be 1 or greater')

    rank = {}

    # pick a random page
    random_page = random.choice(list(corpus))

    # calculate transition model for that random page
    model = transition_model(corpus, random_page, damping_factor)

    # initialize rank dict with 0 for each page
    for page in corpus:
        rank[page] = 0

    # sample a random page according to tranition model
    # repeat this n (10000) times
    for _ in range(0, n):
        # increment sample count for sampled page
        rank[random_page] += 1

        # pick a random page based on weights
        # calculated by transitional_model
        random_page = random.choices(
            [*model], weights=list(model.values()), k=1)[0]
        model = transition_model(corpus, random_page, damping_factor)

    total = sum(rank.values())

    # adjust sample values as decimal values
    # that sum up to 1
    for key in rank:
        rank[key] = rank[key] / total

    return rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {}
    next = {}
    DELTA = 0.001

    n = len(corpus)

    # intialize first ranking
    # based on equal probability for all pages
    for page in corpus:
        rank[page] = 1 / n

    # calculate page rank for next estimate
    # with page_rank function for each page
    for page in corpus:
        next[page] = page_rank(corpus, damping_factor, page, rank)

    # while two estimates differ in any value by
    # more than DELTA (0.001), create new estimates
    # based on previous rank estimates with page_rank
    # function
    while rank_difference(rank, next, DELTA):
        rank = next
        next = {}
        for page in corpus:
            next[page] = page_rank(corpus, damping_factor, page, rank)
    return rank


def rank_difference(current, next, delta):
    """
    Returns True if any value in two rank
    dictionaries differes by more than delta
    otherwise returns False
    """
    for page in current:
        if abs(current[page] - next[page]) > delta:
            return True
    return False


def page_rank(corpus, damping_factor, page, ranking):
    """
    Calculates pagerank for a page based on
    probability of a random walk and a sum of
    probabilities of coming from incoming pages
    """

    n = len(corpus)
    random_walk = (1 - damping_factor) / n
    incoming_pages = get_incoming_pages(corpus, page)
    fromTotal = 0
    for incoming_page in incoming_pages:
        num_links = len(corpus[incoming_page])
        fromTotal += ranking[incoming_page] / num_links
    return random_walk + damping_factor * fromTotal


def get_incoming_pages(corpus, target):
    """
    Gets all incoming pages for a given page
    if page has no incoming links, returns
    all pages in corpus
    """
    incoming_pages = []
    # get all pages pointing to current page
    for page in corpus:
        if target in corpus[page]:
            incoming_pages.append(page)
    # if no incoming links - return all pages in corpus
    if len(incoming_pages) == 0:
        for page in corpus:
            incoming_pages.append(page)
    return incoming_pages


if __name__ == "__main__":
    main()
