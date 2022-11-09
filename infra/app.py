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

from aws_cdk import App, Duration, Environment, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as elb
from aws_cdk import aws_iam as iam
from constructs import Construct

ECR_REPO_NAME = "cdk-dashapp-repo"
SECURITY_GROUP_ID = "sg-0991712be7fe6dde3"
ENVIRONMENT = Environment(account="501280619881", region="eu-central-1")
CONTAINER_PORT = 8094


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
            container_name="Cdk-container",
            port_mappings=[ecs.PortMapping(container_port=CONTAINER_PORT)],
            memory_reservation_mib=128,
            cpu=0,
        )

        security_group_lb = ec2.SecurityGroup(
            self, "create security group", vpc=vpc, allow_all_outbound=True, security_group_name="load_balancer"
        )
        security_group_lb.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(CONTAINER_PORT))
        security_group_lb.add_ingress_rule(peer=ec2.Peer.any_ipv6(), connection=ec2.Port.tcp(CONTAINER_PORT))
        security_group_lb.add_ingress_rule(peer=ec2.Peer.any_ipv4(), connection=ec2.Port.tcp(80))

        target_group = elb.ApplicationTargetGroup(
            self,
            "create target_group",
            target_group_name="tg-dashapp-cdk",
            vpc=vpc,
            health_check={"path": "/health"},
            port=80,
            target_type=elb.TargetType.IP,
        )

        load_balancer = elb.ApplicationLoadBalancer(
            self,
            "Create Load Balancer",
            load_balancer_name="cdk-load-balancer",
            vpc=vpc,
            internet_facing=True,
            security_group=security_group_lb,
        )

        listener = elb.ApplicationListener(
            self,
            "Create listener",
            default_target_groups=[target_group],
            load_balancer=load_balancer,
            port=80,
        )

        # lb = elbv2.ApplicationLoadBalancer(self, "LB", vpc=vpc, internet_facing=True)
        # listener = load_balancer.add_listener("Listener", port=80)
        # service.register_load_balancer_targets(
        #     container_name="web",
        #     container_port=80,
        #     new_target_group_id="ECS",
        #     listener=ecs.ListenerConfig.application_listener(listener,
        #         protocol=elbv2.ApplicationProtocol.HTTPS
        #     )
        # )

        service = ecs.FargateService(
            self,
            "Farghate Service Deployment",
            cluster=cluster,
            task_definition=task_definition,
            service_name="cdkDashappFargateService",
            # certificate=certificate,
            # domain_name=self.full_domain,
            # domain_zone=zone,
            # redirect_http=True,
            # cloud_map_options=cloud_map_options,
            health_check_grace_period=Duration.seconds(30),
        ).register_load_balancer_targets(
            ecs.EcsTarget(
                container_name="Cdk-container",
                container_port=CONTAINER_PORT,
                new_target_group_id="ECS",
                listener=ecs.ListenerConfig.application_listener(listener, protocol=elb.ApplicationProtocol.HTTPS),
            )
        )


app = App()
CreateRepoStack(app, stack_id="CreateRepoStack")
ECSAppDeploymentStack(app, stack_id="dashappSkeletonECSDeploymentStack")

app.synth()
