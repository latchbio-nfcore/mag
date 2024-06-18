from dataclasses import dataclass
from enum import Enum
import os
import subprocess
import requests
import shutil
from pathlib import Path
import typing
import typing_extensions

from latch.resources.workflow import workflow
from latch.resources.tasks import nextflow_runtime_task, custom_task
from latch.types.file import LatchFile
from latch.types.directory import LatchDir, LatchOutputDir
from latch.ldata.path import LPath
from latch_cli.nextflow.workflow import get_flag
from latch_cli.nextflow.utils import _get_execution_name
from latch_cli.utils import urljoins
from latch.types import metadata
from flytekit.core.annotation import FlyteAnnotation

from latch_cli.services.register.utils import import_module_by_path

meta = Path("latch_metadata") / "__init__.py"
import_module_by_path(meta)
import latch_metadata

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
            "storage_gib": 100,
        }
    )
    resp.raise_for_status()
    print("Done.")

    return resp.json()["name"]






@nextflow_runtime_task(cpu=4, memory=8, storage_gib=100)
def nextflow_runtime(pvc_name: str, input: str, single_end: typing.Optional[bool], assembly_input: typing.Optional[str], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], multiqc_methods_description: typing.Optional[str], megahit_fix_cpu_1: typing.Optional[bool], save_clipped_reads: typing.Optional[bool], fastp_save_trimmed_fail: typing.Optional[bool], adapterremoval_trim_quality_stretch: typing.Optional[bool], host_genome: typing.Optional[str], host_fasta: typing.Optional[str], host_removal_verysensitive: typing.Optional[bool], host_removal_save_ids: typing.Optional[bool], save_hostremoved_reads: typing.Optional[bool], keep_phix: typing.Optional[bool], skip_clipping: typing.Optional[bool], save_phixremoved_reads: typing.Optional[bool], bbnorm: typing.Optional[bool], save_bbnorm_reads: typing.Optional[bool], skip_adapter_trimming: typing.Optional[bool], keep_lambda: typing.Optional[bool], save_lambdaremoved_reads: typing.Optional[bool], save_porechop_reads: typing.Optional[bool], save_filtlong_reads: typing.Optional[bool], centrifuge_db: typing.Optional[LatchFile], kraken2_db: typing.Optional[LatchFile], krona_db: typing.Optional[str], skip_krona: typing.Optional[bool], cat_db: typing.Optional[str], cat_db_generate: typing.Optional[bool], save_cat_db: typing.Optional[bool], cat_official_taxonomy: typing.Optional[bool], skip_gtdbtk: typing.Optional[bool], gtdb_mash: typing.Optional[str], genomad_db: typing.Optional[str], coassemble_group: typing.Optional[bool], spades_options: typing.Optional[str], megahit_options: typing.Optional[str], skip_spades: typing.Optional[bool], skip_spadeshybrid: typing.Optional[bool], skip_megahit: typing.Optional[bool], skip_quast: typing.Optional[bool], skip_prodigal: typing.Optional[bool], skip_prokka: typing.Optional[bool], skip_metaeuk: typing.Optional[bool], metaeuk_mmseqs_db: typing.Optional[str], metaeuk_db: typing.Optional[str], save_mmseqs_db: typing.Optional[bool], run_virus_identification: typing.Optional[bool], skip_binning: typing.Optional[bool], skip_metabat2: typing.Optional[bool], skip_maxbin2: typing.Optional[bool], skip_concoct: typing.Optional[bool], bowtie2_mode: typing.Optional[str], save_assembly_mapped_reads: typing.Optional[bool], bin_domain_classification: typing.Optional[bool], skip_binqc: typing.Optional[bool], busco_db: typing.Optional[str], busco_auto_lineage_prok: typing.Optional[bool], save_busco_db: typing.Optional[bool], busco_clean: typing.Optional[bool], checkm_db: typing.Optional[str], save_checkm_data: typing.Optional[bool], refine_bins_dastool: typing.Optional[bool], run_gunc: typing.Optional[bool], gunc_db: typing.Optional[str], gunc_save_db: typing.Optional[bool], ancient_dna: typing.Optional[bool], skip_ancient_damagecorrection: typing.Optional[bool], spades_fix_cpus: typing.Optional[int], spadeshybrid_fix_cpus: typing.Optional[int], metabat_rng_seed: typing.Optional[int], clip_tool: typing.Optional[str], reads_minlength: typing.Optional[int], fastp_qualified_quality: typing.Optional[int], fastp_cut_mean_quality: typing.Optional[int], adapterremoval_minquality: typing.Optional[int], adapterremoval_adapter1: typing.Optional[str], adapterremoval_adapter2: typing.Optional[str], bbnorm_target: typing.Optional[int], bbnorm_min: typing.Optional[int], longreads_min_length: typing.Optional[int], longreads_keep_percent: typing.Optional[int], longreads_length_weight: typing.Optional[int], gtdb_db: typing.Optional[str], gtdbtk_min_completeness: typing.Optional[float], gtdbtk_max_contamination: typing.Optional[float], gtdbtk_min_perc_aa: typing.Optional[float], gtdbtk_min_af: typing.Optional[float], gtdbtk_pplacer_cpus: typing.Optional[float], gtdbtk_pplacer_scratch: typing.Optional[bool], genomad_min_score: typing.Optional[float], genomad_splits: typing.Optional[int], binning_map_mode: typing.Optional[str], min_contig_size: typing.Optional[int], min_length_unbinned_contigs: typing.Optional[int], max_unbinned_contigs: typing.Optional[int], tiara_min_length: typing.Optional[int], binqc_tool: typing.Optional[str], refine_bins_dastool_threshold: typing.Optional[float], postbinning_input: typing.Optional[str], gunc_database_type: typing.Optional[str], pydamage_accuracy: typing.Optional[float], freebayes_ploidy: typing.Optional[int], freebayes_min_basequality: typing.Optional[int], freebayes_minallelefreq: typing.Optional[float], bcftools_view_high_variant_quality: typing.Optional[int], bcftools_view_medium_variant_quality: typing.Optional[int], bcftools_view_minimal_allelesupport: typing.Optional[int]) -> None:
    try:
        shared_dir = Path("/nf-workdir")



        ignore_list = [
            "latch",
            ".latch",
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

        cmd = [
            "/root/nextflow",
            "run",
            str(shared_dir / "main.nf"),
            "-work-dir",
            str(shared_dir),
            "-profile",
            "docker",
            "-c",
            "latch.config",
                *get_flag('input', input),
                *get_flag('single_end', single_end),
                *get_flag('assembly_input', assembly_input),
                *get_flag('outdir', outdir),
                *get_flag('email', email),
                *get_flag('multiqc_title', multiqc_title),
                *get_flag('multiqc_methods_description', multiqc_methods_description),
                *get_flag('megahit_fix_cpu_1', megahit_fix_cpu_1),
                *get_flag('spades_fix_cpus', spades_fix_cpus),
                *get_flag('spadeshybrid_fix_cpus', spadeshybrid_fix_cpus),
                *get_flag('metabat_rng_seed', metabat_rng_seed),
                *get_flag('clip_tool', clip_tool),
                *get_flag('save_clipped_reads', save_clipped_reads),
                *get_flag('reads_minlength', reads_minlength),
                *get_flag('fastp_qualified_quality', fastp_qualified_quality),
                *get_flag('fastp_cut_mean_quality', fastp_cut_mean_quality),
                *get_flag('fastp_save_trimmed_fail', fastp_save_trimmed_fail),
                *get_flag('adapterremoval_minquality', adapterremoval_minquality),
                *get_flag('adapterremoval_trim_quality_stretch', adapterremoval_trim_quality_stretch),
                *get_flag('adapterremoval_adapter1', adapterremoval_adapter1),
                *get_flag('adapterremoval_adapter2', adapterremoval_adapter2),
                *get_flag('host_genome', host_genome),
                *get_flag('host_fasta', host_fasta),
                *get_flag('host_removal_verysensitive', host_removal_verysensitive),
                *get_flag('host_removal_save_ids', host_removal_save_ids),
                *get_flag('save_hostremoved_reads', save_hostremoved_reads),
                *get_flag('keep_phix', keep_phix),
                *get_flag('skip_clipping', skip_clipping),
                *get_flag('save_phixremoved_reads', save_phixremoved_reads),
                *get_flag('bbnorm', bbnorm),
                *get_flag('bbnorm_target', bbnorm_target),
                *get_flag('bbnorm_min', bbnorm_min),
                *get_flag('save_bbnorm_reads', save_bbnorm_reads),
                *get_flag('skip_adapter_trimming', skip_adapter_trimming),
                *get_flag('longreads_min_length', longreads_min_length),
                *get_flag('longreads_keep_percent', longreads_keep_percent),
                *get_flag('longreads_length_weight', longreads_length_weight),
                *get_flag('keep_lambda', keep_lambda),
                *get_flag('save_lambdaremoved_reads', save_lambdaremoved_reads),
                *get_flag('save_porechop_reads', save_porechop_reads),
                *get_flag('save_filtlong_reads', save_filtlong_reads),
                *get_flag('centrifuge_db', centrifuge_db),
                *get_flag('kraken2_db', kraken2_db),
                *get_flag('krona_db', krona_db),
                *get_flag('skip_krona', skip_krona),
                *get_flag('cat_db', cat_db),
                *get_flag('cat_db_generate', cat_db_generate),
                *get_flag('save_cat_db', save_cat_db),
                *get_flag('cat_official_taxonomy', cat_official_taxonomy),
                *get_flag('skip_gtdbtk', skip_gtdbtk),
                *get_flag('gtdb_db', gtdb_db),
                *get_flag('gtdb_mash', gtdb_mash),
                *get_flag('gtdbtk_min_completeness', gtdbtk_min_completeness),
                *get_flag('gtdbtk_max_contamination', gtdbtk_max_contamination),
                *get_flag('gtdbtk_min_perc_aa', gtdbtk_min_perc_aa),
                *get_flag('gtdbtk_min_af', gtdbtk_min_af),
                *get_flag('gtdbtk_pplacer_cpus', gtdbtk_pplacer_cpus),
                *get_flag('gtdbtk_pplacer_scratch', gtdbtk_pplacer_scratch),
                *get_flag('genomad_db', genomad_db),
                *get_flag('coassemble_group', coassemble_group),
                *get_flag('spades_options', spades_options),
                *get_flag('megahit_options', megahit_options),
                *get_flag('skip_spades', skip_spades),
                *get_flag('skip_spadeshybrid', skip_spadeshybrid),
                *get_flag('skip_megahit', skip_megahit),
                *get_flag('skip_quast', skip_quast),
                *get_flag('skip_prodigal', skip_prodigal),
                *get_flag('skip_prokka', skip_prokka),
                *get_flag('skip_metaeuk', skip_metaeuk),
                *get_flag('metaeuk_mmseqs_db', metaeuk_mmseqs_db),
                *get_flag('metaeuk_db', metaeuk_db),
                *get_flag('save_mmseqs_db', save_mmseqs_db),
                *get_flag('run_virus_identification', run_virus_identification),
                *get_flag('genomad_min_score', genomad_min_score),
                *get_flag('genomad_splits', genomad_splits),
                *get_flag('binning_map_mode', binning_map_mode),
                *get_flag('skip_binning', skip_binning),
                *get_flag('skip_metabat2', skip_metabat2),
                *get_flag('skip_maxbin2', skip_maxbin2),
                *get_flag('skip_concoct', skip_concoct),
                *get_flag('min_contig_size', min_contig_size),
                *get_flag('min_length_unbinned_contigs', min_length_unbinned_contigs),
                *get_flag('max_unbinned_contigs', max_unbinned_contigs),
                *get_flag('bowtie2_mode', bowtie2_mode),
                *get_flag('save_assembly_mapped_reads', save_assembly_mapped_reads),
                *get_flag('bin_domain_classification', bin_domain_classification),
                *get_flag('tiara_min_length', tiara_min_length),
                *get_flag('skip_binqc', skip_binqc),
                *get_flag('binqc_tool', binqc_tool),
                *get_flag('busco_db', busco_db),
                *get_flag('busco_auto_lineage_prok', busco_auto_lineage_prok),
                *get_flag('save_busco_db', save_busco_db),
                *get_flag('busco_clean', busco_clean),
                *get_flag('checkm_db', checkm_db),
                *get_flag('save_checkm_data', save_checkm_data),
                *get_flag('refine_bins_dastool', refine_bins_dastool),
                *get_flag('refine_bins_dastool_threshold', refine_bins_dastool_threshold),
                *get_flag('postbinning_input', postbinning_input),
                *get_flag('run_gunc', run_gunc),
                *get_flag('gunc_db', gunc_db),
                *get_flag('gunc_database_type', gunc_database_type),
                *get_flag('gunc_save_db', gunc_save_db),
                *get_flag('ancient_dna', ancient_dna),
                *get_flag('pydamage_accuracy', pydamage_accuracy),
                *get_flag('skip_ancient_damagecorrection', skip_ancient_damagecorrection),
                *get_flag('freebayes_ploidy', freebayes_ploidy),
                *get_flag('freebayes_min_basequality', freebayes_min_basequality),
                *get_flag('freebayes_minallelefreq', freebayes_minallelefreq),
                *get_flag('bcftools_view_high_variant_quality', bcftools_view_high_variant_quality),
                *get_flag('bcftools_view_medium_variant_quality', bcftools_view_medium_variant_quality),
                *get_flag('bcftools_view_minimal_allelesupport', bcftools_view_minimal_allelesupport)
        ]

        print("Launching Nextflow Runtime")
        print(' '.join(cmd))
        print(flush=True)

        env = {
            **os.environ,
            "NXF_HOME": "/root/.nextflow",
            "NXF_OPTS": "-Xms2048M -Xmx8G -XX:ActiveProcessorCount=4",
            "K8S_STORAGE_CLAIM_NAME": pvc_name,
            "NXF_DISABLE_CHECK_LATEST": "true",
        }
        subprocess.run(
            cmd,
            env=env,
            check=True,
            cwd=str(shared_dir),
        )
    finally:
        print()

        nextflow_log = shared_dir / ".nextflow.log"
        if nextflow_log.exists():
            name = _get_execution_name()
            if name is None:
                print("Skipping logs upload, failed to get execution name")
            else:
                remote = LPath(urljoins("latch:///your_log_dir/nf_nf_core_mag", name, "nextflow.log"))
                print(f"Uploading .nextflow.log to {remote.path}")
                remote.upload_from(nextflow_log)



@workflow(metadata._nextflow_metadata)
def nf_nf_core_mag(input: str, single_end: typing.Optional[bool], assembly_input: typing.Optional[str], outdir: typing_extensions.Annotated[LatchDir, FlyteAnnotation({'output': True})], email: typing.Optional[str], multiqc_title: typing.Optional[str], multiqc_methods_description: typing.Optional[str], megahit_fix_cpu_1: typing.Optional[bool], save_clipped_reads: typing.Optional[bool], fastp_save_trimmed_fail: typing.Optional[bool], adapterremoval_trim_quality_stretch: typing.Optional[bool], host_genome: typing.Optional[str], host_fasta: typing.Optional[str], host_removal_verysensitive: typing.Optional[bool], host_removal_save_ids: typing.Optional[bool], save_hostremoved_reads: typing.Optional[bool], keep_phix: typing.Optional[bool], skip_clipping: typing.Optional[bool], save_phixremoved_reads: typing.Optional[bool], bbnorm: typing.Optional[bool], save_bbnorm_reads: typing.Optional[bool], skip_adapter_trimming: typing.Optional[bool], keep_lambda: typing.Optional[bool], save_lambdaremoved_reads: typing.Optional[bool], save_porechop_reads: typing.Optional[bool], save_filtlong_reads: typing.Optional[bool], centrifuge_db: typing.Optional[LatchFile], kraken2_db: typing.Optional[LatchFile], krona_db: typing.Optional[str], skip_krona: typing.Optional[bool], cat_db: typing.Optional[str], cat_db_generate: typing.Optional[bool], save_cat_db: typing.Optional[bool], cat_official_taxonomy: typing.Optional[bool], skip_gtdbtk: typing.Optional[bool], gtdb_mash: typing.Optional[str], genomad_db: typing.Optional[str], coassemble_group: typing.Optional[bool], spades_options: typing.Optional[str], megahit_options: typing.Optional[str], skip_spades: typing.Optional[bool], skip_spadeshybrid: typing.Optional[bool], skip_megahit: typing.Optional[bool], skip_quast: typing.Optional[bool], skip_prodigal: typing.Optional[bool], skip_prokka: typing.Optional[bool], skip_metaeuk: typing.Optional[bool], metaeuk_mmseqs_db: typing.Optional[str], metaeuk_db: typing.Optional[str], save_mmseqs_db: typing.Optional[bool], run_virus_identification: typing.Optional[bool], skip_binning: typing.Optional[bool], skip_metabat2: typing.Optional[bool], skip_maxbin2: typing.Optional[bool], skip_concoct: typing.Optional[bool], bowtie2_mode: typing.Optional[str], save_assembly_mapped_reads: typing.Optional[bool], bin_domain_classification: typing.Optional[bool], skip_binqc: typing.Optional[bool], busco_db: typing.Optional[str], busco_auto_lineage_prok: typing.Optional[bool], save_busco_db: typing.Optional[bool], busco_clean: typing.Optional[bool], checkm_db: typing.Optional[str], save_checkm_data: typing.Optional[bool], refine_bins_dastool: typing.Optional[bool], run_gunc: typing.Optional[bool], gunc_db: typing.Optional[str], gunc_save_db: typing.Optional[bool], ancient_dna: typing.Optional[bool], skip_ancient_damagecorrection: typing.Optional[bool], spades_fix_cpus: typing.Optional[int] = -1, spadeshybrid_fix_cpus: typing.Optional[int] = -1, metabat_rng_seed: typing.Optional[int] = 1, clip_tool: typing.Optional[str] = 'fastp', reads_minlength: typing.Optional[int] = 15, fastp_qualified_quality: typing.Optional[int] = 15, fastp_cut_mean_quality: typing.Optional[int] = 15, adapterremoval_minquality: typing.Optional[int] = 2, adapterremoval_adapter1: typing.Optional[str] = 'AGATCGGAAGAGCACACGTCTGAACTCCAGTCACNNNNNNATCTCGTATGCCGTCTTCTGCTTG', adapterremoval_adapter2: typing.Optional[str] = 'AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT', bbnorm_target: typing.Optional[int] = 100, bbnorm_min: typing.Optional[int] = 5, longreads_min_length: typing.Optional[int] = 1000, longreads_keep_percent: typing.Optional[int] = 90, longreads_length_weight: typing.Optional[int] = 10, gtdb_db: typing.Optional[str] = 'https://data.ace.uq.edu.au/public/gtdb/data/releases/release214/214.1/auxillary_files/gtdbtk_r214_data.tar.gz', gtdbtk_min_completeness: typing.Optional[float] = 50, gtdbtk_max_contamination: typing.Optional[float] = 10, gtdbtk_min_perc_aa: typing.Optional[float] = 10, gtdbtk_min_af: typing.Optional[float] = 0.65, gtdbtk_pplacer_cpus: typing.Optional[float] = 1, gtdbtk_pplacer_scratch: typing.Optional[bool] = True, genomad_min_score: typing.Optional[float] = 0.7, genomad_splits: typing.Optional[int] = 1, binning_map_mode: typing.Optional[str] = 'group', min_contig_size: typing.Optional[int] = 1500, min_length_unbinned_contigs: typing.Optional[int] = 1000000, max_unbinned_contigs: typing.Optional[int] = 100, tiara_min_length: typing.Optional[int] = 3000, binqc_tool: typing.Optional[str] = 'busco', refine_bins_dastool_threshold: typing.Optional[float] = 0.5, postbinning_input: typing.Optional[str] = 'raw_bins_only', gunc_database_type: typing.Optional[str] = 'progenomes', pydamage_accuracy: typing.Optional[float] = 0.5, freebayes_ploidy: typing.Optional[int] = 1, freebayes_min_basequality: typing.Optional[int] = 20, freebayes_minallelefreq: typing.Optional[float] = 0.33, bcftools_view_high_variant_quality: typing.Optional[int] = 30, bcftools_view_medium_variant_quality: typing.Optional[int] = 20, bcftools_view_minimal_allelesupport: typing.Optional[int] = 3) -> None:
    """
    nf-core/mag

    Sample Description
    """

    pvc_name: str = initialize()
    nextflow_runtime(pvc_name=pvc_name, input=input, single_end=single_end, assembly_input=assembly_input, outdir=outdir, email=email, multiqc_title=multiqc_title, multiqc_methods_description=multiqc_methods_description, megahit_fix_cpu_1=megahit_fix_cpu_1, spades_fix_cpus=spades_fix_cpus, spadeshybrid_fix_cpus=spadeshybrid_fix_cpus, metabat_rng_seed=metabat_rng_seed, clip_tool=clip_tool, save_clipped_reads=save_clipped_reads, reads_minlength=reads_minlength, fastp_qualified_quality=fastp_qualified_quality, fastp_cut_mean_quality=fastp_cut_mean_quality, fastp_save_trimmed_fail=fastp_save_trimmed_fail, adapterremoval_minquality=adapterremoval_minquality, adapterremoval_trim_quality_stretch=adapterremoval_trim_quality_stretch, adapterremoval_adapter1=adapterremoval_adapter1, adapterremoval_adapter2=adapterremoval_adapter2, host_genome=host_genome, host_fasta=host_fasta, host_removal_verysensitive=host_removal_verysensitive, host_removal_save_ids=host_removal_save_ids, save_hostremoved_reads=save_hostremoved_reads, keep_phix=keep_phix, skip_clipping=skip_clipping, save_phixremoved_reads=save_phixremoved_reads, bbnorm=bbnorm, bbnorm_target=bbnorm_target, bbnorm_min=bbnorm_min, save_bbnorm_reads=save_bbnorm_reads, skip_adapter_trimming=skip_adapter_trimming, longreads_min_length=longreads_min_length, longreads_keep_percent=longreads_keep_percent, longreads_length_weight=longreads_length_weight, keep_lambda=keep_lambda, save_lambdaremoved_reads=save_lambdaremoved_reads, save_porechop_reads=save_porechop_reads, save_filtlong_reads=save_filtlong_reads, centrifuge_db=centrifuge_db, kraken2_db=kraken2_db, krona_db=krona_db, skip_krona=skip_krona, cat_db=cat_db, cat_db_generate=cat_db_generate, save_cat_db=save_cat_db, cat_official_taxonomy=cat_official_taxonomy, skip_gtdbtk=skip_gtdbtk, gtdb_db=gtdb_db, gtdb_mash=gtdb_mash, gtdbtk_min_completeness=gtdbtk_min_completeness, gtdbtk_max_contamination=gtdbtk_max_contamination, gtdbtk_min_perc_aa=gtdbtk_min_perc_aa, gtdbtk_min_af=gtdbtk_min_af, gtdbtk_pplacer_cpus=gtdbtk_pplacer_cpus, gtdbtk_pplacer_scratch=gtdbtk_pplacer_scratch, genomad_db=genomad_db, coassemble_group=coassemble_group, spades_options=spades_options, megahit_options=megahit_options, skip_spades=skip_spades, skip_spadeshybrid=skip_spadeshybrid, skip_megahit=skip_megahit, skip_quast=skip_quast, skip_prodigal=skip_prodigal, skip_prokka=skip_prokka, skip_metaeuk=skip_metaeuk, metaeuk_mmseqs_db=metaeuk_mmseqs_db, metaeuk_db=metaeuk_db, save_mmseqs_db=save_mmseqs_db, run_virus_identification=run_virus_identification, genomad_min_score=genomad_min_score, genomad_splits=genomad_splits, binning_map_mode=binning_map_mode, skip_binning=skip_binning, skip_metabat2=skip_metabat2, skip_maxbin2=skip_maxbin2, skip_concoct=skip_concoct, min_contig_size=min_contig_size, min_length_unbinned_contigs=min_length_unbinned_contigs, max_unbinned_contigs=max_unbinned_contigs, bowtie2_mode=bowtie2_mode, save_assembly_mapped_reads=save_assembly_mapped_reads, bin_domain_classification=bin_domain_classification, tiara_min_length=tiara_min_length, skip_binqc=skip_binqc, binqc_tool=binqc_tool, busco_db=busco_db, busco_auto_lineage_prok=busco_auto_lineage_prok, save_busco_db=save_busco_db, busco_clean=busco_clean, checkm_db=checkm_db, save_checkm_data=save_checkm_data, refine_bins_dastool=refine_bins_dastool, refine_bins_dastool_threshold=refine_bins_dastool_threshold, postbinning_input=postbinning_input, run_gunc=run_gunc, gunc_db=gunc_db, gunc_database_type=gunc_database_type, gunc_save_db=gunc_save_db, ancient_dna=ancient_dna, pydamage_accuracy=pydamage_accuracy, skip_ancient_damagecorrection=skip_ancient_damagecorrection, freebayes_ploidy=freebayes_ploidy, freebayes_min_basequality=freebayes_min_basequality, freebayes_minallelefreq=freebayes_minallelefreq, bcftools_view_high_variant_quality=bcftools_view_high_variant_quality, bcftools_view_medium_variant_quality=bcftools_view_medium_variant_quality, bcftools_view_minimal_allelesupport=bcftools_view_minimal_allelesupport)

