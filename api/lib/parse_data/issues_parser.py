import json
from api import models, serializers
from api.lib import utils
from api.lib.feeback_to_admin import send_feedback


def parse_issues(owner, repository, issues):
    repo = models.Repository.objects.get(owner=owner, repository=repository)
    for item in issues:
        issue_attributes = {}

        issue_attributes["repository"] = repo.pk

        for key in item:
            _value = item.get(key, None)
            # if _value is not None:
                
            #     _t = type(_value)
            #     if _t == str:
            #         _value = _value.replace("\u0000", "*")
            #     elif _t == dict:
            #         _value = _value.replace("\u0000", "*")
            
            issue_attributes[utils.to_camel_case(key)] = _value
        
        # _str_json = json.dumps(issue_attributes)
        # _str_json = _str_json.replace("\u0000", "*")
        # issue_attributes = json.loads(_str_json)
        try:
            issue_serializer = serializers.FullIssueSerializer(data=issue_attributes)
            if issue_serializer.is_valid():
                issue_serializer.save()
        except Exception as error:
            send_feedback.send(f"Error {error}")
