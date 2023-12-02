# coding: latin-1

import sys
from pathlib import Path
import logging
import configparser

import shutil
from PIL import Image

project_root = Path(__file__).parent

posdata = dict(
    pos0=dict(
        search_string=b"\xC7\x44\x24\x4C\x20\x03\x00\x00\xC7\x44\x24\x50\x58\x02\x00\x00\xEB\x2A\x3C\x01\x75\x12\xC7\x44\x24\x4C",
        x1=0,
        y1=8,
        x2=0x16,
        y2=0x1E,
    ),
    pos1=dict(
        search_string=b"\xC7\x44\x24\x18\x20\x03\x00\x00\xC7\x44\x24\x1C\x58\x02\x00\x00\xEB\x2C\x83\xFE\x01\x75\x12\xC7\x44\x24\x18",
        x1=0,
        y1=8,
        x2=0x17,
        y2=0x1F,
    ),
    pos2=dict(
        search_string=b"\xC7\x44\x24\x3C\x20\x03\x00\x00\xC7\x44\x24\x40\x58\x02\x00\x00\xEB\x22\xC7\x44\x24\x3C",
        x1=0x12,
        y1=0x1A,
        x2=0,
        y2=8,
    ),
    pos3=dict(
        search_string=b"\xC7\x44\x24\x48\x20\x03\x00\x00\xC7\x44\x24\x4C\x58\x02\x00\x00\xEB\x2B\x83\xF8\x01\x75\x12\xC7\x44\x24\x48",
        x1=0,
        y1=8,
        x2=0x16,
        y2=0x1E,
    ),
    pos4=dict(
        search_string=b"\xC7\x44\x24\x24\x20\x03\x00\x00\xC7\x44\x24\x28\x58\x02\x00\x00\xEB\x2C\x83\xF8\x01\x75\x12\xC7\x44\x24\x24",
        x1=0,
        y1=8,
        x2=0x17,
        y2=0x1F,
    ),
    more0=dict(
        search_string=b"\xE8\xFB\xB0\x08\x00\x8B\x0D\xA4\xB0\x6C\x00\xE8\x90\x76\xFD\xFF\xA1\x80\xB2\x6D\x00\x3D\x20\x03\x00\x00\x0F\x84\x62\x01\x00\x00\x3D",
        x1=0,
        y1=-1,
        x2=0xB,
        y2=-1,
    ),
    more1=dict(
        search_string=b"\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\x90\xA1\x80\xB2\x6D\x00\x83\xEC\x1C\x3D\x20\x03\x00\x00\x53\x55\x56\x57\x8B\xF1\x74\x3C\x3D",
        x1=0,
        y1=-1,
        x2=7,
        y2=-1,
    ),
)


def read_resolution(path_to_patrizier_exe: Path) -> (int, int):
    with open(path_to_patrizier_exe, "r+b") as file:
        data: bytes = file.read()
        for key, value in posdata.items():
            if "pos" in key:
                count = data.count(value["search_string"])
                if count != 1:
                    raise ValueError(f"Did not find {key}")

                # find position after search string
                spos = data.find(value["search_string"]) + len(value["search_string"])

                for resolution_index in range(1, 3):
                    x_res = int.from_bytes(
                        data[spos + value[f"x{resolution_index}"] :][:2],
                        byteorder="little",
                    )
                    y_res = int.from_bytes(
                        data[spos + value[f"y{resolution_index}"] :][:2],
                        byteorder="little",
                    )
                    logging.info(
                        f"{key} resolution {resolution_index}: {x_res}x{y_res}"
                    )
            elif "more" in key:
                count = data.count(value["search_string"])
                if count != 1:
                    raise ValueError(f"Did not find {key}")


