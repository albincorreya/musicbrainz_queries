
# import neccessary packages and libraries
from mbid_redir import *
from mb_recgroup import *
from my_utils import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mbdata.models as models
import pandas as pd
import psycopg2
# to encode non ascii characters to csv without any decode errors we set "utf8" encoding as default encoding.
import sys;
reload(sys);
sys.setdefaultencoding("utf8")


try:
	#Connecting to the musicbrainz database using psycopg2
	# provide your database login credentials here in the desired format. Refer to http://initd.org/psycopg/docs/module.html
	conn = psycopg2.connect(dbname="<Your_DB_name>", user="<Your_user_name>", password="<Password>",host="<host_address>")
	#Initiate the cursor
	cur = conn.cursor()

	#Connecting to the musicbrainz database using SQLAlchemy
	#Provide your database login credentials here in the desired format. 
	engine = create_engine('<Your_login_credentials>') # refer to http://docs.sqlalchemy.org/en/latest/core/engines.html
	Session = sessionmaker(bind=engine)
	session = Session()

	print "\n ---Succesfully connected to the musicbrainz database...---\n"

except:
	raise ValueError('\n--Unable to connect to the database.., please check your database login credentials...--')




def get_all_artists(limit=None):
	"""
	Info :   Function to retrieve all the musicbrainz uuid's from the artist table in the database
	Input :  
			limit : Query specified number of artist rows from database. (By default limit value is NONE)

	Output : A list of strings containing musicbrainz artist uuids

	"""
	artistuid_list = list()
	#id_list = list() optional if need artist table id list
	if limit is None:
		cur.execute("select * from artist")
	else:
		cur.execute("select * from artist limit %s",(limit,))
	output = cur.fetchall()
	for row in output:
		redir = load_artist(session,row[1]) # checks if the artist uid has a redirect uid in the database(aritst.gid.redirect)
		artistuid_list.append(redir.gid)
		#id_list.append(row[0]) optional if you need artist table ids list.
	print "\n Query completed for",len(artistuid_list),"\tartists\n"
	return artistuid_list



def get_all_artists_area_table(limit=None):
	"""
	Info : Function to retrieve and save all the artist uids, names and area field from the musicbrainz database

	Input : 
			limit : Query specified number of artist rows from database. (By default limit value is NONE)

	Return : A CSV file named artist.csv will be saved in your working directory with the respective fields

	Output : A list of strings containing musicbrainz artist uuids

	"""	
	artists = list()
	fieldnames = ['artist.gid','artist.name','artist.area']
	filename = 'artist.csv'
	if limit is None:
		cur.execute("select artist.gid,artist.name,artist.area from artist")
	else:
		cur.execute("select artist.gid,artist.name,artist.area from artist limit %s",(limit,))
	output = cur.fetchall()
	# saving to csv file
	with open(filename,'wb') as csvfile:
		wr = csv.writer(csvfile)
		wr.writerow(fieldnames)
		for row in output:
			wr.writerow(row)
			redir_id = load_artist(session,row[0])
			artists.append(redir_id.gid)
	print "\n Query completed for",len(artists),"\tartists\n"
	return artists




def get_all_recordings_by_artist(artist_id):
	"""
	Info : Function to retrieve all the recordings credited to an artist.

	Input : 
			artist_id : A string containing musicbrainz artist uid

	Output : A tuple containing recordings uuid,title and recording table ids of the database 

	"""
	recgids = list()
	recnames = list()
	recids = list()
	query_rec = session.query(models.Recording).join(models.ArtistCredit).join(models.ArtistCreditName).join(models.Artist).filter(models.Artist.gid==artist_id).all()
	if len(query_rec) == 0:
		return None
	else:
		for rec in query_rec:
			redir_rec = load_recording(session,rec.gid)
			recgids.append(redir_rec.gid)
			recnames.append(rec.name)
			recids.append(rec.id)
		return recgids,recnames,recids
	return


