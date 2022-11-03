"""

        # # Retrieve hosted zone for domain
        # zone = route53.PublicHostedZone.from_lookup(self, "HostedZone", domain_name=self.zone_name)

        # # Retrieve certificate for the domain that is used
        # certificate_arn = Fn.import_value(exported_name_for_output(self.zone_name, "certificate", "arn"))
        # certificate = cm.Certificate.from_certificate_arn(self, "GetCertificate", certificate_arn)



        # tag_resource(self.deployment, Environment.tag_name, value=self.environment.value)
        # tag_resource(self.deployment, EnvironmentTier.tag_name, value=self.environment_tier.value)

        self.deployment.target_group.configure_health_check(path=health_check)

"""

from aws_cdk import App, Environment, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_iam as iam
from constructs import Construct

ECR_REPO_NAME = "manual-private-dashapp-repo"
SECURITY_GROUP_ID = "sg-0991712be7fe6dde3"
ENVIRONMENT = Environment(account="501280619881", region="eu-central-1")
CONTAINER_PORT = HOST_PORT = 8094


class CreateEcrRepoStack(Stack):
    """
    This Stack creates the following infra:
    - ECR Repo
    """

    def __init__(self, scope: Construct, stack_id: str, **kwargs):
        super().__init__(scope, stack_id, **kwargs)

        self.repo = ecr.Repository(
            self,
            id="dashapp-skeleton-repo",
            image_tag_mutability=ecr.TagMutability.MUTABLE,
            repository_name=ECR_REPO_NAME,
        )


class ECSAppDeploymentStack(Stack):
    """
    This Stack creates the following infra:
    - ECS Task
    """

    def __init__(self, scope: Construct, stack_id: str):
        super().__init__(
            scope,
            id=stack_id,
            env=ENVIRONMENT,
        )

        repo = ecr.Repository.from_repository_name(self, id="repo_lookup", repository_name=ECR_REPO_NAME)
        vpc = ec2.Vpc.from_lookup(self, "VPC", is_default=True)

        cluster = ecs.Cluster.from_cluster_attributes(
            self,
            "EcsClusterLookup",
            cluster_name="copyCluster",
            security_groups=[],
            vpc=vpc,
        )

        task_role = iam.Role(
            self,
            "Create task definition role",
            role_name="DashAppTaskDefinitionEcsRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy"),
                iam.PolicyStatement(
                    sid="AllowWriteByCiCdPolicy",
                    actions=["s3:GetObject*", "s3:GetBucket*", "s3:List*"],
                    resources=[
                        "arn:aws:s3:::lambda-github-actions-test-bucket",
                        "arn:aws:s3:::lambda-github-actions-test-bucket/*",
                    ],
                    effect=iam.Effect.ALLOW,
                ),
            ],
        )

        task_definition = ecs.Ec2TaskDefinition(
            self,
            id="Add task defnition",
            family="cdk-task-definition_new",
            task_role=task_role,
            network_mode=ecs.NetworkMode.BRIDGE,
        )

        image = ecs.ContainerImage.from_ecr_repository(repo)

        task_definition.add_container(
            id="Add Containter to task defintion",
            image=image,
            container_name="Cdk-container",
            port_mappings=[ecs.PortMapping(container_port=CONTAINER_PORT, host_port=HOST_PORT)],
            memory_reservation_mib=100,
            cpu=0,
        )

        # ecs.Ec2Service(self, "Service", cluster=cluster, task_definition=task_definition)

        ecs_patterns.ApplicationLoadBalancedEc2Service(
            self,
            "ECSServiceDeployment",
            cluster=cluster,
            memory_reservation_mib=2048,
            # memory_limit_mib=memory_limit_mib,
            cpu=256,
            task_definition=task_definition,
            service_name="DashappDeploymentService",
            # certificate=certificate,
            # domain_name=self.full_domain,
            # domain_zone=zone,
            desired_count=2,
            # redirect_http=True,
            # cloud_map_options=cloud_map_options,
        )


app = App()
CreateEcrRepoStack(app, stack_id="dashappSkeletonRepoDeploymentStack")
ECSAppDeploymentStack(app, stack_id="dashappSkeletonECSDeploymentStack")

app.synth()
