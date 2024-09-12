import os
import shutil
import subprocess
import sys
import typing
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import requests
import typing_extensions
from flytekit.core.annotation import FlyteAnnotation
from latch.executions import report_nextflow_used_storage
from latch.ldata.path import LPath
from latch.resources.tasks import custom_task, nextflow_runtime_task
from latch.resources.workflow import workflow
from latch.types import metadata
from latch.types.directory import LatchDir, LatchOutputDir
from latch.types.file import LatchFile
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.nextflow.workflow import get_flag
from latch_cli.services.register.utils import import_module_by_path
from latch_cli.utils import urljoins

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata


def get_flag_defaults(
    name: str, val: typing.Any, default_val: typing.Optional[typing.Any]
):
    if val == default_val or val is None:
        return ""
    else:
        return get_flag(name=name, val=val)


@custom_task(cpu=0.25, memory=0.5, storage_gib=1)
def initialize() -> str:
    token = os.environ.get("FLYTE_INTERNAL_EXECUTION_ID")
    if token is None:
        raise RuntimeError("failed to get execution token")

    headers = {"Authorization": f"Latch-Execution-Token {token}"}

    print("Provisioning shared storage volume... ", end="")
    resp = requests.post(
        "http://nf-dispatcher-service.flyte.svc.cluster.local/provision-storage",
        headers=headers,
        json={
            "storage_expiration_hours": 0,
            "version": 2,
        },
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]


@dataclass
class Assembly_SampleSheet:
    id: str
    group: str
    assembler: str
    fasta: LatchFile


@dataclass
class SampleSheet:
    sample: str
    run: typing.Optional[str]
    group: str
    short_reads_1: LatchFile
    short_reads_2: typing.Optional[LatchFile]
    long_reads: typing.Optional[LatchFile]


input_construct_samplesheet = metadata._nextflow_metadata.parameters[
    "input"
].samplesheet_constructor

assembly_input_construct_samplesheet = metadata._nextflow_metadata.parameters[
    "assembly_input"
].samplesheet_constructor