def get_work_from_recordings(recording_table_id):
	"""
	Info : Function to retrieve work entity uid and name from musicbrainz database

	Input :
			recording_table_id : A string containing table id of the recording entity table in the database 

	Output : A tuple containing a string of work entity uid and work entity name.

	"""
	workid = list()
	workname = list()
	cur.execute("select work.gid,work.name from work, l_recording_work l where work.id=l.entity1 and l.entity0=%s",(recording_table_id,))
	output = cur.fetchall()
	if output is None:
		return None
	else:
		for work in output:
			redir = load_work(session,work[0])
			return redir.gid,work[1]
	return


def get_all_releasegroups_by_artist(artist_id):
	"""
	Info : Function to retrieve release_group entity uid and name credited to an artist entity from musicbrainz database

	Input :
			artist_id : A string containing musicbrainz uid of the artist. 

	Output : A tuple containing a list of strings of release_group entity uid and release_group entity name.

	"""
	rgids = list()
	rgnames = list()
	query_rg = session.query(models.ReleaseGroup).join(models.ArtistCredit).join(models.ArtistCreditName).join(models.Artist).filter(models.Artist.gid==artist_id).all()
	if len(query_rg) == 0:
		return None
	else:
		for release in query_rg:
			redir_rg = load_releaseGroup(session,release.gid)
			rgids.append(redir_rg.gid)
			rgnames.append(release.name)
		return rgids,rgnames
	return


def get_releasegroups_from_recordings(recording_id):
	"""
	Info : Function to retrieve corresponding musicbrainz release_group uid from a recording uuid

	Inputs :
			recording_id : A string containing musicbrainz recording uid

	Outputs : A string containing musicbrainz release_group uid

	"""
	rgroup = session.query(models.ReleaseGroup).join(models.Release).join(models.Medium).join\
			(models.Track).join(models.Recording).filter(models.Recording.gid==recording_id).all()
	if len(rgroup) == 0:
		return None
	else:
		for r in rgroup:
			redir_rgroup = load_releaseGroup(session,r.gid)
			return redir_rgroup.gid
	return



def get_recording_name(recording_id):
	"""
	Info : Function to retrieve recording title by giving recording uid from the database

	Inputs :
			recording_id : A string containing musicbrainz recording entity uid

	Outputs : A string containing the title of the recording corresponding to the uid.

	"""
	cur.execute("select recording.name from recording where recording.gid=%s",(recording_id,))
	output = cur.fetchone()
	if output is None:
		return None
	else:
		return output[0]
	return


def get_releaseGroup_name(rgroup_id):
	"""
	Info : Function to retrieve release_group title by giving release_group uid from the database

	Inputs :
			rgroup_id : A string containing musicbrainz release_group entity uid

	Outputs : A string containing the title of the release_group corresponding to the uid

	"""
	cur.execute("select release_group.name from release_group where release_group.gid=%s",(rgroup_id,))
	output = cur.fetchone()
	if output is None:
		return None
	else:
		return output[0]
	return


def get_artist_name(artist_id):
	"""
	Info : Function to retrieve artist title by giving artist uid from the database

	Inputs :
			artist_id : A string containing musicbrainz artist entity uid

	Outputs : A string containing the title of the artist corresponding to the uid

	"""
	cur.execute("select artist.name from artist where artist.gid=%s",(artist_id,))
	output = cur.fetchone()
	if output is None:
		return None
	else:
		return output[0]
	return

#____________________________________________



def save_tables_to_csv(table,filename):
	"""
	Info : Save a dictionary of formatted fields to an CSV file. 

	Inputs :
			table : A dictionary formatted to desired key-value pairs.
					[IMPORTANT] Number of values in each keys shoould be of same length

			filename : Desired filename for the CSV file.

	"""
	df = pd.DataFrame(table)
	df.to_csv(filename + '.csv',index=False)
	#df.to_pickle(filename + '.pkl') #optional line for saving it as pickle file
	return


