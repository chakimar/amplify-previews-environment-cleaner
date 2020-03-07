import boto3
client = boto3.client("cloudformation")


def handler():
    print("Start cfn cleaner")
    stack_summaries = list_stacks_delete_failed(client)
    for stack_summary in stack_summaries:
        stack_id = stack_summary.get("StackId")
        delete_stack(client, stack_id)
    print("End cfn cleaner")


def list_stacks_delete_failed(client):
    response = client.list_stacks(
        StackStatusFilter=[
            "DELETE_FAILED",
        ]
    )
    stack_summaries = response.get("StackSummaries")
    while "NextToken" in response:
        next_token = response.get("NextToken")
        response = client.list_stacks(
            NextToken=next_token,
            StackStatusFilter=[
                "DELETE_FAILED",
            ]
        )
        next_stack_summaries = response.get("StackSummaries")
        stack_summaries.extend(next_stack_summaries)
    return stack_summaries


def delete_stack(client, stack_id):
    print("Delete cfn start : " + stack_id)
    client.delete_stack(
        StackName=stack_id,
    )
    print("Delete cfn complete : " + stack_id)
