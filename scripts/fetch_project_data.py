"""Fetch public BWM tables or selected ONE datasets; no scientific analyses are run."""

# This must precede imports of requests, ONE, boto3, or other networking libraries.
import os

for _key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY", "http_proxy", "https_proxy", "all_proxy"):
    os.environ.pop(_key, None)
os.environ["NO_PROXY"] = os.environ["no_proxy"] = "*"

import argparse
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
from pathlib import Path
import sys

import requests

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOT = "https://ibl-brain-wide-map-public.s3.amazonaws.com/aggregates"
# Expected MD5s are the release checksums recorded in brainwidemap/bwm_loading.py.
RELEASES = {
    "2024": ("2024_Q2_IBL_et_al_BWM", {
        "trials": (".pqt", "067fb0e3d242ebeface361c42bdcf8c8"),
        "clusters": (".pqt", "b89fac76289f3a3d585910711f1eef41"),
    }),
    "2026": ("2026_Q2_IBL_et_al_BWM", {
        "clusters": (".pqt", "ac22196fbd77687d6ee3a0c6b1b1fc15"),
        "clusters.waveforms_peak": (".npy", "db71666e84ae28b6a9051e3fa866d1c9"),
        "clusters.acgs_log": (".npy", "7f1cc617d97b234b307ca9ff16cbf09f"),
        "acgs_log.times": (".npy", "c331a024cedb4ffa30304dc40af5a703"),
    }),
}
PROFILES = {
    "trials": ("*trials*",),
    "wheel": ("*wheel.*", "*wheelMoves.*"),
    "pose": ("*Camera.dlc.*", "*Camera.lightningPose.*", "*Camera.ROIMotionEnergy.*",
             "*Camera.times.*", "*Camera.features.*"),
    "passive": ("*passivePeriods*", "*passiveGabor*", "*passiveStims*", "*passiveRFM.times*"),
    "widefield": ("*widefieldU.*", "*widefieldSVT.haemoCorrected.*", "*widefieldLandmarks.*",
                  "*imaging.times.*", "*imaging.imagingLightSource.*", "*imagingLightSource.*"),
}
EXAMPLE_EID = "15f742e1-1043-45c9-9504-f1e8a53c1744"
EXAMPLE_PID = "3675290c-8134-4598-b924-83edb7940269"


def md5(path):
    digest = hashlib.md5()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(path, records, **context):
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"checked_utc": datetime.now(timezone.utc).isoformat(), **context, "files": records}
    path.write_text(json.dumps(record, indent=2) + "\n")
    print(f"Manifest: {path}", flush=True)


def fetch_file(url, target, expected_md5):
    """Keep a valid cached file, or atomically replace it after a verified download."""
    if target.exists() and md5(target) == expected_md5:
        print(f"Cached and verified: {target.name}", flush=True)
        return "cached"
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + ".part")
    digest = hashlib.md5()
    received = 0
    try:
        with requests.get(url, stream=True, timeout=(15, 90)) as response:
            response.raise_for_status()
            expected_size = response.headers.get("Content-Length")
            with partial.open("wb") as stream:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    if chunk:
                        stream.write(chunk)
                        digest.update(chunk)
                        received += len(chunk)
        if expected_size is not None and received != int(expected_size):
            raise ValueError(f"Incomplete download: {target.name}, {received}/{expected_size} bytes")
        if digest.hexdigest() != expected_md5:
            raise ValueError(
                f"Checksum mismatch for {target.name}: expected {expected_md5}, got {digest.hexdigest()}. "
                "The remote release may have changed; the existing file was not replaced."
            )
        partial.replace(target)
    finally:
        partial.unlink(missing_ok=True)
    print(f"Downloaded and verified: {target} ({received:,} bytes)", flush=True)
    return "downloaded"


def tables(args):
    tag, known = RELEASES[args.release]
    names = args.files or list(known)
    unknown = set(names) - set(known)
    if unknown:
        raise ValueError(f"Files not defined for {tag}: {', '.join(sorted(unknown))}")
    target_dir = args.cache_dir / "aggregates" / tag
    records = []
    for name in dict.fromkeys(names):
        extension, checksum = known[name]
        filename = name + extension
        url = f"{PUBLIC_ROOT}/{tag}/{filename}"
        with requests.head(url, timeout=(15, 30)) as response:
            response.raise_for_status()
            size = response.headers.get("Content-Length")
            size = int(size) if size is not None else None
        print(f"Online: {tag}/{filename}; bytes={size:,}" if size is not None else f"Online: {url}", flush=True)
        target = target_dir / filename
        status = "online_only" if args.check_only else fetch_file(url, target, checksum)
        records.append({"name": filename, "url": url, "bytes": size, "expected_md5": checksum,
                        "path": str(target), "status": status})
        write_manifest(target_dir / ("availability.json" if args.check_only else "download_manifest.json"),
                       records, release=tag, check_only=args.check_only)


def connect(args):
    from one.api import ONE

    token = os.environ.get("BWM_ONE_TOKEN")
    if token:
        auth = {"token": token}
    else:
        username = os.environ.get("BWM_ONE_USERNAME", "intbrainlab")
        password = os.environ.get("BWM_ONE_PASSWORD")
        if username != "intbrainlab" and not password:
            raise ValueError("Set BWM_ONE_PASSWORD for your username, or use BWM_ONE_TOKEN.")
        auth = {"username": username, "password": password or "international"}
    return ONE(base_url="https://openalyx.internationalbrainlab.org", silent=True,
               cache_dir=Path(os.environ.get("BWM_CACHE_DIR", args.cache_dir / "one")).expanduser(), **auth)