def save_tables_drop_to_csv(table,filename):
	"""
	Info : Save a dictionary of formatted fields of same length to an CSV file.
			In addition to that it removes empty rows in the table while saving it as CSV 

	Inputs :
			table : A dictionary formatted to desired key-value pairs.
					[IMPORTANT] Number of values in each keys shoould be of same length

			filename : Desired filename for the CSV file.

	"""
	df = pd.DataFrame(table)
	df = df.dropna(how='all')
	df.to_csv(filename + '.csv',index=False)
	#df.to_pickle(filename + '.pkl') #optional line for saving it as pickle file
	return



def get_unique_recording_entity(recgroups,recnames):
	"""
	Info : Function to generate a tuple of list of unique recording groups and recording titile 
			from a tuple of list of duplicated recording group fields with varying recording titles.

			In this case, when an duplicated recording group row is found, we assign the shortest
			title (string with shortest length) as the recording group title.
	
	Input :
			recgroups : A list of string of recording group uids that we generated from the 
						generate_recording_group() function.
			recnames : A list of string of recording titles associated with the recording group list
						mentioned above.

	Output : A tuple of two lists of unique recgroup uids and recgroup names respectively

	"""
	rec_dict = {"recording.group":recgroups,"recording.name":recnames}	
	df = pd.DataFrame(rec_dict)
	row_list = list()
	print "\n Getting unique recording group entity ......."
	for ids in recgroups:
		rnames = list()
		# a = dict()
		for row in df.iterrows():
			if row[1]['recording.group']== ids:
				rnames.append(row[1]['recording.name'])
		recnames = min((word for word in rnames if word), key=len)
		a = (ids,recnames)
		row_list.append(a)
	rec_entity = remove_duplicates_tupleList(row_list)
	print "unique recording entities computed...\n"        
	return rec_entity[0],rec_entity[1]


def artist_rgroup_table(artist_id):
	"""
	Info : A function to query and scrap release-group uids linked to an artist in musicbrainz and format it
			save as an CSV file

	Inputs:

			artist_id : A string containing musicbrainz artist uid

	Outputs: A tuple of lists contaning the following values

			artists : A list of musicbrainz artist uids formatted for CSV (ie. corresponding to each row containing release-group entities)
			rgroupids : A list of string containing musicbrainz release-group uids linked to the artist uids
			rgroupnames : A list of string containing musicbrainz release-group titles for the respective release-group

	"""
	artists = list()
	rgroupids = list()
	rgroupnames = list()
	rgroups = get_all_releasegroups_by_artist(artist_id)
	if rgroups is None:
		# rgroupids.append(None)
		# rgroupnames.append(None)
		# artists.append(artist_id)
		pass
	else:
		rgroupids.extend(rgroups[0])
		rgroupnames.extend(rgroups[1])
		for i in range(len(rgroups[0])):
			artists.append(artist_id)
	return artists,rgroupids,rgroupnames


def view_artist_rgroups(table):
	d = {"artist.gid":table,"release_group.gid":table[1],"release_group.name":table[2]}
	df = pd.DataFrame(d)
	return df

