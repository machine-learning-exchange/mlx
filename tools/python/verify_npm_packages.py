#!/usr/bin/env python3

# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

import sys
from typing import Tuple
from subprocess import PIPE, run

no_vulnerabilities = "found 0 vulnerabilities"


class colorText:
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    GREEN = "\033[0;32m"
    END = "\033[0;0m"


def audit_npm(continue_to_audit: bool):
    if not continue_to_audit:
        return

    format_vulnerablility_output = ""
    audit_npm = (
        run("npm audit fix", cwd="./dashboard/origin-mlx/", stdout=PIPE, shell=True)
        .stdout.decode("utf-8")
        .split("\n\n")
    )
    for message in audit_npm:
        format_vulnerablility_output = (
            message if "vulnerabilities" in message else format_vulnerablility_output
        )
    if no_vulnerabilities not in audit_npm:
        print(
            f"\n\n{colorText.RED}Vulnerabilites still present:\n{format_vulnerablility_output}{colorText.END}"
        )
        print("\nMaual investigation necessary to prevent breaking changes\n\n")
        print(
            f"Run:\n\t{colorText.GREEN}npm audit{colorText.END}\nand scroll up to manually manage breaking changes\n\n"
        )
        print(
            f"Run:\n\t{colorText.GREEN}npm audit fix --force{colorText.END}\nto force update all packages including breaking changes\n\n"
        )


def fix_vulnerabilities() -> Tuple[bool, str]:
    run(["rm", "package-lock.json"], cwd="./dashboard/origin-mlx/")
    update_npm = run(
        "npm update", cwd="./dashboard/origin-mlx/", stdout=PIPE, shell=True
    ).stdout.decode("utf-8")

    has_vulnerabilities = no_vulnerabilities not in update_npm
    return (has_vulnerabilities, update_npm)


def identify_remaining_vulnerabilities(
    identified_vulnerabilities: Tuple[bool, str]
) -> bool:
    has_vulnerabilities, update_npm = identified_vulnerabilities
    format_vulnerablility_output = ""
    update_npm = update_npm.split("\n")

    if has_vulnerabilities:
        for message in update_npm:
            format_vulnerablility_output = (
                message
                if "vulnerabilities" in message
                else format_vulnerablility_output
            )
        user_input = input(
            f"{colorText.RED}\n\nVulnerabilities found:\n{format_vulnerablility_output}{colorText.END}\n\nWould you like to audit? [y,n]: "
        )
        return True if user_input in ["Y", "y"] else False


def verify_npm_packages():
    check_outdated = run("npm outdated", cwd="./dashboard/origin-mlx/", shell=True)
    packages_outdated = f"\n\nFound outdated npm packages\n"
    packages_up_to_date = "All packages up to date"

    check_vulnerabilities = run("npm audit", cwd="./dashboard/origin-mlx/", stdout=PIPE, shell=True
    ).stdout.decode("utf-8").split('\n')
    vulnerabilities = [word for word in check_vulnerabilities if 'vulnerabilities' in word]
    packages_vulnerable = f'''\nFound vulnerable packages\n\n{colorText.RED}{vulnerabilities[0]}{colorText.END}\n
                            \rRun {colorText.BLUE}make update_npm_packages{colorText.END} to secure/update\n'''
    packages_safe = "\nNo vulnerabilities found"

    print(packages_up_to_date) if check_outdated.returncode == 0 else print(packages_outdated)
    print('-' * 40)

    if "0 vulnerabilities" not in vulnerabilities[0]:
        print(packages_vulnerable)
        exit(1)
    else:
        print(packages_safe)


if __name__ == "__main__":
    if "--update" in sys.argv:
        remaining_vulnerabilities = fix_vulnerabilities()
        continue_to_audit = identify_remaining_vulnerabilities(
            remaining_vulnerabilities
        )
        audit_npm(continue_to_audit)
    else:
        verify_npm_packages()
