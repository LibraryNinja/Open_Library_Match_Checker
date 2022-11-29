# Open Library Match Checker
Checks ISBNs from an Alma Analytics report against the Open Library API identify items that aren't in their collection to send them

# Notes
- My input file is directly from Alma Analytics, so code here skips the first two rows that include the title of the report and a blank row
- My input file also has quotes around the MMS ID to prevent cutoff in Excel and other places
