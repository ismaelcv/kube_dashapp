from aws_cdk import aws_s3 as s3, aws_ecr as ecr, App, Stack, Environment
from constructs import Construct
from cdk_template_patterns.ecr import EcrRepository
from typing import Dict, Optional, Union

from aws_cdk import aws_certificatemanager as cm
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_pat
from aws_cdk import aws_iam as iam
from aws_cdk import aws_logs as logs
from aws_cdk import aws_route53 as route53
import os

# from source_cdk_patterns import Environment, EnvironmentTier, exported_name_for_output, tag_dict, tag_resource


class ControlDrydownAppRepoStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        EcrRepository(
            self,
            id="dashapp-skeleton-repo-stack",
            image_tag_mutability=ecr.TagMutability.MUTABLE,
            repository_name="dashapp-skeleton-repo",
        )


class ECSAppDeploymentRepoStack(Stack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        # environment: Environment = Environment.DEVELOPMENT,
        # environment_tier: EnvironmentTier = EnvironmentTier.NON_PROD,
        # full_domain: str,
        image: Optional[Union[ecs.ContainerImage, str]] = None,
        # name: str,
        vpc_id: str,
        container_port: int = 8080,
        task_role: Optional[iam.IRole] = None,
        memory_reservation_mib: int = 128,
        memory_limit_mib: Optional[int] = None,
        cpu: int = 256,
        container_environment: Optional[Dict[str, str]] = None,
        container_secrets: Optional[Dict[str, ecs.Secret]] = None,
        health_check: Optional[str] = None,
        desired_count: int = 1,
        cloud_map_options: Optional[ecs.CloudMapOptions] = None,
        log_retention: logs.RetentionDays = logs.RetentionDays.ONE_WEEK,
        env: Environment,
    ):
        super().__init__(scope, id,env=env)
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
        vpc = ec2.Vpc.from_lookup(self, "VPC", vpc_id=vpc_id )

        print(vpc.vpc_id)

        # # Lookup ECS cluster
        # cluster_name_lookup_key = exported_name_for_output(self.environment.value, "ecs", "cluster-name")
        # cluster_name = Fn.import_value(cluster_name_lookup_key)
        # cluster = ecs.Cluster.from_cluster_attributes(
        #     self,
        #     "EcsClusterLookup",
        #     cluster_name=cluster_name,
        #     security_groups=[],
        #     vpc=vpc,
        # )

        # # Configure image
        # if isinstance(image, str):
        #     self.image = ecs.ContainerImage.from_asset(image)
        # else:
        #     self.image = image

        # log_group = logs.LogGroup(
        #     self,
        #     "AppLogGroup",
        #     log_group_name=name,
        #     retention=log_retention,
        # )
        # log_driver = ecs.LogDrivers.aws_logs(log_group=log_group, stream_prefix=name)

        # # Using Cloud Map for service discovery only works if you use the AWS_VPC network mode for your container
        # network_mode = ecs.NetworkMode.AWS_VPC if cloud_map_options is not None else ecs.NetworkMode.BRIDGE
        # task_definition = ecs.Ec2TaskDefinition(
        #     self,
        #     "TaskDefinition",
        #     network_mode=network_mode,
        #     task_role=task_role,
        #     family=name,
        # )
        # task_definition.add_container(
        #     "TaskContainer",
        #     image=self.image,
        #     container_name=f"{name}-container",
        #     port_mappings=[ecs.PortMapping(container_port=container_port)],
        #     logging=log_driver,
        #     environment=container_environment,
        #     memory_limit_mib=memory_limit_mib,
        #     memory_reservation_mib=memory_reservation_mib,
        #     cpu=cpu,
        #     secrets=container_secrets,
        # )

        # # Retrieve hosted zone for domain
        # zone = route53.PublicHostedZone.from_lookup(self, "HostedZone", domain_name=self.zone_name)

        # # Retrieve certificate for the domain that is used
        # certificate_arn = Fn.import_value(exported_name_for_output(self.zone_name, "certificate", "arn"))
        # certificate = cm.Certificate.from_certificate_arn(self, "GetCertificate", certificate_arn)

        # self.deployment = ecs_pat.ApplicationLoadBalancedEc2Service(
        #     self,
        #     "Deployment",
        #     cluster=cluster,
        #     memory_reservation_mib=memory_reservation_mib,
        #     memory_limit_mib=memory_limit_mib,
        #     cpu=cpu,
        #     task_definition=task_definition,
        #     service_name=name,
        #     certificate=certificate,
        #     domain_name=self.full_domain,
        #     domain_zone=zone,
        #     desired_count=desired_count,
        #     redirect_http=True,
        #     cloud_map_options=cloud_map_options,
        # )
        # tag_resource(self.deployment, Environment.tag_name, value=self.environment.value)
        # tag_resource(self.deployment, EnvironmentTier.tag_name, value=self.environment_tier.value)

        # self.deployment.target_group.configure_health_check(path=health_check)

        # # Lookup security group of auto-scaling group
        # security_group_id = Fn.import_value(
        #     exported_name_for_output(self.environment.value, "ecs", "asg-security-group-id")
        # )
        # sg = ec2.SecurityGroup.from_security_group_id(self, "ASGSG", security_group_id)
        # sg.connections.allow_from(self.deployment.load_balancer, port_range=ec2.Port.tcp_range(32768, 65535))


env_EU = Environment(account="501280619881", region="eu-central-1")


app = App()
ControlDrydownAppRepoStack(app, "dashapp-skeleton-deployment")
ECSAppDeploymentRepoStack(
    app,
    id="dashapp-skeleton-ECS-deployment",
    vpc_id="vpc-06dc3ac067318c5fc",
    env=env_EU,
)


#     app,
#     "ControlDrydownAppPrdStack",
#     account=SourceAWSAccount.PRODUCTION,
#     full_domain="drydown-control.source.ag",
#     repo=repo_stack.repo,


app.synth()
