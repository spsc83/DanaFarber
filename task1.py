import fire
import sys
import os


def parse_fastq(fastq_file: str, target_length: int) -> float:
    """
    Parse a fastq file, return the ratio of sequences that are greater
    than given nucleotides long.
    :param fastq_file: The target fastq file.
    :param target_length: The given target nucleotides length.
    :return: The ratio.
    """
    total_read_num = 0
    target_read_num = 0
    with open(fastq_file, 'r') as fp:
        while True:
            read_name = fp.readline().strip()
            if not read_name:
                break
            sequence = fp.readline().strip()
            if sequence is None:
                print(f'Please check the format of the fastq file, sequence={sequence} read_name={read_name}',
                      file=sys.stderr)
                exit()
            line3 = fp.readline().strip()
            if not line3:
                print(f'Please check the format of the fastq file, line3={line3} read_name={read_name}',
                      file=sys.stderr)
                exit()
            qual_str = fp.readline().strip()
            if qual_str is None:
                print(f'Please check the format of the fastq file, qual_str={qual_str} read_name={read_name}',
                      file=sys.stderr)
                exit()
            if len(qual_str) != len(sequence):
                print(f'Please check the format of the fastq file, len(qual_str)={len(qual_str)}!='
                      f'len(seq)={len(sequence)} read_name={read_name}', file=sys.stderr)
                exit()
            total_read_num += 1
            if len(sequence) > target_length:
                target_read_num += 1
    return target_read_num / total_read_num


def find_fastqs(dir: str, target_length: int = 30) -> None:
    """
    For Task1.1
    Recursively find all FASTQ files in a directory and report each file name
    and the percent of sequences in that file that are greater than given nucleotides long.
    :param dir: Target directory.
    :param target_length: The given nucleotides long. Default value: 30.
    :return: None
    """
    if not os.path.exists(dir):
        print(f'Input directory [{dir}] doesn\'t exist', file=sys.stderr)
        exit()
    fq_set = set([])
    for path, dirs, files in os.walk(dir):
        for file in files:
            if not file.endswith('.fastq'):
                continue
            whole_file_name = os.path.realpath(os.path.join(path, file))
            if os.path.exists(whole_file_name):
                fq_set.add(whole_file_name)
    fq_list = list(fq_set)
    fq_list.sort()
    for fq_file in fq_list:
        ratio = parse_fastq(fq_file, target_length)
        print(f'{fq_file}\t{ratio:.2%}')


def parse_fasta(fasta_file: str, top_n: int = 10) -> None:
    """
    For Task 1.2
    Given a FASTA file with DNA sequences,
    find top n most frequent sequences and return the sequence and their counts in the file
    :param top_n: It will find top n most frequent sequences. Default value: 10.
    :param fasta_file: The target fastq file.
    :return: None
    """
    seq_dict = {}
    with open(fasta_file, 'r') as fp:
        while True:
            name_line = fp.readline()
            if not name_line:
                break
            seq = fp.readline()
            if not seq:
                print(f'Please check the format of the fastq file, requence_name={name_line.strip()}', file=sys.stderr)
                exit()
            if seq in seq_dict:
                seq_dict[seq] += 1
            else:
                seq_dict[seq] = 1
    ret_list = sorted(list(seq_dict.items()), key=lambda x: x[1], reverse=True)
    for i in range(top_n):
        print(f"{ret_list[i][0].strip()}\t{ret_list[i][1]}")


class Annotation(object):
    """
    Annotation data structure.
    Attributes:
        raw_data: The raw data line in the annotation file.
        chr: chromosome
        start: The start position.
        stop: The stop position. According to UCSC genome browser, the stop coordinate is the number in the file - 1
        distance: The number of bps in [start, stop]: stop - start + 1
    """

    def __init__(self, data_line):
        """
        Init Annotation with raw data line.
        :param data_line: The raw data line.
        """
        self.raw_data = data_line
        data_list = data_line.strip().split('\t')
        self.chr = data_list[0]
        self.start = int(data_list[3])
        self.stop = int(data_list[4]) - 1
        self.distance = self.stop - self.start + 1

    def __lt__(self, other):
        """
        Use the stop coordinate to sort.
        :param other: other Annotation instance.
        :return: if this instance is smaller than the other instance.
        """
        if self.stop < other.stop:
            return True
        else:
            return False


