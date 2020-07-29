First of all
`pip install -r requirements.txt`

Using cURL:
In case of running from localhost and on port 5000,
abs-path-to-csv-file - absolute path to file
`curl -F 'csv_file=@abs-path-to-csv-file' http://localhost:5000/api/getAddresses`

Reason to use `geopy.distance.geodesic`:
https://en.wikipedia.org/wiki/Vincenty%27s_formulae