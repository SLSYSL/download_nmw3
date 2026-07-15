import shutil
import psutil
import subprocess
import sys
from pathlib import Path

def get_resource_path(relative_path) -> Path:
    base = Path(sys._MEIPASS) if getattr(sys, "frozen", False) else Path(__file__).parent
    return base / relative_path

def close_steam():
    try:
        for p in psutil.process_iter(["name"]):
            if "steam" in p.info["name"].lower():
                p.terminate()
                print(f"已关闭 {p.info['name']} (PID: {p.pid})")
        return None
    except Exception as e:
        return str(e)

def move_files(target_dir, file_pairs):
    errors = []
    for src_rel, dst_rel in file_pairs:
        dst = target_dir / dst_rel
        if dst.exists():
            print(f"已存在，跳过: {dst_rel}")
            continue
        src = get_resource_path(src_rel)
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            shutil.copy2(src, dst)
            print(f"已复制: {src_rel} -> {dst}")
        except Exception as e:
            errors.append(f"{dst_rel}: {e}")
    if errors:
        return "复制失败:\n" + "\n".join(errors)
    return None

def start_steam(steam_path):
    steam_exe = steam_path / "steam.exe"
    if steam_exe.exists():
        subprocess.Popen([str(steam_exe)], shell=True)
        print("已启动 Steam")
        return None
    else:
        return f"{steam_exe} 不存在，请手动启动"

def add_to_steam(steam_path):
    if steam_path is None:
        print("Steam路径未设置")
        return

    err = close_steam()
    if err:
        print(f"关闭 Steam 失败: {err}，请手动关闭后重试。")
        return

    file_pairs = [
        ("assets/OpenSteamTool.dll", "OpenSteamTool.dll"),
        ("assets/dwmapi.dll", "dwmapi.dll"),
        ("assets/3595270.lua", "config/lua/3595270.lua"),
    ]
    err = move_files(steam_path, file_pairs)
    if err:
        print(err)
        return

    err = start_steam(steam_path)
    if err:
        print(err)
    else:
        print("伪入库 COD20 (NMW3) 已完成")