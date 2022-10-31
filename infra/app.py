from typing import Optional

from aws_cdk import App, Environment, Stack
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecr as ecr
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_pat
from aws_cdk import aws_iam as iam
from aws_cdk import aws_logs as logs
from constructs import Construct


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
            repository_name="dashapp-skeleton-repo",
        )


class ECSAppDeploymentStack(Stack):
    """
    This Stack creates the following infra:
    - ECS Task definition
    """

    def __init__(  # pylint: disable=too-many-arguments, too-many-locals
        self,
        scope: Construct,
        stack_id: str,
        # environment: Environment = Environment.DEVELOPMENT,
        # environment_tier: EnvironmentTier = EnvironmentTier.NON_PROD,
        # full_domain: str,
        name: str,  # This is the name we have to provide to our app
        vpc_id: str,
        repo: ecs.ContainerImage,
        env: Environment,
        memory_reservation_mib: int = 128,
        memory_limit_mib: Optional[int] = None,
        cpu: int = 256,
        # container_environment: Optional[Dict[str, str]] = None,
        # container_secrets: Optional[Dict[str, ecs.Secret]] = None,
        health_check: Optional[str] = None,
        desired_count: int = 1,
        cloud_map_options: Optional[ecs.CloudMapOptions] = None,
        container_port: int = 8080,
    ):
        super().__init__(scope, stack_id, env=env)
        # assert image is not None, "The parameter `image` is required!"
        # if full_domain is not None:
        #     assert full_domain.count(".") > 1, "The full domain needs to be provided!"

        # self.environment = environment
        # self.environment_tier = environment_tier
        # self.full_domain = full_domain
        # if self.full_domain is not None:
        #     self.record_name = full_domain.split(".")[0]
        #     self.zone_name = ".".join(full_domain.split(".")[1:])
        # else:
        #     self.record_name = None
        #     self.zone_name = None
        # env_tag = tag_dict(Environment.tag_name, value=self.environment.value)

        # Lookup VPC
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id)

        # vpc = ec2.Vpc.from_Vpc_Attributes(this, 'myvpc', {
        #     vpcId: "vpc-xxxxxxxxxxxxxxxx",
        #     availabilityZones: ['ap-southeast-2a','ap-southeast-2b','ap-southeast-2c'],
        #     privateSubnetIds: ['subnet-xxxxxxxxxxxx', 'subnet-xxxxxxxxxxxx', 'subnet-xxxxxxxxxxxx']
        #     })

        cluster = ecs.Cluster.from_cluster_attributes(
            self,
            "EcsClusterLookup",
            cluster_name="development-cluster",
            security_groups=[],
            vpc=vpc,
        )

        image = ecs.ContainerImage.from_ecr_repository(repo)

        log_group = logs.LogGroup(
            self,
            "AppLogGroup",
            log_group_name=name,
            retention=logs.RetentionDays.ONE_WEEK,
        )

        log_driver = ecs.LogDrivers.aws_logs(log_group=log_group, stream_prefix=name)

        print("VPC        :", vpc.vpc_id, vpc.vpc_arn, vpc.public_subnets)
        print("Cluster    :", cluster.cluster_name, cluster.cluster_arn)
        print("image      :", image.image_name)
        print("log group  :", log_group.log_group_name, log_group.log_group_arn)
        print("log_driver :", log_driver.aws_logs)

        # # Using Cloud Map for service discovery only works if you use the AWS_VPC network mode for your container
        network_mode = ecs.NetworkMode.AWS_VPC if cloud_map_options is not None else ecs.NetworkMode.BRIDGE

        task_role = iam.Role(
            self,
            "ControlDrydownAppEcsRole",
            role_name="ControlDrydownAppEcsRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy"),
                iam.PolicyStatement(
                    sid="AllowWriteByCiCdPolicy",
                    actions=["s3:GetObject*", "s3:GetBucket*", "s3:List*"],
                    resources=[
                        "arn:aws:s3:::source-ag-development-control",
                        "arn:aws:s3:::source-ag-development-control/*",
                    ],
                    effect=iam.Effect.ALLOW,
                ),
            ],
        )

        task_definition = ecs.Ec2TaskDefinition(
            self,
            id="TaskDefinition",
            network_mode=network_mode,
            task_role=task_role,
            family=name,
        )

        task_definition.add_container(
            id="TaskContainer",
            image=image,
            container_name=f"{name}-container",
            port_mappings=[ecs.PortMapping(container_port=container_port)],
            logging=log_driver,
            # environment=container_environment,
            memory_limit_mib=memory_limit_mib,
            memory_reservation_mib=memory_reservation_mib,
            cpu=cpu,
            # secrets=container_secrets,
        )

        # # Retrieve hosted zone for domain
        # zone = route53.PublicHostedZone.from_lookup(self, "HostedZone", domain_name=self.zone_name)

        # # Retrieve certificate for the domain that is used
        # certificate_arn = Fn.import_value(exported_name_for_output(self.zone_name, "certificate", "arn"))
        # certificate = cm.Certificate.from_certificate_arn(self, "GetCertificate", certificate_arn)

        self.deployment = ecs_pat.ApplicationLoadBalancedEc2Service(
            self,
            "Deployment",
            cluster=cluster,
            memory_reservation_mib=memory_reservation_mib,
            memory_limit_mib=memory_limit_mib,
            cpu=cpu,
            task_definition=task_definition,
            service_name=name,
            # certificate=certificate,
            # domain_name=self.full_domain,
            # domain_zone=zone,
            desired_count=desired_count,
            # redirect_http=True,
            cloud_map_options=cloud_map_options,
        )

        # tag_resource(self.deployment, Environment.tag_name, value=self.environment.value)
        # tag_resource(self.deployment, EnvironmentTier.tag_name, value=self.environment_tier.value)

        self.deployment.target_group.configure_health_check(path=health_check)

        # Lookup security group of auto-scaling group
        # security_group_id = Fn.import_value(
        #     exported_name_for_output(self.environment.value, "ecs", "asg-security-group-id")
        # )
        sg = ec2.SecurityGroup.from_security_group_id(self, "ASGSG", "sg-0739218843c74d866")
        sg.connections.allow_from(self.deployment.load_balancer, port_range=ec2.Port.tcp_range(32768, 65535))


env_EU = Environment(account="501280619881", region="eu-central-1")


app = App()
repo_stack = CreateEcrRepoStack(app, "dashapp-skeleton-deployment-stack")
ECSAppDeploymentStack(
    app,
    stack_id="dashapp-skeleton-ECS-deployment-stack",
    name="dashapp_skeleton",
    vpc_id="vpc-06dc3ac067318c5fc",
    env=env_EU,
    repo=repo_stack.repo,
    container_port=8094,
    memory_reservation_mib=2048,
    health_check="/health",
)

app.synth()
