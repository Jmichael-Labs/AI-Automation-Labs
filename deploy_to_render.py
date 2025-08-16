#!/usr/bin/env python3
"""
Deploy Reddit AI Bot to Render.com
Uses Render API for automated deployment
"""

import requests
import json
import os
import time

class RenderDeployer:
    def __init__(self):
        self.api_key = "rnd_zJ8NMqR78ZJmkbqw9VCH2wDNQZZP"
        self.base_url = "https://api.render.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def create_service(self):
        """Create Reddit AI Bot service on Render"""
        
        service_config = {
            "type": "web_service",
            "name": "reddit-ai-problem-solver",
            "repo": "https://github.com/Jmichael-Labs/reddit-ai-problem-solver.git",
            "branch": "main",
            "buildCommand": "pip install -r requirements.txt",
            "startCommand": "python app.py",
            "plan": "free",
            "region": "oregon",
            "env": "python",
            "pythonVersion": "3.11.0",
            "envVars": [
                {
                    "key": "REDDIT_CLIENT_ID",
                    "value": "nv0Nr-9S1M3l152z4svinw"
                },
                {
                    "key": "REDDIT_CLIENT_SECRET", 
                    "value": "NWoge_4_FJZm0sq7l20Clx_nxti6hQ"
                },
                {
                    "key": "REDDIT_USER_AGENT",
                    "value": "AIBot:v1.0 (by /u/SwordfishMany6633)"
                },
                {
                    "key": "REDDIT_USERNAME",
                    "value": "SwordfishMany6633"
                },
                {
                    "key": "REDDIT_PASSWORD",
                    "value": "Makermoney100K@"
                },
                {
                    "key": "EMAIL_CONTACT",
                    "value": "jmichaeloficial@gmail.com"
                },
                {
                    "key": "INSTAGRAM_CONSULTING",
                    "value": "https://www.instagram.com/jmichaeloficial/"
                }
            ]
        }
        
        response = requests.post(
            f"{self.base_url}/services",
            headers=self.headers,
            json=service_config
        )
        
        if response.status_code == 201:
            service = response.json()
            print(f"✅ Service created successfully!")
            print(f"🌐 Service ID: {service['id']}")
            print(f"🔗 URL: {service['serviceDetails']['url']}")
            return service
        else:
            print(f"❌ Failed to create service: {response.status_code}")
            print(f"Error: {response.text}")
            return None
    
    def list_services(self):
        """List existing services"""
        response = requests.get(
            f"{self.base_url}/services",
            headers=self.headers
        )
        
        if response.status_code == 200:
            services = response.json()
            print(f"📋 Found {len(services)} services:")
            for service in services:
                print(f"  - {service['name']}: {service['serviceDetails']['url']}")
            return services
        else:
            print(f"❌ Failed to list services: {response.status_code}")
            return []
    
    def get_service_by_name(self, name):
        """Get service by name"""
        services = self.list_services()
        for service in services:
            if service['name'] == name:
                return service
        return None
    
    def trigger_deploy(self, service_id):
        """Trigger a new deployment"""
        response = requests.post(
            f"{self.base_url}/services/{service_id}/deploys",
            headers=self.headers
        )
        
        if response.status_code == 201:
            deploy = response.json()
            print(f"✅ Deployment triggered!")
            print(f"🚀 Deploy ID: {deploy['id']}")
            return deploy
        else:
            print(f"❌ Failed to trigger deploy: {response.status_code}")
            return None
    
    def check_deploy_status(self, service_id, deploy_id):
        """Check deployment status"""
        response = requests.get(
            f"{self.base_url}/services/{service_id}/deploys/{deploy_id}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            deploy = response.json()
            status = deploy['status']
            print(f"📊 Deploy status: {status}")
            return deploy
        else:
            print(f"❌ Failed to check deploy status: {response.status_code}")
            return None
    
    def wait_for_deploy(self, service_id, deploy_id, max_wait=600):
        """Wait for deployment to complete"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            deploy = self.check_deploy_status(service_id, deploy_id)
            
            if deploy:
                status = deploy['status']
                
                if status == 'live':
                    print("✅ Deployment completed successfully!")
                    return True
                elif status == 'build_failed' or status == 'failed':
                    print("❌ Deployment failed!")
                    return False
                else:
                    print(f"⏳ Deployment in progress: {status}")
                    time.sleep(30)
            else:
                break
        
        print("⏰ Deployment timeout")
        return False

def main():
    """Main deployment function"""
    deployer = RenderDeployer()
    
    print("🚀 Reddit AI Bot - Render Deployment")
    print("="*50)
    
    # Check if service already exists
    existing_service = deployer.get_service_by_name("reddit-ai-problem-solver")
    
    if existing_service:
        print(f"📍 Found existing service: {existing_service['serviceDetails']['url']}")
        
        # Trigger new deployment
        deploy = deployer.trigger_deploy(existing_service['id'])
        if deploy:
            print("⏳ Waiting for deployment...")
            success = deployer.wait_for_deploy(existing_service['id'], deploy['id'])
            
            if success:
                print(f"🎉 Bot deployed successfully!")
                print(f"🌐 URL: {existing_service['serviceDetails']['url']}")
                print(f"🔗 Test: {existing_service['serviceDetails']['url']}/test")
            else:
                print("❌ Deployment failed")
    else:
        print("🆕 Creating new service...")
        service = deployer.create_service()
        
        if service:
            print("⏳ Waiting for initial deployment...")
            # Initial deploy is automatic, just wait a bit
            time.sleep(60)
            print(f"🎉 Service created!")
            print(f"🌐 URL: {service['serviceDetails']['url']}")
    
    print("\n📋 Next Steps:")
    print("1. Test bot: Visit /test endpoint")
    print("2. Trigger run: Visit /run endpoint") 
    print("3. Setup GitHub Actions cron")
    print("4. Monitor with /stats endpoint")

if __name__ == "__main__":
    main()