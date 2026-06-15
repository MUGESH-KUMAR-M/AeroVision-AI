"""
Download NEU-DET dataset for AeroVision AI training.
Source: https://github.com/Marfbin/NEU-DET-with-yolov8
"""

import shutil
import subprocess
import sys
from pathlib import Path

REPO_URL = "https://github.com/Marfbin/NEU-DET-with-yolov8.git"
TEMP_DIR = Path("_temp_neu_det_repo")
TARGET_DIR = Path("NEU-DET")


def run(cmd, cwd=None):
    print(f"> {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}")


def download_with_git_sparse():
    if TARGET_DIR.exists() and any(TARGET_DIR.rglob("*.jpg")):
        print(f"Dataset already present at {TARGET_DIR.resolve()}")
        return True

    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)

    run(["git", "clone", "--filter=blob:none", "--sparse", REPO_URL, str(TEMP_DIR)])
    run(["git", "sparse-checkout", "set", "data/NEU-DET"], cwd=TEMP_DIR)

    source = TEMP_DIR / "data" / "NEU-DET"
    if not source.exists():
        print("Sparse checkout did not find data/NEU-DET")
        return False

    if TARGET_DIR.exists():
        shutil.rmtree(TARGET_DIR)

    shutil.copytree(source, TARGET_DIR)
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    return True


def verify_dataset():
    required = [
        TARGET_DIR / "train" / "images",
        TARGET_DIR / "test" / "images",
    ]
    for path in required:
        if not path.exists():
            return False, f"Missing folder: {path}"

    image_count = len(list(TARGET_DIR.rglob("*.jpg")))
    if image_count < 100:
        return False, f"Too few images found ({image_count}). Download may be incomplete."

    return True, f"OK - {image_count} images in {TARGET_DIR.resolve()}"


def main():
    print("=" * 60)
    print("  AeroVision AI - NEU-DET Dataset Download")
    print("=" * 60)

    try:
        ok = download_with_git_sparse()
    except Exception as exc:
        print(f"\nAutomatic download failed: {exc}")
        print("\nManual download:")
        print("  1. git clone https://github.com/Marfbin/NEU-DET-with-yolov8.git")
        print("  2. Copy data/NEU-DET folder to ./NEU-DET/")
        print("  Or Baidu: https://pan.baidu.com/s/1K-mTgSJfhFrcVSO8MUqHbQ?pwd=6666")
        sys.exit(1)

    if not ok:
        sys.exit(1)

    valid, message = verify_dataset()
    print(message)
    if not valid:
        sys.exit(1)

    print("\nDataset ready. Next step:")
    print("  python train.py")


if __name__ == "__main__":
    main()
