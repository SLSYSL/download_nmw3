import winreg
from pathlib import Path
from add_to_steam import add_to_steam
from gofile_downloader import Manager

steam_path = None


def set_steam_path(path_str):
    global steam_path
    steam_path = Path(path_str)


def get_steam_path() -> bool:
    global steam_path
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam"
        )
        path, _ = winreg.QueryValueEx(key, "InstallPath")
        winreg.CloseKey(key)
        steam_path = Path(path)
        return True
    except Exception:
        return False


def main():
    if not get_steam_path():
        print("自动获取 Steam 路径失败，请手动设置")

    while True:
        print("1: 伪入库 COD20 (NMW3)")
        print("2: 下载战区文件")
        print("3: 设置Steam路径 (获取失败时使用)")
        choice = input("请选择操作: ").strip()
        if choice == "1":
            add_to_steam(steam_path)
        elif choice == "2":
            path = input("请输入战区文件安装路径 (留空则默认exe目录): ")
            mgr = Manager("https://gofile.io/d/NzOvvy", None, root_dir=path or None)
            mgr.run()
        elif choice == "3":
            path = input("请输入 Steam 安装路径（如 C:\\Steam）: ").strip()
            set_steam_path(path)
            print(f"已设置路径: {steam_path}")
        else:
            print("无效操作")

if __name__ == "__main__":
    main()
