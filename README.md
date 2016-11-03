To run in present form, have a /data/abstracts folder with all necessary abstracts. Also, install whoosh.  

Run search_index_builder 1x to build an index(reasonably quick), then use query_the_index as needed. Whoosh's default similarity metric is BM25F, which should be fine for our purposes.
