# file_management_flaskapp
A cloud-based Flask application for secure file management, leveraging AWS ECS, ALB, and S3 for seamless deployment and storage

## Features

- **File Upload**: Users can upload files directly to an S3 bucket.
- **File Listing**: Lists all files stored in the S3 bucket.
- **File Download**: Generates pre-signed URLs for secure file downloads.
- **Cloud Deployment**: Hosted on AWS ECS using a containerized Flask application.

## Prerequisites

1. **AWS Account**: Active AWS account with IAM user permissions.
2. **Docker**: Installed on your local machine for containerization.
3. **AWS CLI**: Installed and configured with proper credentials.
4. **Git**: Installed for version control.

## AWS Services Used

1. **Amazon S3**: For file storage.
2. **Amazon ECS (Fargate)**: To run the containerized application.
3. **Application Load Balancer (ALB)**: For routing traffic.
4. **CloudWatch**: For monitoring logs.
5. **IAM Roles**: For granting permissions to ECS tasks and services.

## Setup Instructions

### 1. S3 Bucket Configuration

- Create an S3 bucket.
- Update bucket policies to allow access from your ECS task role.
- Enable public access for testing (not recommended for production).

### 2. IAM Role Configuration

- Create an IAM role for ECS tasks with the following policies:
  - `AmazonS3FullAccess` (for testing) or specific S3 bucket policies.
  - `AmazonECSTaskExecutionRolePolicy` for ECS execution.
- Attach the role to your ECS service.

### 3. Application Code

- Clone the repository:
  ```bash
  git clone https://github.com/Sidd1303/file_management_flaskapp.git
  cd file_management_flaskapp
  ```
- Build the Docker image:
  ```bash
  docker build -t flask-app .
  ```
- Test locally:
  ```bash
  docker run -p 5000:5000 flask-app
  ```

### 4. Push Docker Image to ECR

- Create an ECR repository in AWS.
- Authenticate Docker to ECR:
  ```bash
  aws ecr get-login-password --region <region> | docker login --username AWS --password-stdin <account_id>.dkr.ecr.<region>.amazonaws.com
  ```
- Tag and push the image:
  ```bash
  docker tag flask-app:latest <account_id>.dkr.ecr.<region>.amazonaws.com/flask-app:latest
  docker push <account_id>.dkr.ecr.<region>.amazonaws.com/flask-app:latest
  ```

### 5. ECS and ALB Setup

1. **ECS Cluster**:
   - Create an ECS cluster using Fargate.
2. **Task Definition**:
   - Configure container settings (image, port 5000, environment variables).
3. **Service**:
   - Create a service in the ECS cluster.
   - Attach the ALB to the service.
4. **Application Load Balancer**:
   - Configure a listener on port 80.
   - Forward requests to the ECS target group.

### 6. VPC and Security Groups

- Ensure your ECS tasks are in a VPC with internet access.
- Configure security groups:
  - Allow inbound traffic from ALB to ECS on port 5000.
  - Allow outbound internet access for ECS tasks.

### 7. Test the Application

- Access the application via the ALB DNS name.
- Test file upload, listing, and download functionalities.

## Logs and Monitoring

- Use AWS CloudWatch to monitor ECS task logs.
- Troubleshoot errors by viewing logs directly from the AWS Console.

## Future Enhancements

- Implement HTTPS using ACM (AWS Certificate Manager).
- Add authentication and user management.
- Optimize permissions and policies for enhanced security.

