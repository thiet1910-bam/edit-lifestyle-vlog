#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TỰ ĐỘNG ĐỒNG BỘ 2 CHIỀU VỚI GITHUB (AUTO-SYNC ENGINE)
- Tự động kéo bản mới nhất từ GitHub (git pull --rebase) để tránh xung đột giữa các máy.
- Tự động phát hiện thay đổi (git status --porcelain), đóng gói commit và đẩy thẳng lên GitHub (git push origin main).
"""
import subprocess, sys, datetime
from pathlib import Path

def sync_to_github(commit_msg: str = ""):
    # Xác định thư mục gốc chứa .git
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[4] if script_path.parents[3].name == ".agent" else Path.cwd()
    if not (repo_root / ".git").exists():
        # Thử tìm từ thư mục hiện tại đi lên
        cur = Path.cwd().resolve()
        for p in [cur] + list(cur.parents):
            if (p / ".git").exists():
                repo_root = p
                break

    if not (repo_root / ".git").exists():
        print("[Auto-Sync] Không tìm thấy kho .git tại:", repo_root)
        return False

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not commit_msg:
        commit_msg = f"chore(auto-sync): cập nhật tự động lúc {now_str}"

    try:
        # 1. Kiểm tra thay đổi tại máy local
        st = subprocess.run(["git", "status", "--porcelain"], cwd=str(repo_root), capture_output=True, text=True)
        has_changes = bool(st.stdout.strip())

        if has_changes:
            subprocess.run(["git", "add", "-A"], cwd=str(repo_root), check=False)
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=str(repo_root), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 2. Kéo thay đổi từ remote (nếu có máy khác vừa đẩy lên) rồi đẩy bản mới nhất lên GitHub
        subprocess.run(["git", "pull", "--rebase", "origin", "main"], cwd=str(repo_root), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        push_res = subprocess.run(["git", "push", "origin", "main"], cwd=str(repo_root), capture_output=True, text=True)
        if push_res.returncode == 0:
            print(f"[Auto-Sync GitHub ✅] Đã tự động đồng bộ lên https://github.com/thiet1910-bam/edit-lifestyle-vlog ({now_str})")
            return True
        else:
            print(f"[Auto-Sync GitHub ⚠️] Lỗi khi push: {push_res.stderr.strip()}")
            return False
    except Exception as e:
        print(f"[Auto-Sync GitHub ⚠️] Ngoại lệ: {e}")
        return False

if __name__ == "__main__":
    msg = " ".join(sys.argv[1:]).strip()
    sync_to_github(msg)
