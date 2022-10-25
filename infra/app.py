from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk.core import App
from source_cdk_patterns.accounts import SourceAWSAccount, tag_for_environment_and_tier
from source_cdk_patterns.ecs import ECSAppDeployment
from source_cdk_patterns.source_stack import SourceStack


class ControlDrydownAppStack(SourceStack):
    def __init__(
        self, app: App, id: str, account: SourceAWSAccount, full_domain: str, repo: ecr.IRepository, **kwargs
    ) -> None:
        super().__init__(app, id, account=account, **kwargs)

        bucket = s3.Bucket.from_bucket_name(
            self, f"source-ag-{account.environment.value}-control", f"source-ag-{account.environment.value}-control"
        )

        task_role = iam.Role(
            self,
            "ControlDrydownAppEcsRole",
            role_name="ControlDrydownAppEcsRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy")
            ],
        )

        bucket.grant_read(task_role, "*")

        env_vars = {"ENVIRONMENT": account.environment.value}

        self.app = ECSAppDeployment(
            self,
            "ControlDrydownAppDeployment",
            name="control-drydown-app",
            environment=account.environment,
            environment_tier=account.environment_tier,
            full_domain=full_domain,
            image=ecs.ContainerImage.from_ecr_repository(repo, tag=account.environment.value),
            task_role=task_role,
            container_port=8094,
            container_environment=env_vars,
            memory_reservation_mib=2048,
            health_check="/health",
        )

        tag_for_environment_and_tier(self.app, account=account)
