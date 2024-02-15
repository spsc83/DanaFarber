import fire
import requests

server = "https://rest.ensembl.org"


def parse_variation(data_dict):
    """
    Parse a variation data dictionary into [most_severe_consequence, mapping info] list.
    The mapping info is a list of [location, alleles, ancestral_allele]
    Args:
        data_dict:
            A particular variation dictionary in the response of GET variation/:species/:id or POST variation/:species/
            References:
                https://rest.ensembl.org/documentation/info/variation_id
                https://rest.ensembl.org/documentation/info/variation_post

    Returns:
        [most_severe_consequence, mapping_list] list.
    """
    most_severe_consequence = data_dict['most_severe_consequence']
    mapping_list = []
    for mapping_dict in data_dict["mappings"]:
        location = mapping_dict['location']
        alleles = mapping_dict['allele_string']
        ancestral_allele = mapping_dict['ancestral_allele']
        mapping_list.append([location, alleles, ancestral_allele])
    return [most_severe_consequence, mapping_list]


def parse_consequence(data_dict):
    """
    Parse a consequence data of a particular variant into a list of
    [variant_allele, transcript_id, consequence_terms, gene_id]
    Args:
        data_dict: The consequence data of a particular variant.
        References:
            https://rest.ensembl.org/documentation/info/vep_id_get
            https://rest.ensembl.org/documentation/info/vep_id_post

    Returns:
        A list of [variant_allele, transcript_id, consequence_terms, gene_id]
    """
    consequence_list = []
    for trans_dict in data_dict["transcript_consequences"]:
        consequence_terms = ','.join(trans_dict['consequence_terms'])
        transcript_id = trans_dict['transcript_id']
        gene_id = trans_dict['gene_id']
        variant_allele = trans_dict['variant_allele']
        consequence_list.append([variant_allele, transcript_id, consequence_terms, gene_id])
    return consequence_list


def query_rsids(rs_ids, species: str = 'human') -> None:
    """
    Report the alleles, locations, effects of variants in transcripts, and genes containing the transcripts information
    via Ensembl API for a list rs ids.
    Args:
        rs_ids: target rs id list. e.g.: rs56116432,rs2332914
        species: Species. Default is 'human'.

    Returns:
        None
    """
    if type(rs_ids) == str:
        rs_ids = (rs_ids,)
    assert type(rs_ids) == tuple, 'rs_ids should be a tuple'
    # collecting data
    rs_ids_str = str(list(rs_ids)).replace("'", '"')
    ext = f"/variation/{species}"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    r = requests.post(server + ext, headers=headers, data=f'{{ "ids" : {rs_ids_str}}}')
    if not r.ok:
        r.raise_for_status()
        exit()
    variants_dict = r.json()

    ext = "/vep/human/id"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    r = requests.post(server + ext, headers=headers, data=f'{{ "ids" : {rs_ids_str} }}')
    if not r.ok:
        r.raise_for_status()
        exit()
    consequence_list = r.json()
    # double-check
    for rs_id in [i['id'] for i in consequence_list]:
        if rs_id not in variants_dict:
            print(f'Did not get information for {rs_id} via /variation/{species} API. Please try again.')
            exit()
    # reporting
    for consequence_dict in consequence_list:
        rs_id = consequence_dict['id']
        print(f'{rs_id}:')
        variant_dict = variants_dict[rs_id]
        most_severe_consequence, mapping_list = parse_variation(variant_dict)
        consequence_list = parse_consequence(consequence_dict)
        print(f'most_severe_consequence={most_severe_consequence}')
        for location, alleles, ancestral_allele in mapping_list:
            print(f'location={location}\talleles={alleles}\tancestral_allele={ancestral_allele}')
        print('Effects of variants in transcripts, and genes containing the transcripts:')
        for variant_allele, transcript_id, consequence_terms, gene_id in consequence_list:
            print(f'variant_allele={variant_allele}\ttranscript_id={transcript_id}\tconsequence_terms='
                  f'{consequence_terms}\tgene_id={gene_id}')
        print('\n')


if __name__ == '__main__':
    fire.Fire()
