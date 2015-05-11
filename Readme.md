#Coord Converter

Performs simple spatial transformations on csv files


##Getting Started

First get the requirements

```bash
pip install -r requirements.txt
```

Then

```bash
./coord_converter --help
```

You can try the tool with the test data by running

```bash
./coord_converter.py -i test_data.csv -s 4326 -x lon -y lat -t 3857 -o outfile.csv
```
