from latch.types.directory import LatchDir
from latch.types.metadata import (
    Fork,
    ForkBranch,
    LatchAuthor,
    NextflowMetadata,
    NextflowParameter,
    NextflowRuntimeResources,
    Params,
    Section,
    Spoiler,
    Text,
)

from .parameters import generated_parameters

flow = [
    Section(
        "Input/Options",
        Params("input", "outdir", "run_name"),
        Spoiler("Optional", Params("assembly_input", "", "single_end")),
    ),
    Spoiler(
        "Optional Parameters",
        Spoiler(
            "Skip Tools",
            Params(
                "skip_clipping",
                "skip_spades",
                "skip_spadeshybrid",
                "skip_megahit",
                "skip_binning",
                "skip_metabat2",
                "skip_maxbin2",
                "skip_concoct",
                "skip_binqc",
                "skip_quast",
                "skip_prodigal",
                "skip_prokka",
                "skip_metaeuk",
            ),
        ),
        Spoiler(
            "Assembly Options",
            Section("MEGAHIT", Params("megahit_fix_cpu_1", "megahit_options")),
            Section(
                "SPADES",
                Params("spades_fix_cpus", "spades_options", "spadeshybrid_fix_cpus"),
            ),
            Section("Coassembly", Params("coassemble_group")),
        ),
        Spoiler(
            "Quality Control",
            Spoiler(
                "Read Trimming Options",
                Params(
                    "save_clipped_reads",
                ),
                Fork(
                    "trimming_tool",
                    "",
                    fastp=ForkBranch(
                        "FastP",
                        Params(
                            "reads_minlength",
                            "fastp_qualified_quality",
                            "fastp_cut_mean_quality",
                            "fastp_save_trimmed_fail",
                        ),
                    ),
                    adapterremoval=ForkBranch(
                        "Adapter Sequence Removal",
                        Params(
                            "adapterremoval_minquality",
                            "adapterremoval_trim_quality_stretch",
                            "adapterremoval_adapter1",
                            "adapterremoval_adapter2",
                        ),
                    ),
                ),
            ),
            Spoiler(
                "Host Contamination Removal",
                Params(
                    "host_genome",
                    "host_fasta",
                    "host_removal_verysensitive",
                    "host_removal_save_ids",
                    "save_hostremoved_reads",
                    "keep_phix",
                    "save_phixremoved_reads",
                ),
            ),
            Spoiler(
                "Read Depth Normalization Options",
                Params("bbnorm", "bbnorm_target", "bbnorm_min", "save_bbnorm_reads"),
            ),
            Spoiler(
                "Long Read Options",
                Params(
                    "skip_adapter_trimming",
                    "longreads_min_length",
                    "longreads_keep_percent",
                    "longreads_length_weight",
                    "keep_lambda",
                    "save_lambdaremoved_reads",
                    "save_porechop_reads",
                    "save_filtlong_reads",
                ),
            ),
        ),
        Spoiler(
            "Pre Binning Taxonomic Annotation",
            Fork(
                "pre_taxonomic_annotation",
                "",
                centrifuge=ForkBranch("centrifuge", Params("centrifuge_db")),
                krona=ForkBranch("krona", Params("skip_krona", "krona_db")),
                kraken=ForkBranch("kraken", Params("kraken_db")),
            ),
        ),
        Spoiler(
            "Contig Binning Options",
            Spoiler(
                "Generic Binning Options",
                Params(
                    "metabat_rng_seed",
                    "min_contig_size",
                    "min_length_unbinned_contigs",
                    "max_unbinned_contigs",
                    "binning_map_mode",
                    "bowtie2_mode",
                    "save_assembly_mapped_reads",
                ),
            ),
            Spoiler(
                "Bin Refining Options",
                Params(
                    "refine_bins_dastool",
                    "refine_bins_dastool_threshold",
                    "postbinning_input",
                ),
            ),
            Spoiler(
                "Binning Quality Control Options",
                Fork(
                    "binqc",
                    "",
                    checkm=ForkBranch(
                        "CheckM", Params("checkm_db", "save_checkm_data")
                    ),
                    busco=ForkBranch(
                        "BUSCO",
                        Params(
                            "busco_db",
                            "busco_auto_lineage_prok",
                            "save_busco_db",
                            "busco_clean",
                        ),
                    ),
                ),
                Spoiler(
                    "Chimera Detection Options",
                    Params("run_gunc", "gunc_db", "gunc_database_type", "gunc_save_db"),
                ),
            ),
            Spoiler(
                "Post Binning Taxonomic Annotation",
                Fork(
                    "post_taxonomic_annotation",
                    "",
                    cat=ForkBranch(
                        "CAT",
                        Params(
                            "cat_db",
                            "cat_db_generate",
                            "save_cat_db",
                            "cat_official_taxonomy",
                        ),
                    ),
                    gtdb=ForkBranch(
                        "GTDB",
                        Params(
                            "skip_gtdbtk",
                            "gtdb_db",
                            "gtdb_mash",
                            "gtdbtk_min_completeness",
                            "gtdbtk_max_contamination",
                            "gtdbtk_min_perc_aa",
                            "gtdbtk_min_af",
                            "gtdbtk_pplacer_cpus",
                            "gtdbtk_pplacer_scratch",
                        ),
                    ),
                ),
            ),
        ),
        Spoiler(
            "Micro Eukaroyote Gene Prediction (metaeuk)",
            Params("metaeuk_mmseqs_db", "metaeuk_db", "save_mmseqs_db"),
        ),
        Spoiler(
            "Viral Elements (Genomad)",
            Params(
                "run_virus_identification",
                "genomad_db",
                "genomad_min_score",
                "genomad_splits",
            ),
        ),
        Spoiler(
            "Ancient DNA Analysis",
            Params(
                "ancient_dna",
                "pydamage_accuracy",
                "skip_ancient_damagecorrection",
                "freebayes_ploidy",
                "freebayes_min_basequality",
                "freebayes_minallelefreq",
                "bcftools_view_high_variant_quality",
                "bcftools_view_medium_variant_quality",
                "bcftools_view_minimal_allelesupport",
            ),
        ),
        Spoiler(
            "MultiQC Options", Params("multiqc_title", "multiqc_methods_description")
        ),
    ),
]

NextflowMetadata(
    display_name="nf-core/mag",
    author=LatchAuthor(
        name="Your Name",
    ),
    parameters=generated_parameters,
    runtime_resources=NextflowRuntimeResources(
        cpus=4,
        memory=8,
        storage_gib=100,
    ),
    flow=flow,
    log_dir=LatchDir("latch:///your_log_dir"),
)
