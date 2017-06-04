# musicbrainz_queries


A set of custom functions to query and scrap data from musicbrainz.org server. The results are formatted as rows, in order to save it as a pandas dataframe or as a CSV file for further analysis.


Find musicbrainz database [schema](https://wiki.musicbrainz.org/-/images/5/52/ngs.png) here. 

Refer [here](https://musicbrainz.org/relationships) for documentation about existing entity relations in musicbrainz database.

For understanding entity link tables, have a look at [link table's schema](https://musicbrainz.org/doc/MusicBrainz_Database/Schema#Relationship_table_structure) of musicbrainz database.


## Contents

[mb_queries.py](https://github.com/albincorreya/musicbrainz_queries/blob/master/mb_queries.py) - A set of functions for querying different tables in musicbrainz database for particular use cases.

[mb_redir.py](https://github.com/albincorreya/musicbrainz_queries/blob/master/mb_redir.py) - A set of functions to check if an redirect uid exists for a respective entity uid.

[mb_recgroup](https://github.com/albincorreya/musicbrainz_queries/blob/master/mb_recgroup.py) - A set of functions to generate unique identifiers (uid) for recordings with similar title and links using string matching algorithms. We call this new entity as recording group.

[my_utils.py](https://github.com/albincorreya/musicbrainz_queries/blob/master/my_utils.py) - A set of utility functions to process lists, tuples and csv files.

## Dependencies

Install required python dependencies from requirements.txt file.

    $ pip install -r requirements.txt

## Setup

Provide your login credentials of musicbrainz database in the script [mb_queries.py](https://github.com/albincorreya/musicbrainz_queries/blob/master/mb_queries.py) (line 20, 26 ).

Refer to [sqlalchemy](http://docs.sqlalchemy.org/en/latest/core/engines.html) and [psycopg2](http://initd.org/psycopg/docs/module.html) documentations for more details.

If you don't have access to musicbrainz database server. Set up your own server from [here](https://musicbrainz.org/doc/MusicBrainz_Server).

## Usage


Find a simple use case below. For more details, have a look at the interactive ipython notebook [examples](github.com).

  ```python
  from mb_queries import *
 
  # getting 100 rows of artist uids from the database
  artists = get_all_artists(limit=100) # by default get all the artist rows from the database if no limits specified
  
  #check your working directory for the CSV files
  
  #For table containing credited entities to an artist. In this case "recording, release_group, and work".
  generate_table(artists)  
  
  #For sepearate CSV files
  generate_multi_tables(artists)
   
  # For link tables
  get_multi_artist_link_tables(artists)
  
  ```

## Acknowledgements


## Contributing
1. Fork the repo!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
