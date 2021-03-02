import json 

try:
    from urllib.parse import unquote 
except ImportError:
     from urlparse import unquote



def data_format_s3(message):
    try:
        temp = message['Records'][0]['s3']['object']['key']
        temp = unquote(temp)
    except KeyError:
        raise Exception    
    
    return temp


def monitor_queue_yiel_result(queue, data_format, function):
        while True:
            messages = queue.get_sqs_message()
            for message in messages:
                formated_data = data_format(message)
                try:
                    data = function(formated_data)
                except:
                    raise TypeError

                return data

def monitor_queue_apply_function(queue, data_format, function):
        while True:
            messages = queue.get_sqs_message()
            for message in messages:
                formated_data = data_format(message)
                try:
                    function(formated_data)
                except:
                    raise TypeError

