# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0
import json
import os
import requests
import subprocess
import tarfile
import shutil


internal_github_raw_url = os.getenv(
    "internal_github_raw_url",
    "https://raw.githubusercontent.com/machine-learning-exchange/mlx/main/",
)
api_url = os.getenv("mlx_api", "mlx-api")
token = os.getenv("enterprise_github_token", "")
repo_name = "mlx"
asset_categories = ["pipelines", "components", "models", "notebooks", "datasets"]


def get_github_files(asset_name, asset_list):
    os.makedirs(asset_name, exist_ok=True)
    for asset in asset_list:
        if token:
            headers = {
                "Accept": "application/vnd.github.v3.raw",
                "Authorization": "token " + token,
            }
        else:
            headers = {}
        if "://" not in asset["source"] and token:
            r = requests.get(internal_github_raw_url + asset["source"], headers=headers)
        elif "raw.github.ibm.com" in asset["source"] and token:
            r = requests.get(asset["source"], headers=headers)
        elif "://" in asset["source"]:
            r = requests.get(asset["source"])
        else:
            continue

        if asset_name != "components":
            filename = os.path.basename(asset["source"])
        else:
            filename = asset["name"].replace(" ", "-") + ".yaml"
        with open(os.path.join(asset_name, filename), "w") as file:
            file.write(r.text)
            asset["download"] = "true"


def upload_asset(asset_name, asset_list):
    for asset in asset_list:
        if asset.get("download", "") == "true":
            if asset_name != "components":
                filename = os.path.basename(asset["source"])
            else:
                filename = asset["name"].replace(" ", "-") + ".yaml"
            tarname = filename.replace(".yaml", ".tgz")
            tarfile_path = os.path.join(asset_name, tarname)
            with tarfile.open(tarfile_path, "w:gz") as tar:
                tar.add(os.path.join(asset_name, filename), arcname=filename)
            tar.close()
            params = {"name": asset.get("name", "")}
            if asset_name == "notebooks" and "://" not in asset["source"] and token:
                data = {"enterprise_github_token": token}
            else:
                data = {}
            with open(os.path.join(asset_name, tarname), "rb") as f:
                r = requests.post(
                    "http://" + api_url + "/apis/v1alpha1/" + asset_name + "/upload",
                    params=params,
                    files={"uploadfile": f},
                    data=data,
                )
            print(r.text)


def cleanup_assets(asset_name):
    r = requests.delete("http://" + api_url + "/apis/v1alpha1/" + asset_name + "/*")
    print(r.text)


def get_github_dir_files(asset_name, asset_list):
    os.makedirs(asset_name, exist_ok=True)
    if token:
        headers = {
            "Accept": "application/vnd.github.v3.raw",
            "Authorization": "token " + token,
        }
        internal_github_url = internal_github_raw_url.replace(
            "raw.", token + "@"
        ).replace("/master/", "")
        command = ["git", "clone", internal_github_url, repo_name]
        subprocess.run(command, check=True)
    for asset in asset_list:
        if "://" not in asset["source"] and token:
            shutil.copytree(
                repo_name + "/" + asset["source"],
                asset_name + "/" + asset["name"].replace(" ", "-"),
            )
            asset["url"] = internal_github_url + "/" + asset["source"]
            asset["download"] = "true"
        elif "://" in asset["source"]:
            source_pieces = asset["source"].split("/")
            github_url = "/".join(source_pieces[0:5])
            github_repo = source_pieces[4]
            source_dir = "/".join(source_pieces[7:])
            command = ["git", "clone", github_url, github_repo]
            if github_repo not in os.listdir("."):
                subprocess.run(command, check=True)
            shutil.copytree(
                github_repo + "/" + source_dir,
                asset_name + "/" + asset["name"].replace(" ", "-"),
            )
            asset["url"] = asset["source"]
            asset["download"] = "true"


def upload_dir_asset(asset_name, asset_list):
    for asset in asset_list:
        if asset.get("download", "") == "true":
            dirname = asset["name"].replace(" ", "-")
            tarname = dirname + ".tgz"
            tarfile_path = os.path.join(asset_name, tarname)
            with tarfile.open(tarfile_path, "w:gz") as tar:
                for filename in os.listdir(os.path.join(asset_name, dirname)):
                    if filename.endswith(".yaml") or filename.endswith(".yml"):
                        tar.add(
                            os.path.join(asset_name, dirname, filename),
                            arcname=filename,
                        )
            tar.close()
            with open(os.path.join(asset_name, tarname), "rb") as f:
                params = {"name": asset.get("name", ""), "url": asset.get("url", "")}
                r = requests.post(
                    "http://" + api_url + "/apis/v1alpha1/" + asset_name + "/upload",
                    files={"uploadfile": f},
                    params=params,
                )
            print(r.text)


def feature_default_assets():
    for category in asset_categories:
        data = ["*"]
        r = requests.post(
            "http://" + api_url + "/apis/v1alpha1/" + category + "/publish_approved",
            json=data,
        )
        print(r.text)
        r = requests.post(
            "http://" + api_url + "/apis/v1alpha1/" + category + "/featured", json=data
        )
        print(r.text)


if __name__ == "__main__":
    with open("/etc/config.json", "r") as f:
        samples = json.load(f)
    f.close()
    if os.getenv("cleanup", "") == "true":
        for category in asset_categories:
            cleanup_assets(category)

    get_github_files("pipelines", samples["pipelines"])
    get_github_files("components", samples["components"])
    get_github_files("models", samples["models"])
    get_github_files("notebooks", samples["notebooks"])
    get_github_files("datasets", samples["datasets"])

    if api_url:
        for asset in samples["pipelines"]:
            if asset.get("download", "") == "true":
                filename = os.path.basename(asset["source"])
                tarname = filename + ".tar.gz"
                command = [
                    "dsl-compile",
                    "--py",
                    os.path.join("pipelines", filename),
                    "--output",
                    os.path.join("pipelines", tarname),
                ]
                subprocess.run(command, check=True)
                with open(os.path.join("pipelines", tarname), "rb") as f:
                    params = {
                        "name": asset.get("name", ""),
                        "description": asset.get("description", ""),
                    }
                    data = {"annotations": json.dumps(asset.get("annotations", {}))}
                    r = requests.post(
                        "http://" + api_url + "/apis/v1alpha1/pipelines/upload",
                        files={"uploadfile": f},
                        params=params,
                        data=data,
                    )
                print(r.text)

    upload_asset("components", samples["components"])
    upload_asset("models", samples["models"])
    upload_asset("notebooks", samples["notebooks"])
    upload_asset("datasets", samples["datasets"])
    feature_default_assets()
