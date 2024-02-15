import fire
import csv


def get_bin_name(gc: float) -> str:
    """
    Generate the bin name with given gc value. gc values range from 0 to 1.
    Args:
        gc: The given gc value.

    Returns:
        The bin name string.
    """
    assert 0 <= gc <= 1, f'GC values range from 0 to 1'
    if gc == 1:
        return f"90-100%gc"
    for i in range(10):
        if i * 10 <= gc * 100 < i * 10 + 10:
            return f'{i * 10:2}-{i * 10 + 10}%gc'


def parse_coverage(coverage_file: str) -> None:
    """
    Parse the coverage file and report the mean target coverage for
    the intervals grouped by GC% bins. Bin in 10%GC intervals
    Args:
        coverage_file: The coverage file.

    Returns:
        None
    """
    with open(coverage_file) as fp:
        reader = csv.reader(fp, dialect="excel-tab")
        header = next(reader)
        bin_dict = {}
        for line in reader:
            line = [i for i in line if len(i) > 0]
            length = int(line[header.index('length')])
            gc = float(line[header.index('%gc')])
            mean_coverage = float(line[header.index('mean_coverage')])
            bin_name = get_bin_name(gc)
            if bin_name not in bin_dict:
                bin_dict[bin_name] = [length * mean_coverage / 100, length]
            else:
                cover_num, total_num = bin_dict[bin_name]
                cover_num += length * mean_coverage / 100
                total_num += length
                bin_dict[bin_name] = [cover_num, total_num]
        print('Bin name\tmean target coverage')
        for bin_name, num_list in sorted(list(bin_dict.items()), key=lambda x: x[0]):
            cover_num, total_num = num_list
            print(f'{bin_name}\t{cover_num / total_num:.2%}')


if __name__ == '__main__':
    fire.Fire()