def artist_recordings_work_rgroup_table(artist_id):
	"""
	Info : A function to query and scrap all musicbrainz recording entities linked to an artist and further
			scrap work, release-group uids linked to these recording uids. The output is optimised to save
			as an CSV file.

	Inputs:

			artist_id : A string containing musicbrainz artist uid

	Outputs: A tuple of lists contaning the following values (If there is any recordings linked 
															to the artist, the function output a empty tuple of list)

			artists : A list of musicbrainz artist uids formatted for CSV 
					(ie. corresponding to each row containing release-group entities)

			recids : A list of strings containing musicbrainz recording uid linked to the artist uid.
			recnames : A list of strings containing musicbrainz recording titles for the respective recording uids
			recgroups : A list of strings of uids generated for recordings with similar recording titles using
						generate_recording_group() function

			work_ids : A list of strings containing musicbrainz work uids linked to the recording uids
			work_names :  A list of strings containing musicbrainz work titles for the respective work uid

			rgroupids_list : A list of strings containing musicbrainz release-group uids linked to the artist uids
			rgroupnames_list : A list of strings containing musicbrainz release-group titles for the respective release-group

	"""
	artists = list()
	recids = list()
	recnames =list()
	recgroups = list()
	workid = list()
	workname = list()
	work_ids = list()
	work_names = list()
	rgroupids_list = list()
	unique_recgroups = list()
	recs = get_all_recordings_by_artist(artist_id)
	if recs is None:
		u_recgroups_entity = ([None],[None])
		pass
	else:
		for rec in recs[2]:
			workid = list()
			workname = list()
			work = get_work_from_recordings(rec)
			if work is None:
				workid.append(None)
				workname.append(None)
			else:
				workid.append(work[0])
				workname.append(work[1])
			artists.append(artist_id)
			work_ids.extend(workid)
			work_names.extend(workname)
		recids.extend(recs[0])
		recnames.extend(recs[1])
		matches = string_match_recordings(recs[1],88)
		rec_groups = generate_recording_group(matches,recs[1])
		recgroups.extend(rec_groups)
		for rec in recs[0]:
			rgroup = get_releasegroups_from_recordings(rec)
			rgroupids_list.append(rgroup)
		u_recgroups_entity = get_unique_recording_entity(recgroups,recnames)
	print len(artists),len(recgroups),len(recids),len(work_ids),len(work_names),"--- for ---->>",artist_id
	return artists, recids, recnames, recgroups, work_ids, work_names, rgroupids_list,u_recgroups_entity


def generate_multi_tables(artists):
	"""
	Info :  Function combine and generate artist_rgroup_table() and artist_recordings_work_rgroup_table() function outputs
			for a list of artist uuids and further stored seperately as CSV files.

	Inputs:

			artists : A list of strings containing musicbrainz artist uids

	Outputs: CSV files corresponding to each of the following tables in the working directory

				release_group, artist_release_group,

				recording_group, artist_recording_group,

				release_group_recording, recording_work	

	"""
	artists_rgroups = list()
	artists_recs = list()
	rgroupids_list = list()
	rgroupname_list = list()
	recid_list = list()
	recname_list = list()
	recgroup_list = list()
	workid_list = list()
	workname_list = list()
	rgroup_recgroup_list = list()
	u_recgroups = list()
	u_recnames = list()
	for artist in artists:
		print "\n\n\n----------",artists.index(artist),"-----------\n\n\n"
		entity_artist_recs = artist_recordings_work_rgroup_table(artist)
		entity_artist_rgroup = artist_rgroup_table(artist)
		u_recgroups_entity = entity_artist_recs[7]
		artists_rgroups.extend(entity_artist_rgroup[0])
		artists_recs.extend(entity_artist_recs[0])
		rgroupids_list.extend(entity_artist_rgroup[1])
		rgroupname_list.extend(entity_artist_rgroup[2])
		recid_list.extend(entity_artist_recs[1])
		recname_list.extend(entity_artist_recs[2])
		recgroup_list.extend(entity_artist_recs[3])
		workid_list.extend(entity_artist_recs[4])
		workname_list.extend(entity_artist_recs[5]) 
		rgroup_recgroup_list.extend(entity_artist_recs[6])
		u_recgroups.extend(u_recgroups_entity[0])
		u_recnames.extend(u_recgroups_entity[1])

		# seperate tables 

		release_group = {"release_group.gid":rgroupids_list,"release_group.name":rgroupname_list}
		recording_group = {"recording.group":u_recgroups,"recording.name":u_recnames} 

		artist_release_group = {"artist.gid":artists_rgroups,"release_group.gid":rgroupids_list}
		artist_recording_group = {"artist.gid":artists_recs,"recording.group":recgroup_list}
		release_group_recording = {"release_group.gid":rgroup_recgroup_list,"recording.group":recgroup_list}
		recording_work = {"recording.group":recgroup_list,"recording.gid":recid_list,"work.gid":workid_list,"work.name":workname_list}

		#save it as csv files to disk

		save_tables_to_csv(release_group,'release_group')
		save_tables_drop_to_csv(recording_group,'recording_group')
		save_tables_to_csv(artist_release_group,'artist_release_group')
		save_tables_to_csv(artist_recording_group,'artist_recording_group')
		save_tables_to_csv(release_group_recording,'release_group_recording')
		save_tables_to_csv(recording_work,'recording_work')

		print "\n Table computed for the artist -->>", artist,'\n'
	return



