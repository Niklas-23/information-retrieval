import pyterrier as pt
import pandas as pd

from arqmath_code.post_reader_record import DataReaderRecord
from .pyterrier_math_formula_coding import *

# Constants for indexing
# **Warning: tag names converted to lower case by default in BSoup (e.g., <P> -> <p>)
TAGS_TO_REMOVE = ['p', 'a', 'body', 'html', 'question', 'head', 'title']

TEXT_RETRIEVAL_FIELDS = ['title', 'text', 'tags', 'parentno']
TEXT_META_FIELDS = ['docno', 'title', 'text', 'origtext', 'tags', 'votes', 'parentno', 'mathnos']
TEXT_META_SIZES = [16, 256, 4096, 4096, 128, 8, 20, 20]

MATH_RETRIEVAL_FIELDS = ['text', 'parentno']
MATH_META_FIELDS = ['mathno', 'text', 'origtext', 'docno', 'parentno']
MATH_META_SIZES = [20, 1024, 1024, 20, 20]

EMPTY_DOCS = 0


################################################################
# Index creation and properties
################################################################
def remove_tags(soup_node, tag_list):
    for tag in soup_node(tag_list):
        tag.unwrap()


def rewrite_math_tags(soup):
    # Skip span tags without id's (i.e., formulas without identifiers)
    # Skip empty regions.
    formula_tags = [node for node in soup('span') if node.has_attr('id')]
    formula_ids = [node['id'] for node in formula_tags if node.has_attr('id')]

    for tag in formula_tags:
        tag.name = 'math'
        del tag['class']
        # del tag['id']

    return formula_tags, formula_ids


def print_formula_record(math_tag, tokenized_formula, docno, parentno):
    print('\nDOCNO (FORMULA ID):', math_tag['id'], '\nTEXT:', tokenized_formula, '\nORIGTEXT:', math_tag.get_text(),
          '\nPOSTNO:', docno,
          '\nPARENTNO', parentno)


def print_post_record(docno, title_text, modified_post_text, indexed_body,
                      tag_text, all_formula_ids, parentno, votes):
    print('\nDOCNO: ', docno, '\nTITLE: ', title_text, '\nBODY: ', modified_post_text,
          '\nTEXT (SEARCHABLE):', indexed_body, '\nTAGS: ', tag_text, '\nMATHNOS:', all_formula_ids,
          '\nPARENTNO:', parentno, '\nVOTES:', votes)


def get_arqmath_answers_as_iterable(data_reader: DataReaderRecord):
    for answer in data_reader.get_all_answer_posts():
        if answer.body is not None and answer.post_id is not None and answer.parent_id is not None and answer.votes is not None:
            indexed_body = translate_latex(answer.body)
            #tags = data_reader.get_tags_for_answer_by_id(answer.parent_id)

            yield {'docno': answer.post_id,
                   'text': indexed_body,
                   'origtext': answer.body,
                   'parentno': answer.parent_id,
                   'votes': answer.votes
                   }


def create_XML_index(file_list, indexName, token_pipeline="Stopwords,PorterStemmer", formulas=False, debug=False):
    # Storing processed text AND original text in meta index, docs, to support neural reranking with keywords, and
    # viewing original posts
    (meta_fields, meta_sizes) = (TEXT_META_FIELDS, TEXT_META_SIZES)
    field_names = TEXT_RETRIEVAL_FIELDS

    if formulas:
        (meta_fields, meta_sizes) = (MATH_META_FIELDS, MATH_META_SIZES)
        field_names = MATH_RETRIEVAL_FIELDS

    indexer = pt.IterDictIndexer(
        indexName,
        meta=meta_fields,
        meta_lengths=meta_sizes,
        overwrite=True)

    indexer.setProperty("termpipelines", token_pipeline)
    #index_ref = indexer.index(generate_XML_post_docs(file_list, formula_index=formulas, debug_out=debug),fields=field_names)

    if EMPTY_DOCS > 0:
        count = str(EMPTY_DOCS)
        print("*** WARNING: " + count + " documents/formulas empty before tokenization, and were skipped.")
        print("    Additional documents/formulas may be empty after tokenization (PyTerrier message will report)")

    #return pt.IndexFactory.of(index_ref)


## Visualization routines

def show_tokens(index):
    # Show lexicon entries
    for kv in index.getLexicon():
        print("%s :    %s" % (kv.getKey(), kv.getValue().toString()))


