from result_output import *
import sys
import json
import importlib.util
import urllib.request
from google.oauth2 import service_account
from pprint import pprint
from google.cloud import logging

class Activity():

    def testcase_check_App_Engine(self,test_object,credentials,project_id):
        testcase_description="Check App Engine name"
        expected_result="default"
        list_of_entries=[]
        i=0
        
        try:
            is_present = False
            actual = 'App Engine name is not '+ expected_result
            logger_name = "appengine.googleapis.com%2Frequest_log"
            logging_client = logging.Client(credentials=credentials)

            try:
                logger = logging_client.logger(logger_name)

                log_filter = (
                    f'resource.type="gae_app" '
                    f'resource.labels.module_id="{expected_result}" '
                )

                for entry in logger.list_entries(filter_=log_filter, page_size=10):
                    if i>=5:
                        break
                    list_of_entries.append(entry)
                    i=i+1
                    if (entry.resource.labels["module_id"] == "default"):
                        is_present=True
                        break

                if not list_of_entries:
                    is_present=False
                else:
                    is_present=True
                    actual=expected_result

            except Exception as e:
                is_present = False

            test_object.update_pre_result(testcase_description,expected_result)
            if is_present==True:
                test_object.update_result(1,expected_result,actual,"Congrats! You have done it right!"," ") 
            else:
                return test_object.update_result(0,expected_result,actual,"Check App Engine name","https://cloud.google.com/appengine/docs")   

        except Exception as e:    
            test_object.update_result(-1,expected_result,"Internal Server error","Please check with Admin","")
            test_object.eval_message["testcase_check_cloud_run_service_name"]=str(e)                

    def testcase_check_App_Engine_Region(self,test_object,credentials,project_id):
        testcase_description="Check App Engine Region"
        module_id="default"
        expected_result="us-east1"
        list_of_entries=[]
        i=0
        
        try:
            is_present = False
            actual = 'App Engine Region is not '+ expected_result
            logger_name = "appengine.googleapis.com%2Frequest_log"
            logging_client = logging.Client(credentials=credentials)

            try:
                logger = logging_client.logger(logger_name)

                log_filter = (
                    f'resource.type="gae_app" '
                    f'resource.labels.module_id="{module_id}" '
                )

                for entry in logger.list_entries(filter_=log_filter, page_size=10):
                    if i>=5:
                        break
                    list_of_entries.append(entry)
                    i=i+1
                    if "us-east1" in entry.resource.labels["zone"]:
                        is_present=True
                        break
                
                if not list_of_entries:
                    is_present=False
                else:
                    is_present=True
                    actual=expected_result

            except Exception as e:
                is_present = False

            test_object.update_pre_result(testcase_description,expected_result)
            if is_present==True:
                test_object.update_result(1,expected_result,actual,"Congrats! You have done it right!"," ") 
            else:
                return test_object.update_result(0,expected_result,actual,"Check App Engine Region","https://cloud.google.com/appengine/docs")   

        except Exception as e:    
            test_object.update_result(-1,expected_result,"Internal Server error","Please check with Admin","")
            test_object.eval_message["testcase_check_cloud_run_service_name"]=str(e)                

def start_tests(credentials, project_id, args):

    if "result_output" not in sys.modules:
        importlib.import_module("result_output")
    else:
        importlib.reload(sys.modules[ "result_output"])
    
    test_object=ResultOutput(args,Activity)
    challenge_test=Activity()
    challenge_test.testcase_check_App_Engine(test_object,credentials,project_id)
    challenge_test.testcase_check_App_Engine_Region(test_object,credentials,project_id)

    json.dumps(test_object.result_final(),indent=4)
    return test_object.result_final()