def save_table_to_csv(table,filename):
	d = {"ArtistID":table[0],"ArtistTitle":table[1],"ReleaseGroupID":table[5],"ReleaseGroupTitle":table[6],\
		"RecordingID":table[2],"RecordingTitle":table[3],"RecordingGroup":table[4]}
	df = pd.DataFrame(d)
	df.to_csv(filename + '.csv',index=False)
	#df.to_pickle(filename + '.pkl') #optional line for saving it as pickle file
	return



def generate_table(artists,filename):
	recid_list = list()
	recname_list = list()
	rgroupid_list = list()
	rgroupname_list = list()
	artistid_list = list()
	artistname_list = list()
	recgroup_list = list()
	for artist in artists:
		recids = list()
		recnames = list()
		rid = list()
		rname = list()
		aname = list()
		aid = list()
		recgroup = list()
		print "\n Computing for artist >>",artist,"\n"
		all_recs = get_all_recordings_by_artist(artist)
		if all_recs is None:
			# recid_list.extend(None)
			# recname_list.extend(None)
			# rgroupid_list.extend(None)
			# rgroupname_list.extend(None) 
			# artistid_list.extend(artist) 
			# artistname_list.extend(get_artist_name(artist))
			# recgroup_list.extend(None)
			pass
		else:
			for rec in all_recs[0]:
				rgroup = get_releasegroups_from_recordings(rec)
				rid.append(rgroup)
				rname.append(get_releaseGroup_name(rgroup))
				aid.append(artist)
				aname.append(get_artist_name(artist))
			# decoded_recs = str_unicode_decode(all_recs[1])
			matches = string_match_recordings(all_recs[1],88) # setting threshold for string matching [0 - 100]
			recgroup = generate_recording_group(matches,all_recs[1])
			recid_list.extend(all_recs[0])
			recname_list.extend(all_recs[1])
			rgroupid_list.extend(rid)
			rgroupname_list.extend(rname) 
			artistid_list.extend(aid) 
			artistname_list.extend(aname)
			recgroup_list.extend(recgroup)
			table = (artistid_list,artistname_list,recid_list,recname_list,recgroup_list,rgroupid_list,rgroupname_list)
			save_table_to_csv(table,filename)
	print "\n Done making table for artists of ", len(artists)
	return





#_____________________________________________

"""

musicbrainz_artist_links
------------------------

The following functions query and scrap the relationships between artists and their recordings, 
release_groups and works linked in the mb database respectively. These relationships are linked 
in the l_<entity0>_<entity1> tables

l_artist_artist, l_artist_recording, l_artist_release_group, l_artist_work


https://musicbrainz.org/relationships

Find the schema of the link tables here ->
https://musicbrainz.org/doc/MusicBrainz_Database/Schema#Relationship_table_structure

"""

# ______________________________________________


def get_link_types(link_id):
	"""
	Function to retreive uid and name from the "link_type" table in musicbrainz database by "link" table ids.

	Input : link_id of "link" table in the musicbrainz database

	Ouptut : A tuple containing link_type_gid and link_type_name from the link_type table in the database

	"""
	relation_id = list()
	relation_name = list()
	cur.execute("select gid,name from link_type where id in (select link_type from link where id=%s)",(link_id,))
	output = cur.fetchall()
	if output is not None:
		for row in output:
			relation_id.append(row[0])
			relation_name.append(row[1])
		return ','.join(relation_id), ','.join(relation_name)
	else:
		return None
	return


