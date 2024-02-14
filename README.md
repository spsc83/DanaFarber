# DanaFarber code test repo
## 1 Prepare python environment
Python version: 3.8.0

```shell
pip install -r requirements.txt 
```

## 2 Running
###Task1.1 - Recursively find all FASTQ files in a directory and report each file name and the percent of sequences in that file that are greater than 30 nucleotides long.
```shell
python task1.py find_fastqs <fastq_directory>
```
###Task1.2 - Given a FASTA file with DNA sequences, find 10 most frequent sequences and return the sequence and their counts in the file.
```shell
python task1.py parse_fasta <fasta_file>
```
###Task1.3 - Given a chromosome and coordinates, write a program for looking up its annotation. Keep in mind you'll be doing this annotation millions of times. Output Annotated file of gene name that input position overlaps.
```shell
python task1.py annotation <chromosome_coordinate_file> <annotation_file> <output_file>
```