@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(
    pvc_name: str,
    input: typing.List[SampleSheet],
    run_name: str,
    assembly_input: typing.List[Assembly_SampleSheet],
    outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({"output": True})],
    email: typing.Optional[str],
    multiqc_title: typing.Optional[str],
    multiqc_methods_description: typing.Optional[str],
    megahit_fix_cpu_1: bool,
    trimming_tool: str,
    save_clipped_reads: bool,
    adapterremoval_trim_quality_stretch: bool,
    host_fasta: typing.Optional[LatchFile],
    save_hostremoved_reads: bool,
    keep_phix: bool,
    save_phixremoved_reads: bool,
    skip_adapter_trimming: bool,
    keep_lambda: bool,
    save_lambdaremoved_reads: bool,
    save_porechop_reads: bool,
    save_filtlong_reads: bool,
    centrifuge_db: typing.Optional[LatchFile],
    kraken2_db: typing.Optional[LatchDir],
    krona_db: typing.Optional[LatchDir],
    skip_krona: bool,
    cat_db: typing.Optional[LatchDir],
    cat_db_generate: bool,
    save_cat_db: bool,
    skip_gtdbtk: bool,
    gtdb_mash: typing.Optional[LatchDir],
    genomad_db: typing.Optional[LatchDir],
    coassemble_group: bool,
    spades_options: typing.Optional[str],
    megahit_options: typing.Optional[str],
    skip_spades: bool,
    skip_spadeshybrid: bool,
    skip_megahit: bool,
    skip_quast: bool,
    skip_prodigal: bool,
    skip_prokka: bool,
    skip_metaeuk: bool,
    metaeuk_mmseqs_db: typing.Optional[LatchDir],
    metaeuk_db: typing.Optional[LatchDir],
    save_mmseqs_db: bool,
    run_virus_identification: bool,
    skip_binning: bool,
    skip_metabat2: bool,
    skip_maxbin2: bool,
    skip_concoct: bool,
    bowtie2_mode: typing.Optional[str],
    save_assembly_mapped_reads: bool,
    bin_domain_classification: bool,
    skip_binqc: bool,
    binqc_tool: typing.Optional[str],
    busco_db: typing.Optional[LatchDir],
    busco_auto_lineage_prok: bool,
    save_busco_db: bool,
    checkm_db: typing.Optional[LatchDir],
    save_checkm_data: bool,
    refine_bins_dastool: bool,
    gunc_db: typing.Optional[LatchFile],
    gunc_save_db: bool,
    skip_ancient_damagecorrection: bool,
    single_end: bool,
    spades_fix_cpus: typing.Optional[int],
    spadeshybrid_fix_cpus: typing.Optional[int],
    metabat_rng_seed: typing.Optional[int],
    clip_tool: str,
    reads_minlength: typing.Optional[int],
    fastp_qualified_quality: typing.Optional[int],
    fastp_cut_mean_quality: typing.Optional[int],
    fastp_save_trimmed_fail: bool,
    adapterremoval_minquality: typing.Optional[int],
    adapterremoval_adapter1: typing.Optional[str],
    adapterremoval_adapter2: typing.Optional[str],
    host_removal_verysensitive: bool,
    host_removal_save_ids: bool,
    skip_clipping: bool,
    bbnorm: bool,
    bbnorm_target: typing.Optional[int],
    bbnorm_min: typing.Optional[int],
    save_bbnorm_reads: bool,
    longreads_min_length: typing.Optional[int],
    longreads_keep_percent: typing.Optional[int],
    longreads_length_weight: typing.Optional[int],
    cat_official_taxonomy: bool,
    gtdb_db: typing.Optional[str],
    gtdbtk_min_completeness: typing.Optional[float],
    gtdbtk_max_contamination: typing.Optional[float],
    gtdbtk_min_perc_aa: typing.Optional[float],
    gtdbtk_min_af: typing.Optional[float],
    gtdbtk_pplacer_cpus: typing.Optional[int],
    gtdbtk_pplacer_scratch: bool,
    genomad_min_score: typing.Optional[float],
    genomad_splits: typing.Optional[int],
    binning_map_mode: typing.Optional[str],
    min_contig_size: typing.Optional[int],
    min_length_unbinned_contigs: typing.Optional[int],
    max_unbinned_contigs: typing.Optional[int],
    tiara_min_length: typing.Optional[int],
    busco_clean: bool,
    refine_bins_dastool_threshold: typing.Optional[float],
    postbinning_input: typing.Optional[str],
    run_gunc: bool,
    gunc_database_type: typing.Optional[str],
    ancient_dna: bool,
    pydamage_accuracy: typing.Optional[float],
    freebayes_ploidy: typing.Optional[int],
    freebayes_min_basequality: typing.Optional[int],
    freebayes_minallelefreq: typing.Optional[float],
    bcftools_view_high_variant_quality: typing.Optional[int],
    bcftools_view_medium_variant_quality: typing.Optional[int],
    bcftools_view_minimal_allelesupport: typing.Optional[int],
) -> None:
    shared_dir = Path("/nf-workdir")

    input_samplesheet = input_construct_samplesheet(input)
    assembly_input_samplesheet = assembly_input_construct_samplesheet(assembly_input)

    ignore_list = [
        "latch",
        ".latch",
        ".git",
        "nextflow",
        ".nextflow",
        "work",
        "results",
        "miniconda",
        "anaconda3",
        "mambaforge",
    ]

    shutil.copytree(
        Path("/root"),
        shared_dir,
        ignore=lambda src, names: ignore_list,
        ignore_dangling_symlinks=True,
        dirs_exist_ok=True,
    )

    profile_list = ["docker"]

    if len(profile_list) == 0:
        profile_list.append("standard")

    profiles = ",".join(profile_list)

    cmd = [
        "/root/nextflow",
        "run",
        str(shared_dir / "main.nf"),
        "-work-dir",
        str(shared_dir),
        "-profile",
        profiles,
        "-c",
        "latch.config",
        "-resume",
        *get_flag("input", input_samplesheet),
        # *get_flag("run_name", run_name),
        *get_flag_defaults("single_end", single_end, False),
    ]

    if len(assembly_input) > 0:
        cmd += [*get_flag("assembly_input", assembly_input_samplesheet)]

    cmd += [
        *get_flag("outdir", outdir),
        *get_flag_defaults("email", email, None),
        *get_flag_defaults("multiqc_title", multiqc_title, None),
        *get_flag_defaults(
            "multiqc_methods_description", multiqc_methods_description, None
        ),
        *get_flag_defaults("megahit_fix_cpu_1", megahit_fix_cpu_1, 1),
        *get_flag_defaults("spades_fix_cpus", spades_fix_cpus, -1),
        *get_flag_defaults("spadeshybrid_fix_cpus", spadeshybrid_fix_cpus, -1),
        *get_flag_defaults("metabat_rng_seed", metabat_rng_seed, 1),
        *get_flag_defaults("clip_tool", trimming_tool, "fastp"),
        *get_flag_defaults("save_clipped_reads", save_clipped_reads, True),
        *get_flag_defaults("reads_minlength", reads_minlength, 15),
        *get_flag_defaults("fastp_qualified_quality", fastp_qualified_quality, 15),
        *get_flag_defaults("fastp_cut_mean_quality", fastp_cut_mean_quality, 15),
        *get_flag_defaults("fastp_save_trimmed_fail", fastp_save_trimmed_fail, False),
        *get_flag_defaults("adapterremoval_minquality", adapterremoval_minquality, 2),
        *get_flag_defaults(
            "adapterremoval_trim_quality_stretch",
            adapterremoval_trim_quality_stretch,
            None,
        ),
        *get_flag_defaults(
            "adapterremoval_adapter1",
            adapterremoval_adapter1,
            "AGATCGGAAGAGCACACGTCTGAACTCCAGTCACNNNNNNATCTCGTATGCCGTCTTCTGCTTG",
        ),
        *get_flag_defaults(
            "adapterremoval_adapter2",
            adapterremoval_adapter2,
            "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT",
        ),
        *get_flag_defaults("host_fasta", host_fasta, None),
        *get_flag_defaults(
            "host_removal_verysensitive", host_removal_verysensitive, False
        ),
        *get_flag_defaults("host_removal_save_ids", host_removal_save_ids, True),
        *get_flag_defaults("save_hostremoved_reads", save_hostremoved_reads, None),
        *get_flag_defaults("keep_phix", keep_phix, None),
        *get_flag_defaults("skip_clipping", skip_clipping, False),
        *get_flag_defaults("save_phixremoved_reads", save_phixremoved_reads, None),
        *get_flag_defaults("bbnorm", bbnorm, False),
        *get_flag_defaults("bbnorm_target", bbnorm_target, 100),
        *get_flag_defaults("bbnorm_min", bbnorm_min, 5),
        *get_flag_defaults("save_bbnorm_reads", save_bbnorm_reads, False),
        *get_flag_defaults("skip_adapter_trimming", skip_adapter_trimming, None),
        *get_flag_defaults("longreads_min_length", longreads_min_length, 1000),
        *get_flag_defaults("longreads_keep_percent", longreads_keep_percent, 90),
        *get_flag_defaults("longreads_length_weight", longreads_length_weight, 10),
        *get_flag_defaults("keep_lambda", keep_lambda, None),
        *get_flag_defaults("save_lambdaremoved_reads", save_lambdaremoved_reads, None),
        *get_flag_defaults("save_porechop_reads", save_porechop_reads, None),
        *get_flag_defaults("save_filtlong_reads", save_filtlong_reads, None),
        *get_flag_defaults("centrifuge_db", centrifuge_db, None),
        *get_flag_defaults("kraken2_db", kraken2_db, None),
        *get_flag_defaults("krona_db", krona_db, None),
        *get_flag_defaults("skip_krona", skip_krona, None),
        *get_flag_defaults("cat_db", cat_db, None),
        *get_flag_defaults("cat_db_generate", cat_db_generate, None),
        *get_flag_defaults("save_cat_db", save_cat_db, None),
        *get_flag_defaults("cat_official_taxonomy", cat_official_taxonomy, True),
        *get_flag_defaults("skip_gtdbtk", skip_gtdbtk, None),
        *get_flag_defaults(
            "gtdb_db",
            gtdb_db,
            "https://data.ace.uq.edu.au/public/gtdb/data/releases/release214/214.1/auxillary_files/gtdbtk_r214_data.tar.gz",
        ),
        *get_flag_defaults("gtdb_mash", gtdb_mash, None),
        *get_flag_defaults("gtdbtk_min_completeness", gtdbtk_min_completeness, 50.0),
        *get_flag_defaults("gtdbtk_max_contamination", gtdbtk_max_contamination, 10.0),
        *get_flag_defaults("gtdbtk_min_perc_aa", gtdbtk_min_perc_aa, 10.0),
        *get_flag_defaults("gtdbtk_min_af", gtdbtk_min_af, 0.65),
        *get_flag_defaults("gtdbtk_pplacer_cpus", gtdbtk_pplacer_cpus, 1),
        *get_flag_defaults("gtdbtk_pplacer_scratch", gtdbtk_pplacer_scratch, True),
        *get_flag_defaults("genomad_db", genomad_db, None),
        *get_flag_defaults("coassemble_group", coassemble_group, None),
        *get_flag_defaults("spades_options", spades_options, None),
        *get_flag_defaults("megahit_options", megahit_options, None),
        *get_flag_defaults("skip_spades", skip_spades, None),
        *get_flag_defaults("skip_spadeshybrid", skip_spadeshybrid, None),
        *get_flag_defaults("skip_megahit", skip_megahit, None),
        *get_flag_defaults("skip_quast", skip_quast, None),
        *get_flag_defaults("skip_prodigal", skip_prodigal, None),
        *get_flag_defaults("skip_prokka", skip_prokka, None),
        *get_flag_defaults("skip_metaeuk", skip_metaeuk, None),
        *get_flag_defaults("metaeuk_mmseqs_db", metaeuk_mmseqs_db, None),
        *get_flag_defaults("metaeuk_db", metaeuk_db, None),
        *get_flag_defaults("save_mmseqs_db", save_mmseqs_db, None),
        *get_flag_defaults("run_virus_identification", run_virus_identification, None),
        *get_flag_defaults("genomad_min_score", genomad_min_score, 0.7),
        *get_flag_defaults("genomad_splits", genomad_splits, 1),
        *get_flag_defaults("binning_map_mode", binning_map_mode, "group"),
        *get_flag_defaults("skip_binning", skip_binning, None),
        *get_flag_defaults("skip_metabat2", skip_metabat2, None),
        *get_flag_defaults("skip_maxbin2", skip_maxbin2, None),
        *get_flag_defaults("skip_concoct", skip_concoct, None),
        *get_flag_defaults("min_contig_size", min_contig_size, 1500),
        *get_flag_defaults(
            "min_length_unbinned_contigs", min_length_unbinned_contigs, 1000000
        ),
        *get_flag_defaults("max_unbinned_contigs", max_unbinned_contigs, 100),
        *get_flag_defaults("bowtie2_mode", bowtie2_mode, None),
        *get_flag_defaults(
            "save_assembly_mapped_reads", save_assembly_mapped_reads, None
        ),
        *get_flag_defaults(
            "bin_domain_classification", bin_domain_classification, None
        ),
        *get_flag_defaults("tiara_min_length", tiara_min_length, 3000),
        *get_flag_defaults("skip_binqc", skip_binqc, None),
        *get_flag_defaults("binqc_tool", binqc_tool, None),
        *get_flag_defaults("busco_db", busco_db, None),
        *get_flag_defaults("busco_auto_lineage_prok", busco_auto_lineage_prok, None),
        *get_flag_defaults("save_busco_db", save_busco_db, None),
        *get_flag_defaults("busco_clean", busco_clean, True),
        *get_flag_defaults("checkm_db", checkm_db, None),
        *get_flag_defaults("save_checkm_data", save_checkm_data, None),
        *get_flag_defaults("refine_bins_dastool", refine_bins_dastool, None),
        *get_flag_defaults(
            "refine_bins_dastool_threshold", refine_bins_dastool_threshold, 0.50
        ),
        *get_flag_defaults("postbinning_input", postbinning_input, "raw_bins_only"),
        *get_flag_defaults("run_gunc", run_gunc, False),
        *get_flag_defaults("gunc_db", gunc_db, None),
        *get_flag_defaults("gunc_database_type", gunc_database_type, None),
        *get_flag_defaults("gunc_save_db", gunc_save_db, None),
        *get_flag_defaults("ancient_dna", ancient_dna, None),
        *get_flag_defaults("pydamage_accuracy", pydamage_accuracy, None),
        *get_flag_defaults(
            "skip_ancient_damagecorrection", skip_ancient_damagecorrection, None
        ),
        *get_flag_defaults("freebayes_ploidy", freebayes_ploidy, None),
        *get_flag_defaults(
            "freebayes_min_basequality", freebayes_min_basequality, None
        ),
        *get_flag_defaults("freebayes_minallelefreq", freebayes_minallelefreq, None),
        *get_flag_defaults(
            "bcftools_view_high_variant_quality",
            bcftools_view_high_variant_quality,
            None,
        ),
        *get_flag_defaults(
            "bcftools_view_medium_variant_quality",
            bcftools_view_medium_variant_quality,
            None,
        ),
        *get_flag_defaults(
            "bcftools_view_minimal_allelesupport",
            bcftools_view_minimal_allelesupport,
            None,
        ),
    ]

    print("Launching Nextflow Runtime")
    print(" ".join(cmd))
    print(flush=True)

    failed = False
    try:
        env = {
            **os.environ,
            "NXF_ANSI_LOG": "false",
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms1536M -Xmx6144M -XX:ActiveProcessorCount=4",
            "NXF_DISABLE_CHECK_LATEST": "true",
            "NXF_ENABLE_VIRTUAL_THREADS": "false",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    except subprocess.CalledProcessError:
        failed = True
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(
                    urljoins(
                        "latch:///your_log_dir/nf_nf_core_mag", name, "nextflow.log"
                    )
                )
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)

        print("Computing size of workdir... ", end="")
        try:
            result = subprocess.run(
                ["du", "-sb", str(shared_dir)],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5 * 60,
            )

            size = int(result.stdout.split()[0])
            report_nextflow_used_storage(size)
            print(f"Done. Workdir size: {size / 1024 / 1024 / 1024: .2f} GiB")
        except subprocess.TimeoutExpired:
            print(
                "Failed to compute storage size: Operation timed out after 5 minutes."
            )
        except subprocess.CalledProcessError as e:
            print(f"Failed to compute storage size: {e.stderr}")
        except Exception as e:
            print(f"Failed to compute storage size: {e}")

    if failed:
        sys.exit(1)