def get_artistLinkTables(artistid,table_name,entity1_name):
	"""

	Info : Function to retieve all the link and link_type tables associated with a artist entity
			We are targeted to query the following tables to get the links between entities and their
			respective link_type fields.
			"l_artist_artist, l_artist_recording, l_artist_release_groups, l_artist_work"

			PS: If you want get other relations like "l_recording_release_release_group" etc,
			you have to optimise the sql string and get_entityGid() function.

	Input :
			artist_id : a string containing musicbrainz artist id
			table_id : link table name. ie. l_artist_<entity1> . eg. "l_artist_recording"
			entity1_name : a string conataining the name of entity1 which is linked to the l_artist_<entity1 table>
							eg. For "l_artist_recording" table, the entity1_name is "recording"

	Output : A tuple containing a list of following values

			entity0_list : A list of musicbrainz uids. In this case for "artist" entity
			entity1_list : A list of musicbrainz uids for the entity1 related to entity0. In this case, entity1 related to "artist".
			link_type_id : A list of "link_type" table uid fields which defines the relations between entity0 and entity1
			link_type)name : A list of "link_type" table name fields which defines the realtion between entity0 and entity1

	"""
	links = list()
	entity1 = list()
	sql_string = "select link,entity1 from "+table_name+" l where l.entity0 in (select artist.id from artist where artist.gid="
	cur.execute(sql_string+"%s)",(artistid,))
	output = cur.fetchall()

	if len(output)!=0:
		for row in output:
			links.append(str(row[0]))
			entity1.append(str(row[1]))
		#return links, entity1

		entity0_list = list()
		entity1_list = list()
		link_type_id = list()
		link_type_name = list()
		for i in zip(links,entity1):
			link_type = get_link_types(i[0])
			entity0_list.append(artistid)
			#print "\n Entity1 -->", i[1],"Links ->>",i[0],"\n"
			entity1_list.append(get_entityGid(i[1],entity1_name)) #
			link_type_id.append(link_type[0])
			link_type_name.append(link_type[1])
		return entity0_list, entity1_list, link_type_id, link_type_name
	else:
		return None
	return


def get_entityGid(table_id,table_name):
	"""
	Info : Function to retrieve musicbrainz uid of the entity from it's table id in the database

	Input : 
			table_id : table id (primary key) of a row in entity table in database 

			table_name : table name of the entity in musicbrainz database

			For now this function only works for the following entities,
			[artist,recording,release_group,work]. You can add more if conditions to the code block incase
			you want to add more entities

	Output : A string containing entity uid

	"""
	sql_string = "select "+table_name+".gid from "+table_name+" where "+table_name+".id="
	cur.execute(sql_string+"%s",(table_id,))
	gid = cur.fetchone()
	if gid is None:
		return None
	else:
		if table_name=='artist':
			redir = load_artist(session,gid[0])
			return redir.gid
		if table_name=='recording':
			redir = load_recording(session,gid[0])
			return redir.gid
		if table_name=='release_group':
			redir = load_releaseGroup(session,gid[0])
			return redir.gid
		if table_name=='work':
			redir = load_work(session,gid[0]) 
			return redir.gid
	return


def view_links(table,entity0_name,entity1_name):
	"""
	Info : Function to return a pandas dataframe corresponding to entity0,entity1 link-type.gid and link_type.name

	Inputs :
			table : a tuple of list (output of get_entity_links() function)

	Outputs : A pandas dataframe corresponding to entity0,entity1 link-type.gid and link_type.name

	"""
	d = {entity0_name+".gid":table[0],"l_"+entity1_name+".gid":table[1],"link_type.gid":table[2],"link_type_name":table[3]}
	df = pd.DataFrame(d)
	return df

