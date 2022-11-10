# TODO: Make sure CI/CD pipeline works
# TODO: Hide var names on env variables
# TODO : document


from aws_cdk import App, Duration, Environment, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_elasticloadbalancingv2 as elb
from aws_cdk import aws_iam as iam
from constructs import Construct

ECR_REPO_NAME = "cdk-dashapp-repo"
SECURITY_GROUP_ID = "sg-0991712be7fe6dde3"
ENVIRONMENT = Environment(account="501280619881", region="eu-central-1")
CONTAINER_PORT = 8094
CONTAINER_NAME = "Cdk-container"


class CreateRepoStack(Stack):
    """
    This Stack creates the following infra:
    - ECR Repo
    """

    def __init__(self, scope: Construct, stack_id: str, **kwargs):
        super().__init__(scope, stack_id, **kwargs)

        self.repo = ecr.Repository(
            self,
            id="Create Repository",
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

        cluster = ecs.Cluster(self, id="Create Cluster", vpc=vpc, cluster_name="fargate_cdk_cluster")

        task_role = iam.Role(
            self,
            "Create task definition role",
            role_name="DashAppTaskDefinitionEcsRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy"),
            ],
        )

        task_role.add_to_policy(
            iam.PolicyStatement(
                sid="AllowWriteByCiCdPolicy",
                actions=["s3:GetObject*", "s3:GetBucket*", "s3:List*"],
                resources=[
                    "arn:aws:s3:::lambda-github-actions-test-bucket",
                    "arn:aws:s3:::lambda-github-actions-test-bucket/*",
                ],
                effect=iam.Effect.ALLOW,
            ),
        )

        image = ecs.ContainerImage.from_ecr_repository(repo)

        task_definition = ecs.FargateTaskDefinition(
            self,
            id="Add task defnition",
            family="cdk-task-definition_fargate",
            task_role=task_role,
            execution_role=task_role,
        )
        task_definition.add_container(
            id="Add Containter to task defintion",
            image=image,
            container_name=CONTAINER_NAME,
            port_mappings=[ecs.PortMapping(container_port=CONTAINER_PORT)],
            memory_reservation_mib=128,
            cpu=0,
        )

        load_balancer_sg = ec2.SecurityGroup(
            self,
            "create load balancersecurity group",
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="load_balancer",
        )
        load_balancer_sg.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(CONTAINER_PORT))
        load_balancer_sg.add_ingress_rule(peer=ec2.Peer.any_ipv6(), connection=ec2.Port.tcp(CONTAINER_PORT))
        load_balancer_sg.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(80))

        load_balancer = elb.ApplicationLoadBalancer(
            self,
            "Create Load Balancer",
            load_balancer_name="cdk-load-balancer",
            vpc=vpc,
            internet_facing=True,
            security_group=load_balancer_sg,
        )

        listener = elb.ApplicationListener(
            self,
            "Create listener",
            load_balancer=load_balancer,
            port=80,
        )

        fargate_sg = ec2.SecurityGroup(
            self,
            "create fargate security group",
            vpc=vpc,
            allow_all_outbound=True,
            security_group_name="fargate_service",
        )
        fargate_sg.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(CONTAINER_PORT))
        fargate_sg.add_ingress_rule(peer=ec2.Peer.any_ipv6(), connection=ec2.Port.tcp(CONTAINER_PORT))

        ecs.FargateService(
            self,
            "Fargate Service Deployment",
            cluster=cluster,
            task_definition=task_definition,
            service_name="cdkDashappFargateService",
            assign_public_ip=True,
            security_groups=[fargate_sg],
            health_check_grace_period=Duration.seconds(30),
        ).register_load_balancer_targets(
            ecs.EcsTarget(
                container_name=CONTAINER_NAME,
                container_port=CONTAINER_PORT,
                new_target_group_id="ECS",
                listener=ecs.ListenerConfig.application_listener(
                    listener,
                    protocol=elb.ApplicationProtocol.HTTP,
                    health_check={"path": "/health"},
                ),
            ),
        )


app = App()
CreateRepoStack(app, stack_id="CreateRepoStack")
ECSAppDeploymentStack(app, stack_id="dashappSkeletonECSDeploymentStack")

app.synth()
