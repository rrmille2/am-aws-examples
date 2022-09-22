#!/usr/bin/python3

# this python script will delete all your SageMaker Domains
# it does this by doing the following:
# 1. delete all SageMaker Apps
# 2. delete all SageMaker User Profiles
# 3. delete all SageMaker Domains

# as of 7/30/2021, SageMaker Domains have the following restrictions:
# 1. you can only have one Sagemaker Domain
# 2. a SageMaker Domain must use either IAM or SSO and this is specified at Domain creation time
# 3. the method of authorization cannot be changed, you must delete the domain and re-create

import json
import boto3

session = boto3.session.Session(profile_name='rrmille-am-admin')
sm = session.client('sagemaker')

print('deleting apps...')
response = sm.list_apps()
for app in response['Apps']:
	try:
		response = sm.delete_app(
			DomainId = app['DomainId'],
			UserProfileName = app['UserProfileName'],
			AppType = app['AppType'],
			AppName = app['AppName'] )
	except:
		pass

print('deleting user profiles...')
response = sm.list_user_profiles()
for user in response['UserProfiles']:
	try:
		response = sm.delete_user_profile(
			DomainId = user['DomainId'],
			UserProfileName = user['UserProfileName'] )
	except:
		pass
	
print('deleting domains...')
response = sm.list_domains()
for domain in response['Domains']:
	try:
		response = sm.delete_domain(
			DomainId = domain['DomainId'],
			RetentionPolicy = { 'HomeEfsFileSystem' : 'Retain' } )
	except:
		pass


print('done')