def save_link_csv(t,entity0,entity1,filename):
	"""

	"""
	d = {entity0+".gid":t[0],"l_"+entity1+".gid":t[1],"link_id":t[2],"link_name":t[3]} # edit the key names of dictionary inorder to optimise this function to be used for saving other entity relations
	df = pd.DataFrame(d)
	# optional - you can save the pandas dataframe (df) in different formats such as .json, pickle etc.
	df.to_csv(filename+".csv",index=False)
	return



def get_multi_artist_links(artists):
	"""
	Info :

	Input : A list of string containing musicbrainz artist uids

	Output : A CSV file in your working directory for each entity0 and entity1 reletionships

	"""

	link_tables = ['l_artist_artist','l_artist_recording','l_artist_release_group','l_artist_work']
	all_entities = ['artist','recording','release_group','work']

	for key in zip(link_tables,all_entities):
		entity0_list = list()
		entity1_list = list()
		link_type_id = list()
		link_type_name = list()

		print "\n\n Scrapping-",key[0], key[1]

		for artist in artists:
			print "\n Computing for the artist- ",artist
			table = get_artistLinkTables(artist,key[0],key[1])
			if table is None:
				pass
			else:
				entity0_list.extend(table[0])
				entity1_list.extend(table[1])
				link_type_id.extend(table[2])
				link_type_name.extend(table[3])
				d = (entity0_list,entity1_list,link_type_id,link_type_name)

				# save to csv
				save_link_csv(d,"artist",key[1],key[0])

				print key[0],"--Table saved"
	return


def get_entity_links(entity0_uid,entity0_name,entity1_name):
	"""

	Info : Function to retieve all the link and link_type tables associated with a particular musicbrainz entity
			We are targeted to query the combinations of following tables to get the links between entities and their
			respective link_type fields.
			"artist, recording, release_groups, work"

			PS: If you want get relations with other entities like "label, area" etc,
			you have to optimise the sql string and if conditions in the get_entityGid() function.

	Input :
			entity0_uid : a string containing musicbrainz entity0 uid

			entity0_name : a string containing title of entity0 table. eg. 'artist'

			entity1_name : a string conataining the name of entity1 which is linked to the l_<entity0>_<entity1 table>
							eg. In "l_artist_recording" table, entity0_name is "artist" and entity1_name is "recording" 

			link_table_name : link table name. ie. l_artist_<entity1> . eg. "l_artist_recording"

	Output : A tuple containing a list of following values

			entity0_list : A list of musicbrainz uids. 
			entity1_list : A list of musicbrainz uids for the entity1 related to entity0.
			link_type_uid : A list of "link_type" table uid fields which defines the relations between entity0 and entity1
			link_type_name : A list of "link_type" table name fields which defines the realtion between entity0 and entity1

	"""
	links = list()
	entity1 = list()
	link_table_name = "l_"+entity0_name+"_"+entity1_name
	sql_string = "select link,entity1 from "+link_table_name+" l where l.entity0 in (select id from "+entity0_name+" where gid="
	cur.execute(sql_string+"%s)",(entity0_uid,))
	output = cur.fetchall()

	if len(output)!=0:
		for row in output:
			links.append(str(row[0]))
			entity1.append(str(row[1]))
		#return links, entity1

		entity0_list = list()
		entity1_list = list()
		link_type_id = list()
		link_type_name = list()
		for i in zip(links,entity1):
			link_type = get_link_types(i[0])
			entity0_list.append(entity0_uid)
			#print "\n Entity1 -->", i[1],"Links ->>",i[0],"\n"
			entity1_list.append(get_entityGid(i[1],entity1_name)) #
			link_type_id.append(link_type[0])
			link_type_name.append(link_type[1])
		return entity0_list, entity1_list, link_type_id, link_type_name
	else:
		return None
	return





