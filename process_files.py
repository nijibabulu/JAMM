#! /usr/bin/env python3

import os
import functools
import click

def outfile_name(samples_dir, prefix, sample_file, chrom):
    sample_base = os.path.basename(sample_file)
    return f"{samples_dir}/{prefix}.{chrom}.{sample_base}"

@click.command()
@click.argument("SAMPLE_FILE")
@click.argument("PREFIX")
@click.argument("SIZE_FILE")
@click.argument("SAMPLES_DIR")
def main(sample_file, prefix, size_file, samples_dir):
    """
    Split out the samples file information into individual, chromosome-specific
    mapping information. Should be given a bed file with samples, an ouptut
    prefix (either sample or bkgd) a two (or
    more) column file with chromosome names and sizes, and an output directory.
    """

    of = functools.partial(outfile_name, samples_dir, prefix, sample_file)

    # create all the files in case some will be empty
    with open(size_file) as f:
        for line in f:
            chrom = line.split()[0].strip()
            if len(chrom):
                open(of(chrom), "w")

    chrom_data = dict()
    with open(sample_file) as f:
        for line in f:
            fields = line.strip().split('\t')
            chrom_data.setdefault(
                fields[0], []).append(f"{fields[1]}\t{fields[5]}")

    for chrom, content in chrom_data.items():
        open(of(chrom), "w").write("\n".join(content))



if __name__ == "__main__":
    main()

