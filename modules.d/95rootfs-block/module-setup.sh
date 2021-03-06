#!/bin/bash
# -*- mode: shell-script; indent-tabs-mode: nil; sh-basic-offset: 4; -*-
# ex: ts=8 sw=4 sts=4 et filetype=sh

check() {
    return 0
}

depends() {
    echo fs-lib
}

cmdline() {
    local dev=/dev/block/$(find_root_block_device)
    if [ -e $dev ]; then
        printf " root=%s" "$(shorten_persistent_dev "$(get_persistent_dev "$dev")")"
        printf " rootflags=%s" "$(find_mp_fsopts /)"
        printf " rootfstype=%s" "$(find_mp_fstype /)"
    fi
}

install() {

    if [[ $hostonly ]]; then
        for dev in "${!host_fs_types[@]}"; do
            [[ ${host_fs_types[$dev]} = "reiserfs" ]] || [[ ${host_fs_types[$dev]} = "xfs" ]] || continue
            rootopts=$(find_dev_fsopts "$dev")
            if [[ ${host_fs_types[$dev]} = "reiserfs" ]]; then
                journaldev=$(fs_get_option $rootopts "jdev")
            elif [[ ${host_fs_types[$dev]} = "xfs" ]]; then
                journaldev=$(fs_get_option $rootopts "logdev")
            fi

            if [ -n "$journaldev" ]; then
                printf "%s\n" "root.journaldev=$journaldev" >> "${initdir}/etc/cmdline.d/95root-journaldev.conf"
            fi
        done
    fi

    inst_multiple umount
    inst_multiple tr
    if ! dracut_module_included "systemd"; then
        inst_hook cmdline 95 "$moddir/parse-block.sh"
        inst_hook pre-udev 30 "$moddir/block-genrules.sh"
        inst_hook mount 99 "$moddir/mount-root.sh"
    fi
}

