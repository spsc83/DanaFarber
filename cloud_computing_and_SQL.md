# Cloud Computing:
## 1 How would you architect a framework for sharing large files (10Gb-25Gb) on the cloud with access controls at the file level? We want to share the same file with multiple users without making a copy. The users should be able to have access to the data on any cloud platform to run bioinformatics analysis pipelines. The users can run any cloud service, there is no restriction. The framework’s responsibility is only to make data accessible with access controls.
I think AWS S3 would be a good choice in this use case.
- The limitation of the file size of a S3 object is up to 5TB. So 10 ~ 25GB won’t be a problem.
- Each user could have credentials of an IAM account with a particular policy. With the policy, we can limit the user's access at the file level. And one file can be shared with multiple users. Below is an example of the policy piece limiting the user to have read-only access with target_file*.
```
{
	"Sid": "LimitReadAccessToTargetFiles",
	"Effect": "Allow",
	"Action": [
		"s3:ListBucket",
		"s3:GetObject*"
	],
	"Resource": [
		"arn:aws:s3:::{bucket_name} ",
		"arn:aws:s3:::{bucket_name} /target_file*",

	]
}
```


- AWS S3 bucket can be mounted with multiple tools, for example, mount-s3. The mounted S3 bucket looks like a native disk. The user can run any bioinformatics software with the files that he has access in the bucket.


## 2 Evaluate the benefits and limitations of using containerization and container orchestration technologies, such as Docker and Kubernetes, for deploying and managing bioinformatics HPC workloads in the cloud.
Benefits:
- Isolation and Reproducibility: Containers provide a isolated environment for running bioinformatics applications. They encapsulate all dependencies and configurations, ensuring reproducibility of analyses across different environments, which is crucial in bioinformatics research.
- Portability: Docker containers can be easily moved between different cloud environments and on-premises infrastructure.
- Scalability: Container orchestration platforms like Kubernetes enable automatic scaling of bioinformatics workloads based on demand.
- Lightweight: Containers consume fewer resources compared to traditional virtual machines, allowing for better utilization of cloud resources and cost optimization.
- Kubernetes is Free.
- Service Discovery and Load Balancing: Kubernetes offers built-in features for service discovery and load balancing, simplifying the deployment and management of distributed bioinformatics applications across multiple containers and nodes.

Limitations:
- Learning Curve: Containerization and container orchestration technologies have a steep learning curve, especially for bioinformatics researchers who may not have extensive experience with software development and DevOps practices. Managing containerized bioinformatics workloads in a distributed environment using Kubernetes involves dealing with complex configurations, networking, and storage considerations, which may require specific expertise.
- Security Concerns: Although containers provide isolation, misconfigurations or vulnerabilities in container images or orchestrator components could potentially lead to security breaches or data leaks.



# SQL:
'HAVING' should be used together with 'GROUP BY'. The correct SQL should be:
```sql
SELECT UserId, AVG(Total) AS AvgOrderTotal FROM Invoices GROUP BY UserId HAVING COUNT(OrderId) >= 1;

```


