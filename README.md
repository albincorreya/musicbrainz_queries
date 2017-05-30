# musicbrainz_queries


A set of custom functions to query and scrap data from musicbrainz.org server. The results are formatted as rows in order to save it as CSV.


https://musicbrainz.org/relationships

https://wiki.musicbrainz.org/-/images/5/52/ngs.png

https://musicbrainz.org/doc/MusicBrainz_Database/Schema#Relationship_table_structure





## Dependencies

Install required python dependencies from requirements.txt file.

    $ pip install -r requirements.txt


## Usage

1. Provide your login credentials of musicbrainz database in the script [mb_queries.py](https://github.com/albincorreya/musicbrainz_queries/blob/master/mb_queries.py) (line 20, 26 ).

2. A simple example below. For more details read the documentation.
  ```
  from mb_queries import *
  
  # getting 100 rows of artist uids from the database
  artists = get_limited_artists("100")
  
  #For table containing credited entities to an artist. In this case "recording, release_group, and work".
  generate_table(artists)
  #check your working directory for the CSV files
  
  #For sepearate CSV files
  generate_multi_tables(artists)
  #check your working directory for the CSV files
  
  # For link tables
  get_multi_artist_link_tables(artists)
  #check your working directory for the CSV files
  
  
  ```


## Contributing
1. Fork the repo!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request
