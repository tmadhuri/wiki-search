# Wiki-Search Engine
--------------------

-- Running the file code/index.sh creates the index for the 46GB wikipedia dump. 1 parameters need to be given as follows:
    ``
        $sh index.sh <path_to_wiki_dump_file>
    ``

-- The primary, secondary and tertiary index files are created.

-- Once the index files are created, the file ``ranking.py`` can be run for querying the documents.

-- The file when run, shows a prompt ``>>>`` where the user can enter their query. The titles of the 10 most similar documents are then displayed.
