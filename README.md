# DanaFarber code test repo
## 1 Prepare python environment
Python version: 3.8.0

```shell
pip install -r requirements.txt 
```

## 2 Running
### Task1.1 - Recursively find all FASTQ files in a directory and report each file name and the percent of sequences in that file that are greater than 30 nucleotides long.
```shell
python task1.py find_fastqs <fastq_directory>
# e.g.: python task1.py find_fastqs data/sample_files/fastq 
```
### Task1.2 - Given a FASTA file with DNA sequences, find 10 most frequent sequences and return the sequence and their counts in the file.
```shell
python task1.py parse_fasta <fasta_file>
# e.g.: python task1.py parse_fasta data/sample_files/fasta/sample.fasta
```
### Task1.3 - Given a chromosome and coordinates, write a program for looking up its annotation. Keep in mind you'll be doing this annotation millions of times. Output Annotated file of gene name that input position overlaps.
```shell
python task1.py annotation <chromosome_coordinate_file> <annotation_file> <output_file>
# e.g.: python task1.py annotation data/sample_files/annotate/coordinates_to_annotate.txt data/sample_files/gtf/hg19_annotations.gtf output
```
### Task2 - Report the mean target coverage for the intervals grouped by GC% bins.
```shell
python task2.py parse_coverage <coverage_file>
# e.g.: python task2.py parse_coverage data/Example.hs_intervals.txt
```
### Task3.1 - Given a list of variant IDs, using Ensembl API retrieve information about alleles, locations, effects of variants in transcripts, and genes containing the transcripts.
```shell
python task3.py query_rsids <rs_id1,rs_id2>
# e.g.: python task3.py query_rsids rs56116432 or python task3.py query_rsids rs56116432,rs2332914
```
### Task3.2 - Create a repository on GitHub and upload your code there. Make some minor changes to your code locally, and use a local Git installation to commit the changes to your GitHub repository.
This is the repository.