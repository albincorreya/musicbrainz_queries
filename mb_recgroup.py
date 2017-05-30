from fuzzywuzzy import process
from my_utils import *
import uuid
import sys;
reload(sys);
sys.setdefaultencoding("utf8")



def string_match_recordings(recordings_list,str_match_threshold):
	"""
	INFO : Function to compute the possible string match candidates for a recording tilte from a 
			list of recording titles associated with a musicbrainz artist uid

	Input :
			recordings_list : A list of string containing recording titles of all recordings associated 
							with a artist

			str_match_threshold : String matching threshold value for the string matching algorithm. 
								Any value between 0 - 100. After some trial and error, 88 found out to be a optimal
								value to str_match_threshold for generating best string matches from recordings.

			(This function uses the string matching algorithm from fuzzywuzzy python package which is based on difflib, refer  >> https://github.com/seatgeek/fuzzywuzzy)

	Output : A list of lists with possible string matches for all the recording titles

	"""
	full_match_list = list()
	print "\nStarting string matching, it would take a while for big recording collections, please be patient....\n"
	for a in recordings_list:
		str_matches = process.extractBests(a,recordings_list)
		match_list = list()
		ref_matches = list()
		for s in str_matches:
			sidx = str_matches.index(s)
			if s[1] >=str_match_threshold: #Threshod value for process.extractBests() function to select possible matches
				match_list.append(s[0])
				ref_matches = remove_duplicate_listitems(match_list)
		full_match_list.append(ref_matches)
	#return full_match_list
	print "First order matching done....\nbeginning second order matching.....\n"
	return_matches = list()
	match_iter = full_match_list
	for j in match_iter:
		newlist = list()
		fref_list = list()
		for match in full_match_list:
			for m in match:
				if m in j:
					newlist.extend(match)
			fref_list = remove_duplicate_listitems(newlist)
			return_matches.append(fref_list)
	f_return_matches = remove_duplicate_listitems(return_matches)
	print "String matching done ....\n"
	return f_return_matches




def generate_recording_group(match_list,recording_list):
	"""
	Info : Function to generate Unique identifiers to for recordings of same artist with similar 
			titles. Designed to use along with string_match_recordings() function. 
	Input:
			match_list : A list of lists with possible string matches for all the recording titles. 
						(output of string_match_recordings() function)
			recording_list: A list of string containing recording titles of all recordings associated 
							with a artist

	Output : A list of recording group ids for the all the recordings in the recording_list

	"""
	recgroup = [None] * len(recording_list)
	print "\n Generating new recording group UID's for the string match list..., this might take a while big recording collections...\n, Please be patient........\n"
	for match in match_list:
		i = 0 
		uid = uuid.uuid4()
		for rec in recording_list:
			if rec in match:
				#idx = recording_list.index(rec) # stopped using list.index () since it gives same index for duplicate elements
				recgroup[i] = str(uid)
			i = i+1
			if i>= len(recording_list):
				i = 0
				pass
	for r in recgroup:
		if r is None:
			recgroup[recgroup.index(r)] = str(uuid.uuid4())
	print "Finished generating recording group ids ......"
	return recgroup
# add another code block to check if there are multiple rows with same recording ids then assign the recording id



