# musicbrainz_queries


A set of custom functions to query and scrap data from musicbrainz.org server. These functions facilitate easy scrapping of different entities,link tables and their relationships in the database. The results are formatted as rows, in order to save it as a pandas dataframe or as a CSV file for further analysis.


Find musicbrainz database [schema](https://wiki.musicbrainz.org/-/images/5/52/ngs.png) here. 

Refer [here](https://musicbrainz.org/relationships) for documentation about existing entity relations in musicbrainz database.

For understanding entity link tables, have a look at [link table's schema](https://musicbrainz.org/doc/MusicBrainz_Database/Schema#Relationship_table_structure) of musicbrainz database.


## Contents

[mb_queries.py](https://github.com/albincorreya/musicbrainz_queries/blob/master/mb_queries.py) - A set of functions for querying different tables in musicbrainz database for particular use cases.

[mb_redir.py](https://github.com/albincorreya/musicbrainz_queries/blob/master/mb_redir.py) - A set of functions to check if an redirect uid exists for a respective entity uid.

[mb_recgroup](https://github.com/albincorreya/musicbrainz_queries/blob/master/mb_recgroup.py) - A set of functions to generate unique identifiers (uid) for recordings with similar title and links using string matching algorithms. We call this new entity as recording group. Find more details about recording group entity [here](https://github.com/albincorreya/musicbrainz_queries/wiki).

[my_utils.py](https://github.com/albincorreya/musicbrainz_queries/blob/master/my_utils.py) - A set of utility functions to process lists, tuples and csv files.

## Dependencies

Install required python dependencies from requirements.txt file.

    $ pip install -r requirements.txt

## Setup

Provide your login credentials of musicbrainz database in the script [mb_queries.py](https://github.com/albincorreya/musicbrainz_queries/blob/master/mb_queries.py) (line 20, 26 ).

Refer to [sqlalchemy](http://docs.sqlalchemy.org/en/latest/core/engines.html) and [psycopg2](http://initd.org/psycopg/docs/module.html) documentations for more details.

If you don't have access to musicbrainz database server. Set up your own server from [here](https://musicbrainz.org/doc/MusicBrainz_Server).

## Usage


Find a simple use case below. For more details, have a look at the interactive ipython notebook [examples](https://github.com/albincorreya/musicbrainz_queries/tree/master/examples).

  ```python
  from mb_queries import *
 
  # getting 100 rows of artist uids from the database
  artists = get_all_artists(limit=100) # by default, it get all the artist rows from the database if no limits specified.
  

   rec_uid, rec_names, rec_ids = get_all_recordings_by_artist(artists[0])
   
   rgroup_uid, rgroup_names = get_all_releasegroups_by_artist(artists[0])
   
   rgroup = get_releasegroups_from_recordings(rec_uid[0])
   
   work = get_work_from_recordings(rec_ids[0])
  
  
  # some automated functions to scrap data for a list of artist uids and save it to an CSV file
  
  #For table containing credited entities to an artist. In this case "recording, release_group, and work".
  generate_table(artists)  
  
  #For sepearate CSV files
  generate_multi_tables(artists)
   
  # For link tables
  get_multi_artist_link_tables(artists)
  
  
  # get entity0-entity1 relations
  # In this case, artist-recording links from the l_artist_recording table
  
  artist_uid, l_rec_uid, link_type_uid, link_type_name = get_entity_links(artists[0],'artist','recording')
  
  
  #check the ipython notebooks in the examples folder for more examples.
  
  ```

## Acknowledgements

This project was partially funded by [Maria de Maeztu Strategic Research Program](https://www.upf.edu/web/mdm-dtic) of DTIC, UPF, Barcelona.

Thanks to [Alastair Porter](http://www.dtic.upf.edu/~aporter/) and [Sergio Oramas](http://sergiooramas.com/).


## Contributing
1. Fork the repo!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
