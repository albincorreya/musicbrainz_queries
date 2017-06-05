# Some custom utitilty functions for different types of list and csv file processing in python 2.7

import sys, csv

#_____________________________________

"""
Some utility functions to process lists and tuples

"""

def str_unicode_decode(str_list):
    decoded_list = list()
    for s in str_list:
        str_decode = s.decode("utf-8","replace")
        decoded_list.append(str_decode)
    return decoded_list


#general with no order preservation
def remove_duplicate_listitems(mylist):
    newlist = list()
    for i in mylist:
        if i not in newlist:
            newlist.append(i)
    return newlist


#for unhashable objects
def remove_duplicate(alist):
    return list(set(alist))


def remove_duplicates_tupleList(tupleList):
    """
    info : get unique elements from a list of tuples by checking if there are multiple items list with the element of tuple[0] 
           is redundant, it removes it from the list and returns a list of all tuple[0] and tuple[1] list by preserving the order

    input : a list of tuple with 2 elements being the first element is the unique id to remove duplicates

    output : a list of all tuple[0] and tuple[1] elements of the tupleList seperately

    """
    item1 = list()
    item2 = list()
    for tuples in tupleList:
        if tuples[0] not in item1:
            item1.append(tuples[0])
            unique_index = tupleList.index(tuples)
            item2.append(tupleList[unique_index][1])
    return item1,item2



def get_row_length(filename):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            reader.line_num
        row_len = int(reader.line_num) - 1
    return row_len


def get_unique_rows_from_csv(filename,field):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        ids = list()
        i = 0
        test = list()
        row_len = get_row_length(filename)
        for row in reader:
            test.append(row[field])
    ids = remove_duplicate(test)
    return ids


def get_release_groups(artistid,filename):
    rgroup_list = list()
    rgroupids = list()
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["ArtistID"] == artistid:
                rgroup_list.append(row["ReleaseGroupID"])
    rgroupids = remove_duplicate(rgroup_list)
    return rgroupids 


#________________________________________________________________

"""
Some utility functions for handling CSV files

"""

# these are some utility functions to read the extracted CSV files and parse required fields for further queries..

def get_artists_from_csv(filename):
    """
    Info :  Function to retrieve all the artist musicbrainz uuid's from the csv file we had scrapped.
            The uuid's should be in the column with fieldname "artist.gid". You can optimise this function 
            for any column with differernt fieldnames.

    Input :  Filename of the CSV file. 

    Output : A list of strings containing musicbrainz artist uuids

    """
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        artists = list()
        for row in reader:
            artists.append(row['artist.gid'])
        remove_duplicate_listitems(artists)
    return artists


def get_unique_rows_from_csv(filename,field):
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        ids = list()
        i = 0
        test = list()
        row_len = get_row_length(filename)
        for row in reader:
            test.append(row[field])
    ids = remove_duplicate_listitems(test)
    return ids



def get_recording_ids_from_csv(rgroupid,filename):
    rec_list = list()
    recids = list()
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["ReleaseGroupID"] == rgroupid:
                rec_list.append(row["recording.gid"])
    recids = remove_duplicate(rec_list)
    return recids 



def get_artist_title_from_csv(filename,artistid):
    artist_title = list()
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["artist.gid"] == artistid: # edit this line inorder to filter the results by another filed name in the CSV
                artist_title = row["artist.name"]
                pass
    return artist_title


def get_rgroup_title_from_csv(filename,rgroupid):
    rgroup_title = list()
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["release_group.gid"] == rgroupid:
                rgroup_title = row["release_group.name"]
                pass
    return rgroup_title


def get_rec_title_from_csv(filename,recid):
    rec_title = list()
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["recording.group"] == recid:
                rec_title = row["recording.name"]
                pass
    return rec_title
