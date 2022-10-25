from aws_cdk import aws_ecr as ecr
from aws_cdk.core import App
from source_cdk_patterns.accounts import SourceAWSAccount
from source_cdk_patterns.ecs import SourceRepo
from source_cdk_patterns.source_stack import SourceStack


class ControlDrydownAppRepoStack(SourceStack):
    def __init__(self, app: App, id: str, account: SourceAWSAccount, **kwargs) -> None:
        super().__init__(app, id, account=account, **kwargs)
        # Create ECR repos
        self.repo = SourceRepo(
            self,
            "ControlDrydownAppRepo",
            image_tag_mutability=ecr.TagMutability.MUTABLE,
            repository_name="control-drydown-app",
        )
