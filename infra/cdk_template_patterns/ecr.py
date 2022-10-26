from typing import Optional, Sequence

from aws_cdk import aws_ecr as ecr
from aws_cdk import RemovalPolicy
from constructs import Construct


class EcrRepository(ecr.Repository):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        image_scan_on_push: Optional[bool] = None,
        image_tag_mutability: Optional[ecr.TagMutability] = None,
        lifecycle_registry_id: Optional[str] = None,
        lifecycle_rules: Optional[Sequence[ecr.LifecycleRule]] = None,
        removal_policy: Optional[RemovalPolicy] = None,
        repository_name: Optional[str] = None,
    ) -> None:
        super().__init__(
            scope,
            id,
            image_scan_on_push=image_scan_on_push,
            image_tag_mutability=image_tag_mutability,
            lifecycle_registry_id=lifecycle_registry_id,
            lifecycle_rules=lifecycle_rules,
            removal_policy=removal_policy,
            repository_name=repository_name,
        )