def session(args):
    import pandas as pd
    from one.util import filter_revision_last_before

    one = connect(args)
    datasets = one.list_datasets(args.eid, details=True, query_type="remote", default_revisions_only=True)
    patterns = args.include or PROFILES[args.profile]
    selected = datasets.loc[datasets.rel_path.map(
        lambda path: any(fnmatch.fnmatch(path if "/" in pattern else Path(path).name, pattern)
                         for pattern in patterns))]
    if "exists" in selected:
        selected = selected.loc[selected["exists"]]
    if selected.empty:
        raise ValueError(f"No online datasets match {patterns} for session {args.eid}; try --list-only with --include '*'.")
    # Remote list_datasets ignores default_revisions_only in some ONE versions.
    # Use ONE's own per-dataset revision selection before downloading exact paths.
    selected = filter_revision_last_before(selected.copy(), assert_unique=False)
    records = []
    for _, row in selected.iterrows():
        rel_path = row.rel_path
        print(f"{'Available' if args.list_only else 'Fetching'}: {rel_path}", flush=True)
        path = None if args.list_only else one.load_dataset(args.eid, rel_path, download_only=True, query_type="remote")
        if not args.list_only and path is None:
            raise RuntimeError(f"ONE did not download {rel_path}")
        records.append({"rel_path": rel_path, "dataset_id": str(row.name),
                        "bytes": int(row.file_size) if pd.notna(row.get("file_size")) else None,
                        "path": str(path) if path else None, "status": "online_only" if args.list_only else "downloaded_or_cached"})
    manifest = args.cache_dir / "manifests" / f"{args.eid}_{args.profile}_{'availability' if args.list_only else 'download'}.json"
    write_manifest(manifest, records, eid=args.eid, profile=args.profile, patterns=list(patterns))


def find_sessions(args):
    from brainwidemap import bwm_query

    one = connect(args)
    sessions = one.search(datasets=args.dataset, query_type="remote")
    frozen = set(bwm_query().eid)
    records = [{"eid": str(eid), "in_frozen_bwm_cohort": str(eid) in frozen} for eid in sessions]
    if args.bwm_only:
        records = [r for r in records if r["in_frozen_bwm_cohort"]]
    print(f"Found {len(records)} sessions matching {args.dataset}", flush=True)
    for record in records[:args.limit]:
        print(f"{record['eid']}  frozen_BWM={record['in_frozen_bwm_cohort']}", flush=True)
    # A search match is not a guarantee of camera/analysis QC eligibility.
    safe_name = "".join(c if c.isalnum() else "_" for c in args.dataset)
    write_manifest(args.cache_dir / "manifests" / f"search_{safe_name}.json", records,
                   dataset=args.dataset, bwm_only=args.bwm_only)


def probe(args):
    from brainwidemap import bwm_query, load_good_units
    from brainbox.io.one import SessionLoader
    from brainwidemap.bwm_loading import MODIFIED_BEFORE

    row = bwm_query().loc[lambda frame: frame.pid == args.pid]
    if len(row) != 1:
        raise ValueError("The probe must occur in the frozen BWM cohort.")
    row = row.iloc[0]
    one = connect(args)
    spikes, clusters = load_good_units(one, row.pid, eid=row.eid, pname=row.probe_name)
    loader = SessionLoader(one=one, eid=row.eid, revision=MODIFIED_BEFORE)
    loader.load_trials()
    write_manifest(args.cache_dir / "manifests" / f"{args.pid}_probe.json", [],
                   pid=row.pid, eid=row.eid, probe=row.probe_name, good_units=len(clusters),
                   spikes=len(spikes["times"]), trials=len(loader.trials),
                   spike_sorting_revision="2024-05-06", trial_revision=MODIFIED_BEFORE,
                   cache_dir=str(one.cache_dir))
    print("Processed good-unit spikes and trials are cached; no statistical analysis was run.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=ROOT / "data")
    sub = parser.add_subparsers(dest="command", required=True)
    table_parser = sub.add_parser("tables", help="Anonymous public S3 aggregate download; default ~110 MiB")
    table_parser.add_argument("--release", choices=RELEASES, default="2024")
    table_parser.add_argument("--files", nargs="+", help="Logical names, e.g. clusters or acgs_log.times")
    table_parser.add_argument("--check-only", action="store_true", help="HEAD requests only; no dataset contents")
    table_parser.set_defaults(run=tables)
    session_parser = sub.add_parser("session", help="List or download a selected modality via ONE")
    session_parser.add_argument("--eid", default=EXAMPLE_EID)
    session_parser.add_argument("--profile", choices=PROFILES, default="trials")
    session_parser.add_argument("--include", action="append", help="Override filename glob; repeatable; quote wildcards")
    session_parser.add_argument("--list-only", action="store_true", help="Only list remote metadata")
    session_parser.set_defaults(run=session)
    search_parser = sub.add_parser("find", help="Find session IDs with a named dataset; metadata only")
    search_parser.add_argument("--dataset", required=True, help="Exact filename including namespace, e.g. _ibl_passiveGabor.table.csv")
    search_parser.add_argument("--bwm-only", action="store_true", help="Restrict to the frozen electrophysiology cohort")
    search_parser.add_argument("--limit", type=int, default=5, help="Maximum session IDs to print; manifest retains all")
    search_parser.set_defaults(run=find_sessions)
    probe_parser = sub.add_parser("probe", help="Cache processed good-unit spikes and trials for one frozen probe")
    probe_parser.add_argument("--pid", default=EXAMPLE_PID)
    probe_parser.set_defaults(run=probe)
    args = parser.parse_args()
    args.cache_dir = args.cache_dir.expanduser().resolve()
    try:
        args.run(args)
    except (requests.RequestException, ValueError, RuntimeError) as error:
        print(f"Fetch failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