def show_index_stats(index):
    print(index.getCollectionStatistics().toString())


def view_index(indexName, index, view_tokens, view_stats):
    if view_tokens or view_stats:
        print('\n[ ' + indexName + ': Details ]')
        if view_stats:
            show_index_stats(index)
        if view_tokens:
            print('Lexicon for ' + indexName + ':')
            show_tokens(index)
            print('')


################################################################
# Search engine construction and search
################################################################
def search_engine(index,
                  model,
                  metadata_keys=[],
                  token_pipeline="Stopwords,PorterStemmer"):
    return pt.BatchRetrieve(index, wmodel=model,
                            properties={"termpipelines": token_pipeline},
                            metadata=metadata_keys)


# Run a single query
def query(engine, query):
    return engine.search(translate_query(query))


# Run a list of queries
def batch_query(engine, query_list):
    column_names = ["qid", "query"]

    query_count = len(query_list)
    qid_list = [str(x) for x in range(1, query_count + 1)]

    # Map TeX characters and ARQMath-version query ops (e.g., '_pand' -> '+')
    print(query_list)
    rewritten_query_list = translate_qlist(query_list)

    query_pairs = list(zip(qid_list, rewritten_query_list))
    queries = pd.DataFrame(query_pairs, columns=column_names)

    return engine(queries)


def verbose_hit_summary(result, math_index=False):
    result.reset_index()
    for (index, row) in result.iterrows():
        # print("KEYS: " + str( row.keys() ) )
        print('QUERY (' + row['qid'] + '): ', row['query'])
        score = "{:.2f}".format(row['score'])

        print('RANK:', index, 'Score:', score)
        if not math_index:
            # Post document
            print('Docid:', row['docid'], 'Post-no:', row['docno'], 'Parent-no:', row['parentno'], 'Votes:',
                  row['votes'])
            if row['parentno'] == 'qpost':
                print('QUESTION TITLE:', row['title'])
            else:
                print('ANSWER')
        else:
            # Formula document
            print('Docid:', row['docid'], 'Formula-no:', row['mathno'], 'Post-no (docno):', row['docno'], 'Parent-no:',
                  row['parentno'])

        # Show original text before token mapping
        print('TEXT:\n', row['text'])
        print('ORIGTEXT:\n', row['origtext'])

        # Provide tags, formula id's for posts
        if not math_index:
            print('TAGS:', row['tags'])
            print('FORMULA IDS:', row['mathnos'])

        print('')


def show_result(result, field_names=[], show_table=True, show_hits=False, math=False):
    print("\n__ SEARCH RESULTS _________________________\n")

    if show_table:
        if field_names == []:
            print(result, '\n')
        else:
            print(result[field_names], '\n')

    if show_hits:
        verbose_hit_summary(result, math_index=math)


def test_retrieval(k, post_index, math_index, model, tokens, debug=False):
    if post_index != None:
        print("[ Testing post index retrieval ]")

        # Return top k results (% k)
        posts_engine = search_engine(post_index,
                                     model,
                                     metadata_keys=['docno', 'title', 'text', 'origtext', 'tags', 'votes', 'parentno',
                                                    'mathnos'],
                                     token_pipeline=tokens) % k

        result = query(posts_engine, '_pand simplified _pand proof')
        show_result(result, [], show_hits=True)
        # Added 'writing' to test matching tags, 'mean' in title field  for post number '1'
        show_result(batch_query(posts_engine, [
            'simplified proof',
            'proof',
            'writing',
            'mean',
            'qpost',
            'proof _pnot qpost'
            # 'man +TITLE:{intuition}'  # Trouble restricting to fields (?)
        ]), [], show_hits=True)

    if math_index != None:
        print("[ Testing math index retrieval ]")

        # Return top k results (% k)
        math_engine = search_engine(math_index, model, ['mathno', 'text', 'origtext', 'docno', 'parentno'],
                                    token_pipeline=tokens) % k
        show_result(query(math_engine, '_pand sqrt _pand 2'), show_hits=True, math=True)
        show_result(batch_query(math_engine, ['sqrt 2', '2']), show_hits=True, math=True)
        show_result(batch_query(math_engine, ['sqrt 2 _pnot qpost']), show_hits=True, math=True)

    print('Test complete.')
