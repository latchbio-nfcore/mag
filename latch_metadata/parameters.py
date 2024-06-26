
from dataclasses import dataclass
import typing
import typing_extensions

from flytekit.core.annotation import FlyteAnnotation

from latch.types.metadata import NextflowParameter
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir

# Import these into your `__init__.py` file:
#
# from .parameters import generated_parameters

generated_parameters = {
    'input': NextflowParameter(
        type=str,
        default=None,
        section_title='Input/output options',
        description='CSV samplesheet file containing information about the samples in the experiment.',
    ),
    'single_end': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specifies that the input is single-end reads.',
    ),
    'assembly_input': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Additional input CSV samplesheet containing information about pre-computed assemblies. When set, both read pre-processing and assembly are skipped and the pipeline begins at the binning stage.',
    ),
    'outdir': NextflowParameter(
        type=typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})],
        default=None,
        section_title=None,
        description='The output directory where the results will be saved. You have to use absolute paths to storage on Cloud infrastructure.',
    ),
    'email': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Email address for completion summary.',
    ),
    'multiqc_title': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='MultiQC report title. Printed as page header, used for filename if not otherwise specified.',
    ),
    'multiqc_methods_description': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title='Generic options',
        description='Custom MultiQC yaml file containing HTML including a methods description.',
    ),
    'megahit_fix_cpu_1': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Reproducibility options',
        description='Fix number of CPUs for MEGAHIT to 1. Not increased with retries.',
    ),
    'spades_fix_cpus': NextflowParameter(
        type=typing.Optional[int],
        default=-1,
        section_title=None,
        description='Fix number of CPUs used by SPAdes. Not increased with retries.',
    ),
    'spadeshybrid_fix_cpus': NextflowParameter(
        type=typing.Optional[int],
        default=-1,
        section_title=None,
        description='Fix number of CPUs used by SPAdes hybrid. Not increased with retries.',
    ),
    'metabat_rng_seed': NextflowParameter(
        type=typing.Optional[int],
        default=1,
        section_title=None,
        description='RNG seed for MetaBAT2.',
    ),
    'clip_tool': NextflowParameter(
        type=typing.Optional[str],
        default='fastp',
        section_title='Quality control for short reads options',
        description='Specify which adapter clipping tool to use.',
    ),
    'save_clipped_reads': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specify to save the resulting clipped FASTQ files to --outdir.',
    ),
    'reads_minlength': NextflowParameter(
        type=typing.Optional[int],
        default=15,
        section_title=None,
        description='The minimum length of reads must have to be retained for downstream analysis.',
    ),
    'fastp_qualified_quality': NextflowParameter(
        type=typing.Optional[int],
        default=15,
        section_title=None,
        description='Minimum phred quality value of a base to be qualified in fastp.',
    ),
    'fastp_cut_mean_quality': NextflowParameter(
        type=typing.Optional[int],
        default=15,
        section_title=None,
        description='The mean quality requirement used for per read sliding window cutting by fastp.',
    ),
    'fastp_save_trimmed_fail': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save reads that fail fastp filtering in a separate file. Not used downstream.',
    ),
    'adapterremoval_minquality': NextflowParameter(
        type=typing.Optional[int],
        default=2,
        section_title=None,
        description='The minimum base quality for low-quality base trimming by AdapterRemoval.',
    ),
    'adapterremoval_trim_quality_stretch': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Turn on quality trimming by consecutive stretch of low quality bases, rather than by window.',
    ),
    'adapterremoval_adapter1': NextflowParameter(
        type=typing.Optional[str],
        default='AGATCGGAAGAGCACACGTCTGAACTCCAGTCACNNNNNNATCTCGTATGCCGTCTTCTGCTTG',
        section_title=None,
        description='Forward read adapter to be trimmed by AdapterRemoval.',
    ),
    'adapterremoval_adapter2': NextflowParameter(
        type=typing.Optional[str],
        default='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT',
        section_title=None,
        description='Reverse read adapter to be trimmed by AdapterRemoval for paired end data.',
    ),
    'host_genome': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Name of iGenomes reference for host contamination removal.',
    ),
    'host_fasta': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Fasta reference file for host contamination removal.',
    ),
    'host_removal_verysensitive': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Use the `--very-sensitive` instead of the`--sensitive`setting for Bowtie 2 to map reads against the host genome.',
    ),
    'host_removal_save_ids': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save the read IDs of removed host reads.',
    ),
    'save_hostremoved_reads': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specify to save input FASTQ files with host reads removed to --outdir.',
    ),
    'keep_phix': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Keep reads similar to the Illumina internal standard PhiX genome.',
    ),
    'skip_clipping': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip read preprocessing using fastp or adapterremoval.',
    ),
    'save_phixremoved_reads': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specify to save input FASTQ files with phiX reads removed to --outdir.',
    ),
    'bbnorm': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Run BBnorm to normalize sequence depth.',
    ),
    'bbnorm_target': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title=None,
        description='Set BBnorm target maximum depth to this number.',
    ),
    'bbnorm_min': NextflowParameter(
        type=typing.Optional[int],
        default=5,
        section_title=None,
        description='Set BBnorm minimum depth to this number.',
    ),
    'save_bbnorm_reads': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save normalized read files to output directory.',
    ),
    'skip_adapter_trimming': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Quality control for long reads options',
        description='Skip removing adapter sequences from long reads.',
    ),
    'longreads_min_length': NextflowParameter(
        type=typing.Optional[int],
        default=1000,
        section_title=None,
        description='Discard any read which is shorter than this value.',
    ),
    'longreads_keep_percent': NextflowParameter(
        type=typing.Optional[int],
        default=90,
        section_title=None,
        description='Keep this percent of bases.',
    ),
    'longreads_length_weight': NextflowParameter(
        type=typing.Optional[int],
        default=10,
        section_title=None,
        description='The higher the more important is read length when choosing the best reads.',
    ),
    'keep_lambda': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Keep reads similar to the ONT internal standard Escherichia virus Lambda genome.',
    ),
    'save_lambdaremoved_reads': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specify to save input FASTQ files with lamba reads removed  to --outdir.',
    ),
    'save_porechop_reads': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specify to save the resulting clipped FASTQ files to --outdir.',
    ),
    'save_filtlong_reads': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Specify to save the resulting length filtered FASTQ files to --outdir.',
    ),
    'centrifuge_db': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title='Taxonomic profiling options',
        description='Database for taxonomic binning with centrifuge.',
    ),
    'kraken2_db': NextflowParameter(
        type=typing.Optional[LatchFile],
        default=None,
        section_title=None,
        description='Database for taxonomic binning with kraken2.',
    ),
    'krona_db': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Database for taxonomic binning with krona',
    ),
    'skip_krona': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip creating a krona plot for taxonomic binning.',
    ),
    'cat_db': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Database for taxonomic classification of metagenome assembled genomes. Can be either a zipped file or a directory containing the extracted output of such.',
    ),
    'cat_db_generate': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Generate CAT database.',
    ),
    'save_cat_db': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save the CAT database generated when specified by `--cat_db_generate`.',
    ),
    'cat_official_taxonomy': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Only return official taxonomic ranks (Kingdom, Phylum, etc.) when running CAT.',
    ),
    'skip_gtdbtk': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip the running of GTDB, as well as the automatic download of the database',
    ),
    'gtdb_db': NextflowParameter(
        type=typing.Optional[str],
        default='https://data.ace.uq.edu.au/public/gtdb/data/releases/release214/214.1/auxillary_files/gtdbtk_r214_data.tar.gz',
        section_title=None,
        description='Specify the location of a GTDBTK database. Can be either an uncompressed directory or a `.tar.gz` archive. If not specified will be downloaded for you when GTDBTK or binning QC is not skipped.',
    ),
    'gtdb_mash': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Specify the location of a GTDBTK mash database. If missing, GTDB-Tk will skip the ani_screening step',
    ),
    'gtdbtk_min_completeness': NextflowParameter(
        type=typing.Optional[float],
        default=50,
        section_title=None,
        description='Min. bin completeness (in %) required to apply GTDB-tk classification.',
    ),
    'gtdbtk_max_contamination': NextflowParameter(
        type=typing.Optional[float],
        default=10,
        section_title=None,
        description='Max. bin contamination (in %) allowed to apply GTDB-tk classification.',
    ),
    'gtdbtk_min_perc_aa': NextflowParameter(
        type=typing.Optional[float],
        default=10,
        section_title=None,
        description='Min. fraction of AA (in %) in the MSA for bins to be kept.',
    ),
    'gtdbtk_min_af': NextflowParameter(
        type=typing.Optional[float],
        default=0.65,
        section_title=None,
        description='Min. alignment fraction to consider closest genome.',
    ),
    'gtdbtk_pplacer_cpus': NextflowParameter(
        type=typing.Optional[float],
        default=1,
        section_title=None,
        description='Number of CPUs used for the by GTDB-Tk run tool pplacer.',
    ),
    'gtdbtk_pplacer_scratch': NextflowParameter(
        type=typing.Optional[bool],
        default=True,
        section_title=None,
        description='Reduce GTDB-Tk memory consumption by running pplacer in a setting writing to disk.',
    ),
    'genomad_db': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Database for virus classification with geNomad',
    ),
    'coassemble_group': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Assembly options',
        description='Co-assemble samples within one group, instead of assembling each sample separately.',
    ),
    'spades_options': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Additional custom options for SPAdes.',
    ),
    'megahit_options': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Additional custom options for MEGAHIT.',
    ),
    'skip_spades': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip Illumina-only SPAdes assembly.',
    ),
    'skip_spadeshybrid': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip SPAdes hybrid assembly.',
    ),
    'skip_megahit': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip MEGAHIT assembly.',
    ),
    'skip_quast': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip metaQUAST.',
    ),
    'skip_prodigal': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Gene prediction and annotation options',
        description='Skip Prodigal gene prediction',
    ),
    'skip_prokka': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip Prokka genome annotation.',
    ),
    'skip_metaeuk': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip MetaEuk gene prediction and annotation',
    ),
    'metaeuk_mmseqs_db': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='A string containing the name of one of the databases listed in the [mmseqs2 documentation](https://github.com/soedinglab/MMseqs2/wiki#downloading-databases). This database will be downloaded and formatted for eukaryotic genome annotation. Incompatible with --metaeuk_db.',
    ),
    'metaeuk_db': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to either a local fasta file of protein sequences, or to a directory containing an mmseqs2-formatted database, for annotation of eukaryotic genomes.',
    ),
    'save_mmseqs_db': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save the downloaded mmseqs2 database specified in `--metaeuk_mmseqs_db`.',
    ),
    'run_virus_identification': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Virus identification options',
        description='Run virus identification.',
    ),
    'genomad_min_score': NextflowParameter(
        type=typing.Optional[float],
        default=0.7,
        section_title=None,
        description='Minimum geNomad score for a sequence to be considered viral',
    ),
    'genomad_splits': NextflowParameter(
        type=typing.Optional[int],
        default=1,
        section_title=None,
        description="Number of groups that geNomad's MMSeqs2 databse should be split into (reduced memory requirements)",
    ),
    'binning_map_mode': NextflowParameter(
        type=typing.Optional[str],
        default='group',
        section_title='Binning options',
        description='Defines mapping strategy to compute co-abundances for binning, i.e. which samples will be mapped against the assembly.',
    ),
    'skip_binning': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip metagenome binning entirely',
    ),
    'skip_metabat2': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip MetaBAT2 Binning',
    ),
    'skip_maxbin2': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip MaxBin2 Binning',
    ),
    'skip_concoct': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Skip CONCOCT Binning',
    ),
    'min_contig_size': NextflowParameter(
        type=typing.Optional[int],
        default=1500,
        section_title=None,
        description='Minimum contig size to be considered for binning and for bin quality check.',
    ),
    'min_length_unbinned_contigs': NextflowParameter(
        type=typing.Optional[int],
        default=1000000,
        section_title=None,
        description='Minimal length of contigs that are not part of any bin but treated as individual genome.',
    ),
    'max_unbinned_contigs': NextflowParameter(
        type=typing.Optional[int],
        default=100,
        section_title=None,
        description='Maximal number of contigs that are not part of any bin but treated as individual genome.',
    ),
    'bowtie2_mode': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Bowtie2 alignment mode',
    ),
    'save_assembly_mapped_reads': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save the output of mapping raw reads back to assembled contigs',
    ),
    'bin_domain_classification': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Enable domain-level (prokaryote or eukaryote) classification of bins using Tiara. Processes which are domain-specific will then only receive bins matching the domain requirement.',
    ),
    'tiara_min_length': NextflowParameter(
        type=typing.Optional[int],
        default=3000,
        section_title=None,
        description='Minimum contig length for Tiara to use for domain classification. For accurate classification, should be longer than 3000 bp.',
    ),
    'skip_binqc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Bin quality check options',
        description='Disable bin QC with BUSCO or CheckM.',
    ),
    'binqc_tool': NextflowParameter(
        type=typing.Optional[str],
        default='busco',
        section_title=None,
        description='Specify which tool for bin quality-control validation to use.',
    ),
    'busco_db': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Download URL for BUSCO lineage dataset, or path to a tar.gz archive, or local directory containing already downloaded and unpacked lineage datasets.',
    ),
    'busco_auto_lineage_prok': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Run BUSCO with automated lineage selection, but ignoring eukaryotes (saves runtime).',
    ),
    'save_busco_db': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save the used BUSCO lineage datasets provided via `--busco_db`.',
    ),
    'busco_clean': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Enable clean-up of temporary files created during BUSCO runs.',
    ),
    'checkm_db': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Path to local folder containing already downloaded and uncompressed CheckM database.',
    ),
    'save_checkm_data': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save the used CheckM reference files downloaded when not using --checkm_db parameter.',
    ),
    'refine_bins_dastool': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Turn on bin refinement using DAS Tool.',
    ),
    'refine_bins_dastool_threshold': NextflowParameter(
        type=typing.Optional[float],
        default=0.5,
        section_title=None,
        description='Specify single-copy gene score threshold for bin refinement.',
    ),
    'postbinning_input': NextflowParameter(
        type=typing.Optional[str],
        default='raw_bins_only',
        section_title=None,
        description='Specify which binning output is sent for downstream annotation, taxonomic classification, bin quality control etc.',
    ),
    'run_gunc': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Turn on GUNC genome chimerism checks',
    ),
    'gunc_db': NextflowParameter(
        type=typing.Optional[str],
        default=None,
        section_title=None,
        description='Specify a path to a pre-downloaded GUNC dmnd database file',
    ),
    'gunc_database_type': NextflowParameter(
        type=typing.Optional[str],
        default='progenomes',
        section_title=None,
        description='Specify which database to auto-download if not supplying own',
    ),
    'gunc_save_db': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='Save the used GUNC reference files downloaded when not using --gunc_db parameter.',
    ),
    'ancient_dna': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title='Ancient DNA assembly',
        description='Turn on/off the ancient DNA subworfklow',
    ),
    'pydamage_accuracy': NextflowParameter(
        type=typing.Optional[float],
        default=0.5,
        section_title=None,
        description='PyDamage accuracy threshold',
    ),
    'skip_ancient_damagecorrection': NextflowParameter(
        type=typing.Optional[bool],
        default=None,
        section_title=None,
        description='deactivate damage correction of ancient contigs using variant and consensus calling',
    ),
    'freebayes_ploidy': NextflowParameter(
        type=typing.Optional[int],
        default=1,
        section_title=None,
        description='Ploidy for variant calling',
    ),
    'freebayes_min_basequality': NextflowParameter(
        type=typing.Optional[int],
        default=20,
        section_title=None,
        description='minimum base quality required for variant calling',
    ),
    'freebayes_minallelefreq': NextflowParameter(
        type=typing.Optional[float],
        default=0.33,
        section_title=None,
        description='minimum minor allele frequency for considering variants',
    ),
    'bcftools_view_high_variant_quality': NextflowParameter(
        type=typing.Optional[int],
        default=30,
        section_title=None,
        description='minimum genotype quality for considering a variant high quality',
    ),
    'bcftools_view_medium_variant_quality': NextflowParameter(
        type=typing.Optional[int],
        default=20,
        section_title=None,
        description='minimum genotype quality for considering a variant medium quality',
    ),
    'bcftools_view_minimal_allelesupport': NextflowParameter(
        type=typing.Optional[int],
        default=3,
        section_title=None,
        description='minimum number of bases supporting the alternative allele',
    ),
}