def change_resolution(
    path_to_patrizier_exe: Path, width: int = 1024, height: int = 768
):
    width_small = 1024
    height_small = 768
    backup_file = path_to_patrizier_exe.with_suffix(".bak")
    if backup_file.exists():
        logging.warning(f"Keeping existing backup file: {backup_file}")
    else:
        logging.info(f"Backing up {path_to_patrizier_exe}")
        shutil.copy(path_to_patrizier_exe, backup_file)

    game_root_directory = path_to_patrizier_exe.parent

    # patch new resolution into Patrizier II.exe
    with open(path_to_patrizier_exe, "r+b") as file:
        data: bytes = file.read()

        for key, value in posdata.items():
            if "pos" in key:
                # write resolution
                spos = data.index(value["search_string"]) + len(value["search_string"])
                file.seek(spos + value["x1"])
                file.write(int(width_small).to_bytes(length=2, byteorder="little"))
                file.seek(spos + value["y1"])
                file.write(int(height_small).to_bytes(length=2, byteorder="little"))
                spos = data.index(value["search_string"]) + len(value["search_string"])
                file.seek(spos + value["x2"])
                file.write(int(width).to_bytes(length=2, byteorder="little"))
                file.seek(spos + value["y2"])
                file.write(int(height).to_bytes(length=2, byteorder="little"))

            if width >= 1280 and "more" in key:
                spos = data.index(value["search_string"]) + len(value["search_string"])
                file.seek(spos + value["x2"])
                file.write(int(width).to_bytes(length=2, byteorder="little"))

    logging.info("Resize pictures for res >=1280")

    images_directory = game_root_directory / "images"
    if not images_directory.is_dir():
        logging.info(f"Creating non existing directory {images_directory}")
        images_directory.mkdir()

    data_directory = project_root / "data"

    if1 = Image.open(data_directory / "Vollansichtskarte.bmp")
    if1n = if1.resize((width, height))
    if1n.save(game_root_directory / "images" / "Vollansichtskarte1280.bmp")
    if2 = Image.open(data_directory / "HauptscreenE.bmp")
    if2n = if2.resize((284, 424 - 1024 + height))
    if2n.save(game_root_directory / "images" / "HauptscreenE1280.bmp")

    scripts_dir = game_root_directory / "scripts"
    if not scripts_dir.is_dir():
        logging.info(f"Creating non existing directory {scripts_dir}")
        scripts_dir.mkdir()

    def patch_script_file(filename: str, patches: list):
        config = configparser.ConfigParser()

        config.read(data_directory / filename, encoding="LATIN1")

        for patch in patches:
            config[patch["section"]][patch["key"]] = patch["value"]

        with open(scripts_dir / filename, "w", encoding="LATIN1") as file:
            config.write(file)

    patch_script_file(
        "screenGame.ini",
        [
            # patch resolution 1
            #dict(
            #    section="ANIM41",
            #    key="Frame0",
            #    value="10 0 0 0 0 " + str(width_small - 284) + " 42 0",
            #),
            #dict(
            #    section="ANIM43",
            #    key="Frame0",
            #    value="8 0 0 0 0 284 " + str(284 + (height_small - 768)),
            #),
            #dict(section="ANIM43", key="Pos", value=str(width_small - 284) + " 600"),
            # patch resolution 2
            dict(section="ANIM42", key="Frame0", value=f"11 0 0 0 0 {width - 284} 42"),
            dict(
                section="ANIM44",
                key="Frame0",
                value=f"9 0 0 0 0 284 {424 + (height - 1024)}",
            ),
            dict(section="ANIM44", key="Pos", value=f"{width - 284} 600"),
        ],
    )

    patch_script_file(
        "accelMap.ini",
        [
            # patch resolution 1
            dict(section="SCREEN1", key="Size", value=f"{width_small} {height_small}"),
            #dict(
            #    section="ANIM1",
            #    key="Frame0",
            #    value=f"30023 0 0 0 0 {width_small} {height_small} 0",
            #),
            # patch resolution 2
            dict(section="SCREEN2", key="Size", value=f"{width} {height}"),
            dict(
                section="ANIM2", key="Frame0", value=f"30024 0 0 0 0 {width} {height} 0"
            ),
        ],
    )

    patch_script_file(
        "textures.ini",
        [
            # patch resolution 1
            #dict(
            #    section="TEX30023",
            #    key="OffsetNSize0",
            #    value=f"0 0 {width_small} {height_small}",
            #),
            # path resolution 2
            dict(section="TEX30024", key="OffsetNSize0", value=f"0 0 {width} {height}"),
        ],
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    if len(sys.argv) == 2:
        read_resolution(Path(sys.argv[1]))
    elif len(sys.argv) == 4:
        change_resolution(Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
