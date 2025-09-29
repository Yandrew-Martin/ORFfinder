#!/usr/local/bin/python3

import cgi, json
import os
import mysql.connector
import subprocess
import re
from biocode import utils

def main():

    #create a class for the orf data to be stored
    class Orf():
        id = None
        start = None
        end = None
        strand = None
        frame = None
        description = None
        seq_len = None

    print("Content-Type: application/json\n\n")
    form = cgi.FieldStorage()
    sequence = form.getvalue('sequence')

    #open temp file for sequence to be written
    tempseq = open('tempseq.fasta', "w+")
    tempseq.write(sequence)
    
    #run ORFfinder with temp file
    tempseq.close()
    subprocess.call(['./ORFfinder', '-in', 'tempseq.fasta', '-out', 'output.fasta'])

    #remove temp file
    os.remove('./tempseq.fasta')
    
    #prepare insert query where orf data will be placed in the database
    insert = "INSERT IGNORE INTO orf VALUES(%s, %s, %s, %s, %s, %s, %s);"

    # Load the fasta entries - fasta_dict_from_file creates a dictionary and returns it
    # Dictionary structure: ['id':['h':'s']]
    fasta = utils.fasta_dict_from_file("output.fasta")
    
    os.remove('./output.fasta')

    conn = mysql.connector.connect(user='amart161', password='AJstat6625', host='localhost', database='amart161')
    curs1 = conn.cursor()

    frame_list = [3,1,2]

    for id in fasta:
        # Create class as object and insert the corresponding variables from the fasta file
        info = re.split(":",id)
        orf_id = re.search("ORF\d+",info[0]).group(0)
        entry = Orf()
        entry.id = str(orf_id)
        entry.start = int(info[1])+1
        entry.end = int(info[2])+1
        if (int(entry.start) < int(entry.end)):
            entry.strand = "+"
            entry.frame = frame_list[int(entry.start)%3]

        else:
            entry.strand = "-"
            entry.frame = frame_list[int(entry.end)%3]
        entry.description = fasta[id]['h']
        entry.seq_len = (len(fasta[id]['s'])+1)*3
        #insert ORFs into database
        curs1.execute(insert, (str(entry.id), entry.start, entry.end, str(entry.strand), entry.frame, entry.seq_len, str(entry.description)))


    conn.commit()

    curs2 = conn.cursor()
    
    #prepare query to pull orf data from database and place into results dictionary
    qry = "SELECT * FROM orf"

    curs2.execute(qry)

    #create results dictionary and fill list with orf data
    results = { 'orf_count': 0, 'orfs': list() }
    for row in curs2:
        results['orfs'].append({'orf_id': row[0], 'start': row[1], 'end': row[2], 'strand': row[3], 'frame': row[4], 'seq_len': row[5], 'description': row[6]})
        results['orf_count'] += 1
    
    curs3 = conn.cursor()
    
    qry = "DELETE FROM orf;"

    curs3.execute(qry)
    conn.commit()

    curs1.close()	
    curs2.close()
    curs3.close()
    conn.close()

    print(json.dumps(results))


if __name__ == '__main__':
    main()
