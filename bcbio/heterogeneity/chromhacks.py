"""Hacks to handle subsetting of chromosomes for heterogeneity analysis.

This puts ugly chromosome naming assumptions that restrict heterogeneity estimations
to autosomal chromosomes in a single place.
"""
from bcbio import utils
from bcbio.distributed.transaction import file_transaction

def _is_autosomal(chrom):
    """Keep chromosomes that are a digit 1-22, or chr prefixed digit chr1-chr22
    """
    try:
        int(chrom)
        return True
    except ValueError:
        try:
            int(str(chrom.replace("chr", "")))
            return True
        except ValueError:
            return False

def bed_to_standardonly(in_file, data):
    out_file = "%s-stdchrs%s" % utils.splitext_plus(in_file)
    if not utils.file_exists(out_file):
        with file_transaction(data, out_file) as tx_out_file:
            with open(in_file) as in_handle:
                with open(tx_out_file, "w") as out_handle:
                    for line in in_handle:
                        if _is_autosomal(line.split()[0]):
                            out_handle.write(line)
    return out_file