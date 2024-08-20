import sys
import requests
import argparse
import auth


def create_lakehouse(workspace_id, lakehouse_name, enable_schemas):
    headers = {"Authorization": "Bearer " + auth.interactive_auth()}
    body = {"displayName": lakehouse_name, "workloadPayload": f"{{\"enableSchemas\": {enable_schemas}}}"}
    response = requests.post(f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses", headers=headers, json=body)

    if response.status_code == 201:
        print("Lakehouse created successfully")
    else:
        print("Error creating lakehouse")
        print(response.json())

def delete_lakehouse(workspace_id, lakehouse_id):
    headers = {"Authorization": "Bearer " + auth.interactive_auth()}
    response = requests.delete(f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}", headers=headers)

    if response.status_code == 204:
        print("Lakehouse deleted successfully")
    else:
        print("Error deleting lakehouse")
        print(response.json())

def update_lakehouse( workspace_id, lakehouse_id, lakehouse_name):
    headers = {"Authorization": "Bearer " + auth.interactive_auth()}
    body = {"displayName": lakehouse_name}
    response = requests.patch(f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses/{lakehouse_id}", headers=headers, json=body)

    if response.status_code == 200:
        print("Lakehouse updated successfully")
    else:
        print("Error updating lakehouse")
        print(response.json())

def list_lakehouses( workspace_id):
    headers = {"Authorization": "Bearer " + auth.interactive_auth()}
    response = requests.get(f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/lakehouses", headers=headers)

    if response.status_code == 200:
        lakehouses = response.json()
        for lakehouse in lakehouses:
            print(lakehouse["id"], lakehouse["displayName"])
    else:
        print("Error listing lakehouses")
        print(response.json())


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Manage lakehouses in a workspace.")
    subparsers = parser.add_subparsers(dest="command")

    # Subparser for the create command
    parser_create = subparsers.add_parser("create", help="Create a new lakehouse")
    parser_create.add_argument("workspace_id", help="The ID of the workspace")
    parser_create.add_argument("lakehouse_name", help="The name of the lakehouse")
    parser_create.add_argument("enable_schemas", type=bool, help="Enable schemas (true/false)")

    # Subparser for the delete command
    parser_delete = subparsers.add_parser("delete", help="Delete an existing lakehouse")
    parser_delete.add_argument("workspace_id", help="The ID of the workspace")
    parser_delete.add_argument("lakehouse_id", help="The ID of the lakehouse")

    # Subparser for the update command
    parser_update = subparsers.add_parser("update", help="Update an existing lakehouse")
    parser_update.add_argument("workspace_id", help="The ID of the workspace")
    parser_update.add_argument("lakehouse_id", help="The ID of the lakehouse")
    parser_update.add_argument("lakehouse_name", help="The new name of the lakehouse")

    # Subparser for the list command
    parser_list = subparsers.add_parser("list", help="List all lakehouses in a workspace")
    parser_list.add_argument("workspace_id", help="The ID of the workspace")

    args = parser.parse_args()

    if args.command == "create":
        
        create_lakehouse(args.workspace_id, args.lakehouse_name, args.enable_schemas)
    elif args.command == "delete":
        delete_lakehouse(args.workspace_id, args.lakehouse_id)
    elif args.command == "update":
        update_lakehouse(args.workspace_id, args.lakehouse_id, args.lakehouse_name)
    elif args.command == "list":
        list_lakehouses(args.workspace_id)
    else:
        parser.print_help()