def load_target_pos(target_pos_file):
    """
    Load
    :param target_pos_file:
    :return:
    """
    target_dict = {}
    with open(target_pos_file, 'r') as fp:
        while True:
            data_line = fp.readline()
            if not data_line:
                break
            chrom, pos = data_line.strip().split('\t')
            if chrom not in target_dict:
                target_dict[chrom] = [int(pos)]
            else:
                target_dict[chrom].append(int(pos))
    for key, value in target_dict.items():
        target_dict[key] = sorted(value)
    return target_dict


def load_anno(anno_file):
    """
    Load the annotation file into a dictionary.
    The key is chromosome, the value is a sorted list of Annotation instance.
    :param anno_file: The annotation file.
    :return: The annotation dictionary.
    """
    anno_dict = {}
    with open(anno_file, 'r') as fp:
        while True:
            data_line = fp.readline()
            if not data_line:
                break
            chrom = data_line.split('\t')[0]
            anno = Annotation(data_line)
            if chrom not in anno_dict:
                anno_dict[chrom] = [anno]
            else:
                anno_dict[chrom].append(anno)

    for key, value in anno_dict.items():
        anno_dict[key] = sorted(value)
    return anno_dict


def annotation(target_pos_file: str, annotation_file: str, output: str) -> None:
    """
    For Task 1.3
    Given a chromosome and coordinates, write a program for looking up its annotation.
    Output Annotated file of gene name that input position overlaps.
    :param target_pos_file: chromosome and coordinates file
    :param annotation_file: annotation file
    :param output: output file
    :return: None
    """
    anno_dict = load_anno(annotation_file)
    target_dict = load_target_pos(target_pos_file)
    with open(output, 'w') as fp_out:  # todo: multiple process
        for target_chr, target_pos_list in target_dict.items():
            if target_chr not in anno_dict:
                continue
            anno_list = anno_dict[target_chr]  # type: list[Annotation]
            max_dist = max([i.distance for i in anno_list])
            index_l = 0
            for target_pos in target_pos_list:
                for i in range(index_l, len(anno_list)):
                    if target_pos > anno_list[i].stop:
                        tmp = i + 1
                    elif target_pos >= anno_list[i].start:
                        fp_out.write(f'{target_chr}\t{target_pos}\t{anno_list[i].raw_data}')
                    elif anno_list[i].stop - target_pos <= max_dist:
                        continue
                    else:
                        break
                index_l = tmp


# def annotation2(target_pos_file: str, annotation_file: str, output: str):
#     start = time.time()
#     anno_dict = load_anno(annotation_file)
#     print(f'load anno time {time.time() - start}')
#     target_dict = load_target_pos(target_pos_file)
#     with open(output, 'w') as fp_out:
#         for target_chr, target_pos_list in target_dict.items():
#             if target_chr not in anno_dict:
#                 continue
#             anno_list = anno_dict[target_chr]  # type: list[Annotation]
#             index_l = 0
#             for target_pos in target_pos_list:
#                 for i in range(index_l, len(anno_list)):
#                     if target_pos > anno_list[i].stop:
#                         tmp = i + 1
#                     elif target_pos >= anno_list[i].start:
#                         fp_out.write(f'{target_chr}\t{target_pos}\t{anno_list[i].raw_data}')
#                     else:
#                         continue
#                 index_l = tmp
#     end = time.time()
#     print(f'running time = {end - start}')
#
#
# def annotation(target_pos_file: str, annotation_file: str, output: str):
#     start = time.time()
#     anno_dict = load_anno(annotation_file)
#     with open(target_pos_file, 'r') as fp, open(output, 'w') as fp_out:
#         while True:
#             data_line = fp.readline()
#             if not data_line:
#                 break
#             chrom, pos = data_line.strip().split('\t')
#             pos = int(pos)
#             if chrom not in anno_dict:
#                 continue
#             target_anno_list = anno_dict[chrom]
#             for anno in target_anno_list:
#                 if anno.is_hit(chrom, pos):
#                     fp_out.write(f'{chrom}\t{pos}\t{anno.raw_data}')
#     end = time.time()
#     print(f'running time = {end - start}')


if __name__ == '__main__':
    fire.Fire()
