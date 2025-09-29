# Final-Project
Final project

--ABOUT--

This is a web front end display for an ORFfinder program

Source code: https://github.com/amarti54/Final-Project

Demo at: http://bfx3.aap.jhu.edu/amart161/Final%20Project/ORFfinder.html

Utilizes NCBI ORFfinder as primary analyzing program
Source: ftp://ftp.ncbi.nlm.nih.gov/genomes/TOOLS/ORFfinder/linux-i64/

--REQUIREMENTS--

MySql Database
Python3 utilities

Minimal storage (~25MB)
Minimum RAM: 1GB
OS: Linux x64

--USAGE--

1. Enter in a sequence into the text area, may contain fasta style heading, but does not require it. 
Input must contain A, T, G, or C, in any given order. Do not exceed 5,000bp.

2. Click 'Submit'

3. The sequence will be piped through the ORFfinder and the following information will be displayed:
-ORF ID- -Start- -End- -Strand- -Frame- -Sequence Length- -Description-

--DEMO--

1. Must be on the class server, bfx3.aap.jhu.edu
2. Proceed to http://bfx3.aap.jhu.edu/amart161/Final%20Project/ORFfinder.html
3. Copy and Paste the sample DNA sequence found within the sample_sequence.txt file
4. Enjoy the newly found ORFs!