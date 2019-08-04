READ ME - Ramesh Kalagnanam - Hawaii Weather Analysis

I would like to provide a few notes about the Jupiter Notebook and Flask files I have submitted as follows:

1. I requested Lisa Shemancik to give me an extension of two days and she was kind enough to grant my request.
   Lisa also confirmed that in person with Michael Dinh during the class on Saturday, August 3, 2019.
   
2. With respect to the query of "prcp" for the 12-month period, it gives 2,021 values because it is retrieving
   values from various weather stations for the given day (Cell 12 has the code and Cell 13 has a display of the header).  
   
   In addition to this, I also calculated average precipitation recorded at all weather stations for a 
   given day. This gave me 366 values for the 366 days beginning August 23, 2016. I suppose I could have altered the start 
   date such that I would have 365 days. I am assuming this is OK.
   
   In the FLASK application, I have chosen to display the average precipitation for each days as described above. This was a 
   choice I made based on the fact that it will display a manageable amount of data.
   
3. For the bar charts, I tried to read up on it to understand better but I have not encountered using "max - min" difference.
   The tutorials said either standard deviation or standard error is commonly used (https://www.youtube.com/watch?v=NMcogBp1rnA&t=238s).

4. For FLASK, in the last two routes, the URL should resemble the following:

		For the route /api/v1.0/start:

		http://127.0.0.1:5000/api/v1.0/2017-05-01
		
		and for the route /api/v1.0/begin/end:
		
		http://127.0.0.1:5000/api/v1.0/2017-05-01/2017-05-15
		
5. I have incorporated code which verifies that the end date is later than begin date in the second route above. If the condition is not met,
   it will return an error.
		