@workflow(metadata._nextflow_metadata)
def nf_nf_core_mag(
    input: typing.List[SampleSheet],
    run_name: str,
    assembly_input: typing.List[Assembly_SampleSheet],
    outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({"output": True})],
    email: typing.Optional[str],
    multiqc_title: typing.Optional[str],
    multiqc_methods_description: typing.Optional[str],
    megahit_fix_cpu_1: bool,
    trimming_tool: str,
    save_clipped_reads: bool,
    adapterremoval_trim_quality_stretch: bool,
    host_fasta: typing.Optional[LatchFile],
    save_hostremoved_reads: bool,
    keep_phix: bool,
    save_phixremoved_reads: bool,
    skip_adapter_trimming: bool,
    keep_lambda: bool,
    save_lambdaremoved_reads: bool,
    save_porechop_reads: bool,
    save_filtlong_reads: bool,
    centrifuge_db: typing.Optional[LatchFile],
    kraken2_db: typing.Optional[LatchDir],
    krona_db: typing.Optional[LatchDir],
    skip_krona: bool,
    cat_db: typing.Optional[LatchDir],
    cat_db_generate: bool,
    save_cat_db: bool,
    skip_gtdbtk: bool,
    gtdb_mash: typing.Optional[LatchDir],
    genomad_db: typing.Optional[LatchDir],
    coassemble_group: bool,
    spades_options: typing.Optional[str],
    megahit_options: typing.Optional[str],
    skip_spades: bool,
    skip_spadeshybrid: bool,
    skip_megahit: bool,
    skip_quast: bool,
    skip_prodigal: bool,
    skip_prokka: bool,
    skip_metaeuk: bool,
    metaeuk_mmseqs_db: typing.Optional[LatchDir],
    metaeuk_db: typing.Optional[LatchDir],
    save_mmseqs_db: bool,
    run_virus_identification: bool,
    skip_binning: bool,
    skip_metabat2: bool,
    skip_maxbin2: bool,
    skip_concoct: bool,
    bowtie2_mode: typing.Optional[str],
    save_assembly_mapped_reads: bool,
    bin_domain_classification: bool,
    skip_binqc: bool,
    binqc_tool: typing.Optional[str],
    busco_db: typing.Optional[LatchDir],
    busco_auto_lineage_prok: bool,
    save_busco_db: bool,
    checkm_db: typing.Optional[LatchDir],
    save_checkm_data: bool,
    refine_bins_dastool: bool,
    gunc_db: typing.Optional[LatchFile],
    gunc_save_db: bool,
    skip_ancient_damagecorrection: bool,
    single_end: bool = False,
    spades_fix_cpus: typing.Optional[int] = -1,
    spadeshybrid_fix_cpus: typing.Optional[int] = -1,
    metabat_rng_seed: typing.Optional[int] = 1,
    clip_tool: str = "fastp",
    reads_minlength: typing.Optional[int] = 15,
    fastp_qualified_quality: typing.Optional[int] = 15,
    fastp_cut_mean_quality: typing.Optional[int] = 15,
    fastp_save_trimmed_fail: bool = False,
    adapterremoval_minquality: typing.Optional[int] = 2,
    adapterremoval_adapter1: typing.Optional[
        str
    ] = "AGATCGGAAGAGCACACGTCTGAACTCCAGTCACNNNNNNATCTCGTATGCCGTCTTCTGCTTG",
    adapterremoval_adapter2: typing.Optional[
        str
    ] = "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT",
    host_removal_verysensitive: bool = False,
    host_removal_save_ids: bool = True,
    skip_clipping: bool = False,
    bbnorm: bool = False,
    bbnorm_target: typing.Optional[int] = 100,
    bbnorm_min: typing.Optional[int] = 5,
    save_bbnorm_reads: bool = False,
    longreads_min_length: typing.Optional[int] = 1000,
    longreads_keep_percent: typing.Optional[int] = 90,
    longreads_length_weight: typing.Optional[int] = 10,
    cat_official_taxonomy: bool = True,
    gtdb_db: typing.Optional[
        str
    ] = "https://data.ace.uq.edu.au/public/gtdb/data/releases/release214/214.1/auxillary_files/gtdbtk_r214_data.tar.gz",
    gtdbtk_min_completeness: typing.Optional[float] = 50.0,
    gtdbtk_max_contamination: typing.Optional[float] = 10.0,
    gtdbtk_min_perc_aa: typing.Optional[float] = 10.0,
    gtdbtk_min_af: typing.Optional[float] = 0.65,
    gtdbtk_pplacer_cpus: typing.Optional[int] = 1,
    gtdbtk_pplacer_scratch: bool = True,
    genomad_min_score: typing.Optional[float] = 0.7,
    genomad_splits: typing.Optional[int] = 1,
    binning_map_mode: typing.Optional[str] = "group",
    min_contig_size: typing.Optional[int] = 1500,
    min_length_unbinned_contigs: typing.Optional[int] = 1000000,
    max_unbinned_contigs: typing.Optional[int] = 100,
    tiara_min_length: typing.Optional[int] = 3000,
    busco_clean: bool = True,
    refine_bins_dastool_threshold: typing.Optional[float] = 0.5,
    postbinning_input: typing.Optional[str] = "raw_bins_only",
    run_gunc: bool = False,
    gunc_database_type: typing.Optional[str] = "progenomes",
    ancient_dna: bool = False,
    pydamage_accuracy: typing.Optional[float] = 0.5,
    freebayes_ploidy: typing.Optional[int] = 1,
    freebayes_min_basequality: typing.Optional[int] = 20,
    freebayes_minallelefreq: typing.Optional[float] = 0.33,
    bcftools_view_high_variant_quality: typing.Optional[int] = 30,
    bcftools_view_medium_variant_quality: typing.Optional[int] = 20,
    bcftools_view_minimal_allelesupport: typing.Optional[int] = 3,
) -> None:
    """
    nf-core/mag

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(
        pvc_name=pvc_name,
        input=input,
        run_name=run_name,
        single_end=single_end,
        assembly_input=assembly_input,
        outdir=outdir,
        email=email,
        multiqc_title=multiqc_title,
        multiqc_methods_description=multiqc_methods_description,
        megahit_fix_cpu_1=megahit_fix_cpu_1,
        spades_fix_cpus=spades_fix_cpus,
        spadeshybrid_fix_cpus=spadeshybrid_fix_cpus,
        metabat_rng_seed=metabat_rng_seed,
        trimming_tool=trimming_tool,
        clip_tool=clip_tool,
        save_clipped_reads=save_clipped_reads,
        reads_minlength=reads_minlength,
        fastp_qualified_quality=fastp_qualified_quality,
        fastp_cut_mean_quality=fastp_cut_mean_quality,
        fastp_save_trimmed_fail=fastp_save_trimmed_fail,
        adapterremoval_minquality=adapterremoval_minquality,
        adapterremoval_trim_quality_stretch=adapterremoval_trim_quality_stretch,
        adapterremoval_adapter1=adapterremoval_adapter1,
        adapterremoval_adapter2=adapterremoval_adapter2,
        host_fasta=host_fasta,
        host_removal_verysensitive=host_removal_verysensitive,
        host_removal_save_ids=host_removal_save_ids,
        save_hostremoved_reads=save_hostremoved_reads,
        keep_phix=keep_phix,
        skip_clipping=skip_clipping,
        save_phixremoved_reads=save_phixremoved_reads,
        bbnorm=bbnorm,
        bbnorm_target=bbnorm_target,
        bbnorm_min=bbnorm_min,
        save_bbnorm_reads=save_bbnorm_reads,
        skip_adapter_trimming=skip_adapter_trimming,
        longreads_min_length=longreads_min_length,
        longreads_keep_percent=longreads_keep_percent,
        longreads_length_weight=longreads_length_weight,
        keep_lambda=keep_lambda,
        save_lambdaremoved_reads=save_lambdaremoved_reads,
        save_porechop_reads=save_porechop_reads,
        save_filtlong_reads=save_filtlong_reads,
        centrifuge_db=centrifuge_db,
        kraken2_db=kraken2_db,
        krona_db=krona_db,
        skip_krona=skip_krona,
        cat_db=cat_db,
        cat_db_generate=cat_db_generate,
        save_cat_db=save_cat_db,
        cat_official_taxonomy=cat_official_taxonomy,
        skip_gtdbtk=skip_gtdbtk,
        gtdb_db=gtdb_db,
        gtdb_mash=gtdb_mash,
        gtdbtk_min_completeness=gtdbtk_min_completeness,
        gtdbtk_max_contamination=gtdbtk_max_contamination,
        gtdbtk_min_perc_aa=gtdbtk_min_perc_aa,
        gtdbtk_min_af=gtdbtk_min_af,
        gtdbtk_pplacer_cpus=gtdbtk_pplacer_cpus,
        gtdbtk_pplacer_scratch=gtdbtk_pplacer_scratch,
        genomad_db=genomad_db,
        coassemble_group=coassemble_group,
        spades_options=spades_options,
        megahit_options=megahit_options,
        skip_spades=skip_spades,
        skip_spadeshybrid=skip_spadeshybrid,
        skip_megahit=skip_megahit,
        skip_quast=skip_quast,
        skip_prodigal=skip_prodigal,
        skip_prokka=skip_prokka,
        skip_metaeuk=skip_metaeuk,
        metaeuk_mmseqs_db=metaeuk_mmseqs_db,
        metaeuk_db=metaeuk_db,
        save_mmseqs_db=save_mmseqs_db,
        run_virus_identification=run_virus_identification,
        genomad_min_score=genomad_min_score,
        genomad_splits=genomad_splits,
        binning_map_mode=binning_map_mode,
        skip_binning=skip_binning,
        skip_metabat2=skip_metabat2,
        skip_maxbin2=skip_maxbin2,
        skip_concoct=skip_concoct,
        min_contig_size=min_contig_size,
        min_length_unbinned_contigs=min_length_unbinned_contigs,
        max_unbinned_contigs=max_unbinned_contigs,
        bowtie2_mode=bowtie2_mode,
        save_assembly_mapped_reads=save_assembly_mapped_reads,
        bin_domain_classification=bin_domain_classification,
        tiara_min_length=tiara_min_length,
        skip_binqc=skip_binqc,
        binqc_tool=binqc_tool,
        busco_db=busco_db,
        busco_auto_lineage_prok=busco_auto_lineage_prok,
        save_busco_db=save_busco_db,
        busco_clean=busco_clean,
        checkm_db=checkm_db,
        save_checkm_data=save_checkm_data,
        refine_bins_dastool=refine_bins_dastool,
        refine_bins_dastool_threshold=refine_bins_dastool_threshold,
        postbinning_input=postbinning_input,
        run_gunc=run_gunc,
        gunc_db=gunc_db,
        gunc_database_type=gunc_database_type,
        gunc_save_db=gunc_save_db,
        ancient_dna=ancient_dna,
        pydamage_accuracy=pydamage_accuracy,
        skip_ancient_damagecorrection=skip_ancient_damagecorrection,
        freebayes_ploidy=freebayes_ploidy,
        freebayes_min_basequality=freebayes_min_basequality,
        freebayes_minallelefreq=freebayes_minallelefreq,
        bcftools_view_high_variant_quality=bcftools_view_high_variant_quality,
        bcftools_view_medium_variant_quality=bcftools_view_medium_variant_quality,
        bcftools_view_minimal_allelesupport=bcftools_view_minimal_allelesupport,
    )
