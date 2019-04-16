#!/usr/bin/env python3

import requests
import os
import json
from pick import pick
import argparse
from groupy.client import Client

parser = argparse.ArgumentParser(description="Control Yalebot directly")
parser.add_argument("verb", choices=("join", "leave", "send", "purge"))
parser.add_argument("--token", default=os.environ.get("GROUPME_ACCESS_TOKEN"))
parser.add_argument("--groups-file", default="groups.json")
parser.add_argument("--users-file", default="users.txt")
args = parser.parse_args()


def read(prop, default):
    return input(f"{prop} [{default}]: ") or default


def get_user_groups():
    return requests.get(f"https://api.groupme.com/v3/groups?token={args.token}").json()["response"]


def get_joined_groups():
    with open(args.groups_file, "r") as f:
        return json.load(f)


def save_groups(groups):
    with open(args.groups_file, "w") as f:
        json.dump(groups, f)


def pick_joined_group(groups=None) -> str:
    """
    :return: ID of group chosen
    """
    if groups is None:
        groups = get_joined_groups()
    group_name = pick([groups[group_id]["name"] for group_id in groups])[0]
    # Knowing name chosen, get group ID
    for candidate in groups:
        if groups[candidate]["name"] == group_name:
            group_id = candidate
            print(f"Selected group {group_id}/{group_name}.")
            return group_id


def pick_user_group(groups=None) -> str:
    """
    :return:
    """
    if groups is None:
        groups = get_user_groups()
    group_name = pick([group["name"] for group in groups])[0]
    # Knowing name chosen, get group id
    for candidate in groups:
        if candidate["name"] == group_name:
            group_id = candidate["group_id"]
            print(f"Selected group {group_id}/{group_name}.")
            return group_id


if args.verb == "send":
    groups = get_joined_groups()
    group_id = pick_joined_group(groups)
    while True:
        try:
            text = input("> ")
        except EOFError:
            print("\r", end="")
            break
        if not text:
            print("\r", end="")
            break
        # TODO: Merge the above two cases
        requests.post("https://api.groupme.com/v3/bots/post", data={"text": text, "bot_id": groups[group_id]["bot_id"]})
elif args.verb == "purge":
    group_id = 46649296
    client = Client.from_token(args.token)
    group = client.groups.get(id=group_id)
    with open(args.users_file, "r") as f:
        targets = [target.strip("\n") for target in f.readlines()]
        print(targets)
    print(group.members)
    for member in group.members:
        if member.name in targets:
            print(member.remove())
