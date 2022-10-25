from app import ControlDrydownAppStack
from aws_cdk.core import App
from repo import ControlDrydownAppRepoStack
from source_cdk_patterns.accounts import SourceAWSAccount

app = App()

repo_stack = ControlDrydownAppRepoStack(app, "ControlDrydownAppRepoStack", SourceAWSAccount.INFRA)

ControlDrydownAppStack(
    app,
    "ControlDrydownAppDevStack",
    account=SourceAWSAccount.DEVELOPMENT,
    full_domain="drydown-control.dev.source.ag",
    repo=repo_stack.repo,
)

ControlDrydownAppStack(
    app,
    "ControlDrydownAppPrdStack",
    account=SourceAWSAccount.PRODUCTION,
    full_domain="drydown-control.source.ag",
    repo=repo_stack.repo,
)

app.synth()
